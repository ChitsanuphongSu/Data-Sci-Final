(() => {
  'use strict';
  const data=window.quickData, key=`ds-${data.slug}-v1`, chapters=[7,8,9,10,11,12];
  const $=s=>document.querySelector(s), area=$('#quick-questions'), result=$('#quick-result');
  let state={chapter:7,answers:{},graded:{}}, wrongOnly=false, storageOK=true, recovered=false;
  const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
  try {
    const saved=JSON.parse(localStorage.getItem(key)||'null');
    if(saved!==null){
      if(!object(saved)||!object(saved.answers)||!object(saved.graded)) recovered=true;
      else {
        if(chapters.includes(saved.chapter))state.chapter=saved.chapter;
        for(const [i,v] of Object.entries(saved.answers))
          if(/^\d+$/.test(i)&&Number(i)<data.questions.length&&Number.isInteger(v)&&v>=0&&v<4)state.answers[i]=v;
        for(const ch of chapters)state.graded[ch]=saved.graded[ch]===true;
      }
    }
  } catch(e){if(e instanceof SyntaxError)recovered=true;else storageOK=false;}
  function warning(){ $('#quick-warning').hidden=false; $('#quick-warning').textContent='บันทึกอัตโนมัติไม่ได้ คำตอบยังอยู่ในหน้านี้ กรุณาดาวน์โหลดก่อนปิดหรือรีโหลด'; }
  function save(){try{localStorage.setItem(key,JSON.stringify(state));}catch{storageOK=false;warning();}}
  if(!storageOK)warning();
  if(recovered){$('#quick-warning').hidden=false;$('#quick-warning').textContent='ข้อมูลที่บันทึกอ่านไม่ได้ ระบบเริ่มสถานะใหม่อย่างปลอดภัย';}
  function items(ch=state.chapter){return data.questions.map((q,i)=>({q,i})).filter(x=>x.q.ch===ch);}
  function score(list){return list.filter(({q,i})=>state.answers[i]===q.answer).length;}
  function el(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
  function progress(){
    const list=items(), answered=list.filter(({i})=>state.answers[i]!==undefined).length;
    $('#quick-progress').textContent=`บท ${state.chapter} · ตอบแล้ว ${answered}/${list.length} ข้อ · ตรวจคำตอบแล้ว ${chapters.filter(ch=>state.graded[ch]).length}/6 บท`;
    for(const b of document.querySelectorAll('[data-quick-chapter]')){
      const ch=Number(b.dataset.quickChapter), subset=items(ch), count=subset.filter(({i})=>state.answers[i]!==undefined).length;
      b.textContent=`บท ${ch} · ${state.graded[ch]?score(subset)+'/15 คะแนน':count+'/15 ตอบ'}`;
      b.setAttribute('aria-pressed',String(ch===state.chapter));
    }
  }
  function render(){
    $('#quick-chapter').value=String(state.chapter);
    $('#quick-heading').textContent=`บท ${state.chapter} · ${data.titles[state.chapter]}`;
    $('#quick-review').href=`chapter-${String(state.chapter).padStart(2,'0')}.html`;
    $('#quick-prev').disabled=state.chapter===7;$('#quick-next').disabled=state.chapter===12;
    $('#quick-wrong').textContent=wrongOnly?'แสดงทุกข้อในบท':'ทบทวนข้อผิด / ยังไม่ตอบ';
    $('#quick-wrong').setAttribute('aria-pressed',String(wrongOnly));
    $('#quick-wrong').disabled=!state.graded[state.chapter];
    area.replaceChildren();result.replaceChildren();
    const list=items();progress();
    if(state.graded[state.chapter]){
      const card=el('div',undefined,'result-card'), correct=score(list), blank=list.filter(({i})=>state.answers[i]===undefined).length;
      card.append(el('h3',`บท ${state.chapter}: ${correct}/${list.length} · ${Math.round(correct/list.length*100)}%`),el('p',`ไม่ตอบ ${blank} ข้อ · อ่านเหตุผลใต้แต่ละข้อ คะแนนนี้เป็นการฝึก ไม่ใช่เกณฑ์ผ่านของผู้สอน`));result.append(card);
    }
    let shown=0;
    list.forEach(({q,i},localIndex)=>{
      if(wrongOnly&&state.answers[i]===q.answer)return;
      shown++;
      const field=el('fieldset',undefined,'question');field.id='quick-q'+i;
      const legend=el('legend');legend.append(el('span',q.topic,'chapter-chip'),document.createElement('br'),document.createTextNode(`${localIndex+1}. ${q.stem}`));field.append(legend);
      q.options.forEach((option,j)=>{
        const label=el('label'), input=el('input');input.type='radio';input.name='quick-q'+i;input.value=j;input.checked=state.answers[i]===j;
        if(state.graded[state.chapter]){if(j===q.answer)label.classList.add('quick-correct-option');else if(input.checked)label.classList.add('quick-wrong-option');}
        input.addEventListener('change',()=>{
          state.answers[i]=j;
          if(state.graded[state.chapter]){
            state.graded[state.chapter]=false;wrongOnly=false;save();render();
            area.querySelector(`#quick-q${i} input[value="${j}"]`)?.focus();
          }else{save();progress();}
        });
        label.append(input,el('span',`${String.fromCharCode(65+j)}. ${option}`));field.append(label);
      });
      if(state.graded[state.chapter]){
        const correct=state.answers[i]===q.answer;field.classList.add(correct?'correct':'incorrect');
        const feedback=el('div',undefined,'feedback');
        feedback.append(el('strong',`${correct?'✓ ถูกต้อง':state.answers[i]===undefined?'ยังไม่ได้ตอบ':'คำตอบยังไม่ถูก'} · เฉลย ${String.fromCharCode(65+q.answer)}. ${q.options[q.answer]}`),el('p',q.why));
        const a=el('a',`ทบทวนบท ${q.ch} →`);a.href=`chapter-${String(q.ch).padStart(2,'0')}.html`;feedback.append(a);field.append(feedback);
      }
      area.append(field);
    });
    if(!shown)area.append(el('p','ถูกครบทุกข้อในบทนี้แล้ว ลองอีกชุดหรือทบทวนเหตุผลด้วยการอธิบายจากความจำ','note'));
  }
  function select(ch){state.chapter=ch;wrongOnly=false;save();render();$('#quick-heading').focus();}
  $('#quick-chapter').addEventListener('change',e=>select(Number(e.target.value)));
  document.querySelectorAll('[data-quick-chapter]').forEach(b=>b.addEventListener('click',()=>select(Number(b.dataset.quickChapter))));
  $('#quick-prev').addEventListener('click',()=>select(Math.max(7,state.chapter-1)));
  $('#quick-next').addEventListener('click',()=>select(Math.min(12,state.chapter+1)));
  for(const button of [$('#quick-grade'),$('#quick-grade-bottom')])button.addEventListener('click',()=>{state.graded[state.chapter]=true;wrongOnly=false;save();render();result.focus();result.scrollIntoView({behavior:'smooth',block:'start'});});
  $('#quick-wrong').addEventListener('click',()=>{wrongOnly=!wrongOnly;render();});
  $('#quick-reset').addEventListener('click',()=>{
    const ch=state.chapter, dialog=$('#quick-confirm');
    $('#quick-confirm-text').textContent=`ล้างคำตอบและคะแนนเฉพาะบท ${ch} ในชุดนี้? บทอื่นและอีกชุดจะยังอยู่`;
    dialog.showModal();$('#quick-cancel').focus();
  });
  $('#quick-cancel').addEventListener('click',()=>$('#quick-confirm').close());
  $('#quick-confirm-yes').addEventListener('click',()=>{for(const {i} of items())delete state.answers[i];delete state.graded[state.chapter];wrongOnly=false;save();$('#quick-confirm').close();render();$('#quick-heading').focus();});
  $('#quick-export').addEventListener('click',()=>{
    const payload={schemaVersion:1,assessment:data.slug,exportedAt:new Date().toISOString(),...state,
      responses:data.questions.map((q,i)=>({chapter:q.ch,topic:q.topic,question:q.stem,selected:state.answers[i]===undefined?null:q.options[state.answers[i]],correct:state.graded[q.ch]?state.answers[i]===q.answer:null,explanation:state.graded[q.ch]?q.why:null}))};
    const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
    const a=el('a');a.href=url;a.download=data.slug+'-answers.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  render();
})();
