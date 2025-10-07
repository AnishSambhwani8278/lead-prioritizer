let scoredLeads = [];

const loader = document.getElementById('loader');

document.getElementById('uploadBtn').addEventListener('click',()=>{
    const file = document.getElementById('csvFile').files[0];
    if(!file){alert("Select a CSV"); return;}
    
    loader.style.display = 'block';
    scoredLeads = [];
    renderTable([]); 

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/score', { method:'POST', body: formData })
    .then(r => r.json())
    .then(data => {
        loader.style.display = 'none';
        if(data.status==='success'){
            scoredLeads = data.leads;
            renderTable(scoredLeads);
        } else {
            alert(data.message);
        }
    })
    .catch(err => {
        loader.style.display = 'none';
        alert('Error: ' + err);
    });
});


document.getElementById('downloadBtn').addEventListener('click', () => {
    if (scoredLeads.length === 0) { alert("No data"); return; }
    fetch('http://127.0.0.1:5000/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ leads: scoredLeads })
    }).then(resp => resp.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'prioritized_leads.csv';
            a.click();
        });
});

function renderTable(data){
    const table = document.getElementById('resultsTable');
    table.innerHTML='';
    if(data.length===0) return;

    const headers = Object.keys(data[0]);
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headers.forEach(h=>{
        const th = document.createElement('th');
        th.innerText = h;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement('tbody');
    data.forEach(row=>{
        const tr = document.createElement('tr');
        headers.forEach(h=>{
            const td = document.createElement('td');
            td.innerText = row[h];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
}

