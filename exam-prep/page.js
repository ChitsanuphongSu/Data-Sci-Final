const pageSlug=document.body.dataset.page;
const readButton=document.querySelector('#mark-read');
function getRead(){try{const v=JSON.parse(localStorage.getItem('ds-read')||'[]');return Array.isArray(v)?v.filter(x=>typeof x==='string'):[]}catch{return []}}
function renderRead(){const read=getRead().includes(pageSlug);readButton.textContent=read?'✓ อ่านแล้ว — ยกเลิกเครื่องหมาย':'ทำเครื่องหมายอ่านแล้ว';readButton.setAttribute('aria-pressed',String(read))}
renderRead();
readButton.addEventListener('click',()=>{let read=getRead();read=read.includes(pageSlug)?read.filter(s=>s!==pageSlug):[...read,pageSlug];try{localStorage.setItem('ds-read',JSON.stringify(read));renderRead();parent.postMessage({type:'ds-progress'},'*')}catch{readButton.textContent='เบราว์เซอร์ไม่อนุญาตบันทึกความคืบหน้า'}});
document.querySelectorAll('.code-wrap').forEach(block=>{
 const pre=block.querySelector('pre'),copy=block.querySelector('.copy');
 block.querySelector('.wrap-code')?.addEventListener('click',e=>{e.currentTarget.setAttribute('aria-pressed',String(block.classList.toggle('wrapped')))});
 block.querySelector('.expand-code')?.addEventListener('click',e=>{const expanded=block.classList.toggle('expanded');e.currentTarget.setAttribute('aria-expanded',String(expanded));e.currentTarget.textContent=expanded?'ย่อ':'ขยาย'});
 copy.addEventListener('click',async()=>{
  const text=pre.querySelector('code').textContent;
  let ok=false;
  try{await navigator.clipboard.writeText(text);ok=true}catch{
   const ta=document.createElement('textarea');ta.value=text;ta.style.cssText='position:fixed;left:-9999px';document.body.append(ta);ta.select();
   try{ok=document.execCommand('copy')}catch{}finally{ta.remove();copy.focus()}
  }
  copy.textContent=ok?'คัดลอกแล้ว':'เลือกโค้ดเพื่อคัดลอก';setTimeout(()=>copy.textContent='คัดลอก',2200);
 });
});
window.addEventListener('storage',renderRead);
if(parent!==window)parent.postMessage({type:'ds-page',slug:pageSlug},'*');
