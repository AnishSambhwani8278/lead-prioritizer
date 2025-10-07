from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

CORS(app)

TITLE_WEIGHTS = {'ceo':30,'founder':25,'cto':20,'cfo':20,'head':15,'manager':5,'engineer':2,'intern':-5}
COMPANY_SIZE_WEIGHTS = {'1-10':-5,'11-50':5,'51-200':10,'201-1000':15,'1001+':20}

def score_row(row):
    s = 0
    title = str(row.get('title','')).lower()
    for k,v in TITLE_WEIGHTS.items():
        if k in title: s+=v
    email = str(row.get('email',''))
    try:
        validate_email(email)
        if any(domain in email for domain in ['mailinator.com','tempmail.com','example.com']): s-=10
        else: s+=10
    except: s-=20
    cs = str(row.get('company_size',''))
    s += COMPANY_SIZE_WEIGHTS.get(cs,0)
    loc = str(row.get('location','')).lower()
    if 'remote' in loc: s+=2
    return s

def dedupe_df(df):
    df['email_lower'] = df['email'].str.lower().fillna('')
    df = df.drop_duplicates(subset=['email_lower']).drop(columns=['email_lower'])
    return df

@app.route('/score', methods=['POST'])
def score_csv():
    file = request.files.get('file')
    if not file: 
        return jsonify({'status':'error','message':'No file uploaded'}), 400

    df = pd.read_csv(file)
    for col in ['name','title','company','email','domain','location','company_size']:
        if col not in df.columns: 
            df[col] = ''
    
    df = dedupe_df(df)
    df['score'] = df.apply(score_row, axis=1)
    df = df.sort_values('score', ascending=False)

    # Convert NaN to None so jsonify can handle it
    result = df.where(pd.notnull(df), None).to_dict(orient='records')
    return jsonify({'status':'success','leads': result})


@app.route('/sample', methods=['GET'])
def sample_data():
    df = pd.read_csv('sample_leads.csv')
    return jsonify({'status':'success','leads':df.to_dict(orient='records')})

@app.route('/download', methods=['POST'])
def download_csv():
    data = request.get_json()
    df = pd.DataFrame(data.get('leads',[]))
    buf = io.StringIO()
    df.to_csv(buf,index=False)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode()),mimetype='text/csv',as_attachment=True,download_name='prioritized_leads.csv')

if __name__=='__main__':
    app.run(debug=True)
