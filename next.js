// fetch live info
fetch('http://localhost:5000/api/live')
.then(res => res.json())
.then(data => {
    document.getElementById('liveplayer').src = data.streamUrl;
    
    document.getElementById('liveTitle').innerText = data.title;
});

//fetch schedule
fetch('http://localhost:5000/api/program')
.then(res => res.json())
.then(programs => {
    const list = 
    document.getElementById('programList');
    programs.forEach(p => {
        list.innerHTML += 
         `<div><span>${p.time} - ${p.title} </span><span style="color:$ 
         {p.status=='live'?'red':'#999'}">$
         {p.status}</span></div>`;
    });
});