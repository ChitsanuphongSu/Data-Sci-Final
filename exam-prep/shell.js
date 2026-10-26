const reader=document.querySelector('#reader'), shell=document.querySelector('#shell');
const slugs=new Set(sitePages.map(p=>p.slug));
function progress(){let read=[];try{const saved=JSON.parse(localStorage.getItem('ds-read')||'[]');read=Array.isArray(saved)?[...new Set(saved.filter(x=>typeof x==='string'))]:[]}catch{}document.querySelector('#progress').textContent=`อ่านแล้ว ${read.filter(s=>slugs.has(s)).length} / ${sitePages.length} หมวด`;document.querySelectorAll('[data-slug]').forEach(a=>a.classList.toggle('done',read.includes(a.dataset.slug)))}
function active(slug){document.querySelectorAll('[data-slug]').forEach(a=>{a.classList.toggle('active',a.dataset.slug===slug);if(a.dataset.slug===slug)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')})}
function route(){const requested=location.hash.slice(1),slug=slugs.has(requested)?requested:'overview';const target=`exam-prep/${slug}.html`;reader.src=target;active(slug);shell.classList.remove('menu-open');document.querySelector('.menu-toggle').setAttribute('aria-expanded','false');document.querySelector('#search-results').hidden=true}
window.addEventListener('hashchange',route);
window.addEventListener('message',e=>{if(e.source!==reader.contentWindow)return;if(e.data?.type==='ds-progress')progress();if(e.data?.type==='ds-page'&&slugs.has(e.data.slug)){history.replaceState(null,'','#'+e.data.slug);reader.setAttribute('data-current',e.data.slug);active(e.data.slug)}});
window.addEventListener('storage',progress);
document.querySelector('.menu-toggle').addEventListener('click',e=>{const open=shell.classList.toggle('menu-open');e.currentTarget.setAttribute('aria-expanded',String(open))});
const search=document.querySelector('#search'), results=document.querySelector('#search-results');
search.addEventListener('input',()=>{const term=search.value.trim().toLocaleLowerCase();results.replaceChildren();if(!term){results.hidden=true;return}let count=0;for(const p of searchData){const at=p.text.toLocaleLowerCase().indexOf(term);if(at<0&&!p.title.toLocaleLowerCase().includes(term))continue;count++;const a=document.createElement('a');a.className='search-hit';a.href='#'+p.slug;const title=document.createElement('strong');title.textContent=p.title;const excerpt=document.createElement('small');excerpt.textContent=p.text.slice(Math.max(0,at-50),Math.max(0,at-50)+190)+'…';a.append(title,excerpt);a.addEventListener('click',()=>{results.hidden=true;search.value='';if(location.hash==='#'+p.slug){reader.src=`exam-prep/${p.slug}.html`;active(p.slug)}});results.append(a)}if(!count)results.textContent='ไม่พบคำนี้ ลองใช้คำไทยหรือชื่อภาษาอังกฤษ';results.hidden=false});
search.addEventListener('keydown',e=>{if(e.key==='Escape'){results.hidden=true;search.value=''}});
route();progress();


// Keyboard users can dismiss navigation/search without moving focus off-screen.
document.addEventListener('keydown',e=>{if(e.key==='Escape'){results.hidden=true;if(shell.classList.contains('menu-open')){shell.classList.remove('menu-open');const toggle=document.querySelector('.menu-toggle');toggle.setAttribute('aria-expanded','false');toggle.focus()}}});
document.addEventListener('click',e=>{if(!results.contains(e.target)&&e.target!==search)results.hidden=true});
