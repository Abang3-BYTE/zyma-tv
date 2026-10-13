async function loadTV(){
  try{
    let res = await fetch('http://127.0.0.1:5000/api/live');
    let live = await res.json();
    document.getElementById('liveplayer').src = live.streamUrl;
    document.getElementById('liveTitle').innerText = live.title;
  }catch(e){
    document.getElementById('liveplayer').src = "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1&mute=1";
    document.getElementById('liveTitle').innerText = "LIVE: ZYMA TV Studio - Abuja (Offline Demo)";
  }

  try{
    let res2 = await fetch('http://127.0.0.1:5000/api/programs');
    let programs = await res2.json();
    let html = "";
    programs.forEach(p=>{
      html += `<div class="program ${p.status}"><span>${p.time} - ${p.title}</span><span>${p.status}</span></div>`;
    });
    document.getElementById('programList').innerHTML = html;
  }catch(e){
    document.getElementById('programList').innerHTML = "Backend not running. Run python backend.py";
  }
}
loadTV();


async function loadChat(){
  let res = await fetch('http://127.0.0.1:5000/api/chat');
  let chats = await res.json();
  document.getElementById('chatBox').innerHTML = chats.map(c=>`<div><b>${c.user}:</b> ${c.text}</div>`).join('');
}
async function sendChat(){
  let user = document.getElementById('chatName').value || 'Viewer';
  let text = document.getElementById('chatText').value;
  if(!text) return;
  await fetch('http://127.0.0.1:5000/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user,text})});
  document.getElementById('chatText').value=''; loadChat();
}
setInterval(loadChat,2000);
loadChat();