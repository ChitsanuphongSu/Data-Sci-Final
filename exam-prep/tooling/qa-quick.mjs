import assert from 'node:assert/strict';
import {JSDOM,VirtualConsole} from 'jsdom';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const checks=[];
async function test(name,fn){await fn();checks.push(name);console.log('PASS',name);}
async function setup(n,saved,blocked=false){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(await readFile(`${root}quick-quiz-${n}.html`,'utf8'),{url:'https://example.test/exam-prep/',runScripts:'outside-only',virtualConsole:vc});
 const w=dom.window,key=`ds-quick-quiz-${n}-v1`,doc=w.document;
 w.Element.prototype.scrollIntoView=()=>{};
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};
 if(saved!==undefined)w.localStorage.setItem(key,typeof saved==='string'?saved:JSON.stringify(saved));
 if(blocked)Object.defineProperty(w,'localStorage',{value:{getItem(){throw new w.DOMException('blocked','SecurityError')},setItem(){throw new w.DOMException('blocked','SecurityError')}}});
 w.eval([...doc.scripts].find(s=>s.textContent.includes('window.quickData=')).textContent);
 w.eval(await readFile(root+'quick-quiz.js','utf8'));
 return {w,doc,key,errors,close:()=>dom.window.close()};
}
const click=(e,s)=>e.doc.querySelector(s).click();
function select(e,ch){const s=e.doc.querySelector('#quick-chapter');s.value=ch;s.dispatchEvent(new e.w.Event('change'));}
function answer(e,i,value){const r=e.doc.querySelector(`#quick-q${i} input[value="${value}"]`);assert.ok(r);r.checked=true;r.dispatchEvent(new e.w.Event('change'));}
for(const n of [1,2]){
 await test(`Set ${n}: all six chapters score 15/15 independently; 90 unique questions`,async()=>{
  const e=await setup(n),qs=e.w.quickData.questions;assert.equal(qs.length,90);assert.equal(new Set(qs.map(q=>q.stem)).size,90);
  for(const ch of [7,8,9,10,11,12]){
   select(e,ch);assert.equal(e.doc.querySelectorAll('fieldset').length,15);assert.equal(e.doc.querySelectorAll('.feedback').length,0);
   qs.forEach((q,i)=>{if(q.ch===ch)answer(e,i,q.answer)});click(e,'#quick-grade');
   assert.match(e.doc.querySelector('#quick-result').textContent,/15\/15 · 100%/);assert.equal(e.doc.querySelectorAll('.correct').length,15);
   assert.equal(e.doc.querySelectorAll('.feedback a').length,15);
  }
  const state=JSON.parse(e.w.localStorage.getItem(e.key));assert.equal(Object.values(state.graded).filter(Boolean).length,6);assert.equal(Object.keys(state.answers).length,90);assert.deepEqual(e.errors,[]);e.close();
 });
 await test(`Set ${n}: blank grading, wrong filter and edits invalidate only current chapter`,async()=>{
  const e=await setup(n);click(e,'#quick-grade');assert.match(e.doc.querySelector('#quick-result').textContent,/0\/15/);assert.match(e.doc.querySelector('#quick-result').textContent,/ไม่ตอบ 15/);
  select(e,8);click(e,'#quick-grade');select(e,7);answer(e,0,e.w.quickData.questions[0].answer);
  let state=JSON.parse(e.w.localStorage.getItem(e.key));assert.equal(state.graded[7],false);assert.equal(state.graded[8],true);assert.equal(e.doc.querySelectorAll('.feedback').length,0);
  click(e,'#quick-grade');click(e,'#quick-wrong');assert.equal(e.doc.querySelectorAll('fieldset').length,14);click(e,'#quick-wrong');assert.equal(e.doc.querySelectorAll('fieldset').length,15);e.close();
 });
 await test(`Set ${n}: reset cancellation and confirmation preserve other chapters`,async()=>{
  const e=await setup(n);answer(e,0,0);select(e,8);answer(e,15,1);click(e,'#quick-grade');click(e,'#quick-reset');click(e,'#quick-cancel');
  assert.equal(JSON.parse(e.w.localStorage.getItem(e.key)).answers[15],1);
  click(e,'#quick-reset');click(e,'#quick-confirm-yes');const state=JSON.parse(e.w.localStorage.getItem(e.key));assert.equal(state.answers[0],0);assert.equal(state.answers[15],undefined);assert.equal(state.graded[8],undefined);e.close();
 });
 await test(`Set ${n}: restore chapter, answer and score`,async()=>{
  const e=await setup(n,{chapter:9,answers:{30:2},graded:{9:true}});assert.equal(e.doc.querySelector('#quick-chapter').value,'9');assert.ok(e.doc.querySelector('#quick-q30 input[value="2"]').checked);assert.equal(e.doc.querySelectorAll('.feedback').length,15);e.close();
 });
}
await test('Separate storage keys prevent set 1 and set 2 mixing',async()=>{
 const a=await setup(1),b=await setup(2);assert.notEqual(a.key,b.key);answer(a,0,1);assert.equal(b.w.localStorage.getItem(b.key),null);a.close();b.close();
});
await test('Malformed/null arrays, invalid options and invalid chapter handled safely',async()=>{
 for(const saved of ['{bad','[]',{chapter:99,answers:{'-1':0,0:9,1:'2',100:0},graded:{7:'true'}}]){
  const e=await setup(1,saved);assert.equal(e.doc.querySelectorAll('fieldset').length,15);assert.equal(e.doc.querySelectorAll('input:checked').length,0);assert.equal(e.doc.querySelectorAll('.feedback').length,0);assert.deepEqual(e.errors,[]);e.close();
 }
});
await test('Storage unavailable still allows answering and grading with warning',async()=>{
 const e=await setup(1,undefined,true);answer(e,0,e.w.quickData.questions[0].answer);click(e,'#quick-grade');assert.match(e.doc.querySelector('#quick-result').textContent,/1\/15/);assert.equal(e.doc.querySelector('#quick-warning').hidden,false);assert.deepEqual(e.errors,[]);e.close();
});
await test('JSON export has readable selected answer and graded explanation',async()=>{
 const e=await setup(2);let payload,download;
 e.w.Blob=class{constructor(parts){payload=JSON.parse(parts[0])}};e.w.URL.createObjectURL=()=> 'blob:test';e.w.URL.revokeObjectURL=()=>{};
 e.w.HTMLAnchorElement.prototype.click=function(){download=this.download};
 answer(e,0,e.w.quickData.questions[0].answer);click(e,'#quick-grade');click(e,'#quick-export');
 assert.equal(download,'quick-quiz-2-answers.json');assert.equal(payload.responses.length,90);assert.equal(payload.responses[0].correct,true);assert.ok(payload.responses[0].explanation);assert.equal(payload.responses[15].explanation,null);e.close();
});
await test('Independent arithmetic audit for numerical practice examples',async()=>{
 const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8);
 close(1-(1-.8)*19/17,.7764705882352941);close((2**2+(-2)**2+1)/3,3);
 close(Math.exp(-.5),.6065306597126334);close(2*.8*.6/(.8+.6),.6857142857142857);
 close(1-.75**2-.25**2,.375);close(.25*4+.75*4/4,1.75);
 close((3/4)**4,.31640625);close((2-5)/5,-.6);close(.9*.9+.3*.1,.84);
 assert.equal(3*2*4*5+1,121);assert.equal(12*3+1,37);assert.equal(10*60,600);
 assert.equal(1000+1.5*200,1300);assert.equal(20+.2*5,21);assert.equal(12+.25*4,13);
});
await writeFile(root+'results/qa-quick-tests.json',JSON.stringify({passed:checks.length,checks},null,2));
console.log(`${checks.length} Quick Quiz QA tests passed.`);
