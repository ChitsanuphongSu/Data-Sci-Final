(() => {
  const data=window.assessmentData, exam=data.kind==='mock-exam', key='ds-'+data.kind+'-v1';
  const area=document.querySelector('#assessment'), result=document.querySelector('#result');
  let state={answers:{},written:{},self:{},graded:false,started:false,deadline:null,filter:'all'}, storageOK=true, onlyWrong=false;
  let recovered=false;
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  try{
    const raw=localStorage.getItem(key),saved=JSON.parse(raw||'null');
    if(saved){
      if(!object(saved)||!object(saved.answers)){recovered=true}
      else{
        for(const [i,v] of Object.entries(saved.answers))if(/^\d+$/.test(i)&&Number(i)<data.questions.length&&Number.isInteger(v)&&v>=0&&v<4)state.answers[i]=v;
        for(const [i,v] of Object.entries(object(saved.written)?saved.written:{}))if(data.written[i]&&typeof v==='string')state.written[i]=v;
        for(const [i,v] of Object.entries(object(saved.self)?saved.self:{}))if(data.written[i]&&(v===''||typeof v==='number'&&Number.isFinite(v)))state.self[i]=v===''?'':Math.min(data.written[i].points,Math.max(0,v));
        state.filter=['all','7','8','9','10','11','12'].includes(saved.filter)?saved.filter:'all';
        state.graded=saved.graded===true;state.started=saved.started===true;
        state.deadline=Number.isFinite(saved.deadline)&&saved.deadline>0?saved.deadline:null;
        state.autoSubmit=saved.autoSubmit===true;
        if(Number.isFinite(saved.finishedAt))state.finishedAt=saved.finishedAt;
        if(exam&&state.started&&!state.graded&&!state.deadline){state.started=false;recovered=true}
      }
    }
  }catch(error){if(error instanceof SyntaxError)recovered=true;else storageOK=false}
  function save(){try{localStorage.setItem(key,JSON.stringify(state))}catch{storageOK=false;showStorageWarning()}}
  function showStorageWarning(){if(document.querySelector('.storage-warning'))return;const n=document.createElement('p');n.className='storage-warning';n.textContent='เบราว์เซอร์ไม่อนุญาตบันทึกอัตโนมัติ กรุณาอย่ารีโหลดระหว่างทำ และดาวน์โหลดคำตอบก่อนออก';result.before(n)}
  if(!storageOK)showStorageWarning();
  if(recovered){const notice=document.createElement('p');notice.className='recovered-state';notice.textContent='ข้อมูลที่บันทึกบางส่วนอ่านไม่ได้ ระบบคืนสถานะที่ปลอดภัยแล้ว กรุณาตรวจคำตอบก่อนเริ่มต่อ';result.before(notice)}
  const progress=document.createElement('p');progress.className='assessment-progress';area.before(progress);
  function updateProgress(){const ids=data.questions.map((q,i)=>({q,i})).filter(({q})=>exam||state.filter==='all'||q.ch===Number(state.filter));progress.textContent=`ตอบปรนัยแล้ว ${ids.filter(({i})=>state.answers[i]!==undefined).length} / ${ids.length} ข้อ`+(exam?` · เขียนอัตนัยแล้ว ${data.written.filter((_,i)=>(state.written[i]||'').trim()).length} / ${data.written.length} ข้อ`:'')}
  function expired(){if(exam&&state.started&&!state.graded&&Date.now()>=state.deadline){submit(true);return true}return false}
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function askConfirm(message){return new Promise(resolve=>{const dialog=document.createElement('dialog');dialog.setAttribute('aria-label','ยืนยันการทำรายการ');dialog.style.cssText='max-width:520px;border:1px solid #cad6cc;border-radius:14px;padding:28px;color:#172c32';const p=document.createElement('p');p.textContent=message;const yes=document.createElement('button'),no=document.createElement('button');yes.textContent='ยืนยัน';no.textContent='ยกเลิก';no.className='secondary';no.style.marginLeft='10px';function finish(value){dialog.close();dialog.remove();resolve(value)}yes.onclick=()=>finish(true);no.onclick=()=>finish(false);dialog.addEventListener('cancel',e=>{e.preventDefault();finish(false)});dialog.append(p,yes,no);document.body.append(dialog);dialog.showModal();no.focus()})}
  function visible(){return data.questions.map((q,i)=>({q,i})).filter(({q,i})=>(exam||state.filter==='all'||q.ch===Number(state.filter))&&(!onlyWrong||state.answers[i]!==q.answer))}
  function score(items){return items.filter(({q,i})=>state.answers[i]===q.answer).length}
  function renderQuestions(){
    area.innerHTML='';
    updateProgress();
    if(!exam)document.querySelector('#wrong-only').textContent=onlyWrong?'แสดงทุกข้อ':'ทบทวนข้อที่ผิด';
    const items=visible();
    if(!items.length){area.innerHTML='<p class="note">ไม่มีข้อผิดในหมวดที่เลือก</p>';return}
    for(const {q,i} of items){
      const field=document.createElement('fieldset');field.className='question';field.id='q'+i;
      field.innerHTML=`<legend><span class="chapter-chip">บท ${q.ch} · ${exam?'2.5 คะแนน':'ฝึกทบทวน'}</span><br>${i+1}. ${escape(q.stem)}</legend>`;
      q.options.forEach((option,j)=>{
        const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');
        input.type='radio';input.name='q'+i;input.value=j;input.checked=state.answers[i]===j;
        input.disabled=exam&&(!state.started||state.graded);text.textContent=String.fromCharCode(65+j)+'. '+option;
        input.addEventListener('change',()=>{if(expired())return;state.answers[i]=j;if(!exam&&state.graded){state.graded=false;onlyWrong=false;save();renderQuestions();result.innerHTML='';return}save();updateProgress()});
        label.append(input,text);field.append(label);
      });
      if(state.graded){const correct=state.answers[i]===q.answer;field.classList.add(correct?'correct':'incorrect');const f=document.createElement('div');f.className='feedback';f.innerHTML=`<strong>${correct?'✓ ถูกต้อง':state.answers[i]===undefined?'ยังไม่ได้ตอบ':'คำตอบยังไม่ถูก'} · เฉลย ${String.fromCharCode(65+q.answer)}</strong><br>${escape(q.why)}<br><a href="chapter-${String(q.ch).padStart(2,'0')}.html">ทบทวนบท ${q.ch} →</a>`;field.append(f)}
      area.append(field);
    }
  }
  function renderResult(){
    if(!state.graded){result.innerHTML='';return}
    const items=data.questions.map((q,i)=>({q,i})).filter(({q})=>exam||state.filter==='all'||q.ch===Number(state.filter));
    const correct=score(items), unanswered=items.filter(({i})=>state.answers[i]===undefined).length;
    const breakdown=[7,8,9,10,11,12].map(ch=>{const subset=items.filter(({q})=>q.ch===ch);return subset.length?`<a href="chapter-${String(ch).padStart(2,'0')}.html">บท ${ch}: ${score(subset)}/${subset.length}</a>`:''}).filter(Boolean).join(' · ');
    if(exam){const self=Object.entries(state.self).reduce((sum,[i,v])=>sum+Math.min(data.written[i]?.points||0,Math.max(0,Number(v)||0)),0);const marked=data.written.filter((_,i)=>state.self[i]!==undefined&&state.self[i]!=='').length;result.innerHTML=`<div class="result-card"><h2>ปรนัย ${correct*2.5} / 60 คะแนน</h2><p>ถูก ${correct}/${items.length} ข้อ · ไม่ตอบ ${unanswered} ข้อ<br>อัตนัยตรวจตนเอง ${self} / 40 (${marked}/6 ข้อ) · รวมเบื้องต้น ${correct*2.5+self} / 100</p><p>${marked<6?'ยังตรวจอัตนัยไม่ครบ คะแนนรวมยังไม่สมบูรณ์':'คะแนนอัตนัยเป็นการประเมินตนเอง ไม่ใช่คะแนนจากผู้สอน'}</p><p>${breakdown}</p></div>`}
    else result.innerHTML=`<div class="result-card"><h2>${correct} / ${items.length} ข้อ · ${Math.round(correct/items.length*100)}%</h2><p>ไม่ตอบ ${unanswered} ข้อ · อ่านเหตุผลใต้แต่ละข้อ แล้วกลับไปทบทวนหัวข้อที่ผิด</p><p>${breakdown}</p></div>`;
  }
  function renderWritten(){if(!exam)return;const container=document.querySelector('#written');container.innerHTML='';data.written.forEach((w,i)=>{const section=document.createElement('section');section.innerHTML=`<h2>${escape(w.title)} · ${w.points} คะแนน</h2><p>${escape(w.prompt)}</p>`;const ta=document.createElement('textarea');ta.setAttribute('aria-label','คำตอบ '+w.title);ta.value=state.written[i]||'';ta.disabled=!state.started||state.graded;ta.placeholder='เขียนคำตอบ วิธีคำนวณ หรือ pseudocode ที่นี่…';ta.addEventListener('input',()=>{if(expired())return;state.written[i]=ta.value;save();updateProgress()});section.append(ta);if(state.graded){const detail=document.createElement('details');detail.className='recall';detail.open=true;detail.innerHTML=`<summary>แนวคำตอบและเกณฑ์ให้คะแนน</summary><p>${escape(w.answer)}</p><ul>${w.rubric.map(x=>`<li>${escape(x)}</li>`).join('')}</ul>`;const label=document.createElement('label');label.textContent=`คะแนนที่ตรวจเอง (0–${w.points}): `;const input=document.createElement('input');input.className='self-score';input.type='number';input.min=0;input.max=w.points;input.step=.5;input.value=state.self[i]??'';input.setAttribute('aria-label','คะแนนตรวจเอง '+w.title);input.addEventListener('input',()=>{if(input.value==='')state.self[i]='';else{state.self[i]=Math.min(w.points,Math.max(0,Number(input.value)||0));input.value=state.self[i]}save();renderResult()});label.append(input);detail.append(label);section.append(detail)}container.append(section)})}
  function submit(auto=false){if(!state.started||state.graded)return;auto=auto||Date.now()>=state.deadline;state.graded=true;state.finishedAt=Date.now();state.autoSubmit=auto;save();renderQuestions();renderWritten();renderResult();updateTimer();if(!auto)result.scrollIntoView({behavior:'smooth'})}
  function updateTimer(){if(!exam)return;const timer=document.querySelector('#timer'),status=document.querySelector('#exam-state');document.querySelector('#start-exam').disabled=state.started;document.querySelector('#submit-exam').disabled=!state.started||state.graded;if(state.graded){timer.textContent='ส่งแล้ว';status.textContent=state.autoSubmit?'หมดเวลา · ส่งอัตโนมัติ':'ตรวจปรนัยแล้ว · ตรวจอัตนัยด้วย rubric';return}if(!state.started){timer.textContent='120:00';status.textContent='พร้อมเริ่ม';return}const seconds=Math.max(0,Math.ceil((state.deadline-Date.now())/1000));timer.textContent=`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;status.textContent='กำลังสอบ · บันทึกคำตอบในเครื่อง';if(seconds===0)submit(true)}
  document.querySelector('#reset').addEventListener('click',async()=>{if((Object.keys(state.answers).length||state.started)&&!await askConfirm('เริ่มใหม่และล้างคำตอบชุดนี้? ดาวน์โหลดคำตอบก่อนหากต้องการเก็บ'))return;state={answers:{},written:{},self:{},graded:false,started:false,deadline:null,filter:'all'};onlyWrong=false;save();if(!exam){document.querySelector('#chapter-filter').value='all';document.querySelector('#wrong-only').textContent='ทบทวนข้อที่ผิด'}renderQuestions();renderWritten();renderResult();updateTimer()});
  document.querySelector('#export').addEventListener('click',()=>{const payload={assessment:data.kind,exportedAt:new Date().toISOString(),...state,schemaVersion:1,responses:data.questions.map((q,i)=>({number:i+1,chapter:q.ch,question:q.stem,selectedOption:state.answers[i]===undefined?null:q.options[state.answers[i]],correct:state.graded?state.answers[i]===q.answer:null})),writtenResponses:data.written.map((w,i)=>({question:w.title,prompt:w.prompt,answer:state.written[i]||'',selfScore:state.self[i]??null,maxScore:w.points})),questionCount:data.questions.length,correct:state.graded?score(data.questions.map((q,i)=>({q,i}))):null};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=data.kind+'-answers.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
  if(exam){document.querySelector('#start-exam').addEventListener('click',()=>{state.started=true;state.deadline=Date.now()+120*60*1000;save();renderQuestions();renderWritten();updateTimer()});document.querySelector('#submit-exam').addEventListener('click',async()=>{const unanswered=data.questions.filter((_,i)=>state.answers[i]===undefined).length;if(!await askConfirm(`ส่งคำตอบและเปิดเฉลย? ยังไม่ตอบปรนัย ${unanswered} ข้อ หลังส่งจะแก้คำตอบไม่ได้`))return;submit()});setInterval(updateTimer,1000)}
  else{const select=document.querySelector('#chapter-filter');select.value=state.filter;select.addEventListener('change',()=>{state.filter=select.value;onlyWrong=false;save();renderQuestions();renderResult()});document.querySelector('#grade').addEventListener('click',()=>{state.graded=true;onlyWrong=false;save();renderQuestions();renderResult();result.scrollIntoView({behavior:'smooth'})});document.querySelector('#wrong-only').addEventListener('click',()=>{if(!state.graded){result.innerHTML='<p class="note">กดตรวจคำตอบก่อน เพื่อกรองข้อที่ผิด</p>';return}onlyWrong=!onlyWrong;document.querySelector('#wrong-only').textContent=onlyWrong?'แสดงทุกข้อ':'ทบทวนข้อที่ผิด';renderQuestions()})}
  renderQuestions();renderWritten();renderResult();updateTimer();
})();
