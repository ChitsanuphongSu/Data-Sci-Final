// Build-time highlighting: no CDN or runtime highlighter needed on the website.
import {createHighlighter} from 'shiki';
import {readFile,writeFile,readdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const highlighter=await createHighlighter({themes:['one-dark-pro'],langs:['python','powershell']});
const decode=s=>s.replace(/&(#\d+|#x[\da-f]+|amp|lt|gt|quot|apos);/gi,(_,e)=>{
 if(e[0]==='#')return String.fromCodePoint(e[1].toLowerCase()==='x'?parseInt(e.slice(2),16):parseInt(e.slice(1),10));
 return {amp:'&',lt:'<',gt:'>',quot:'"',apos:"'"}[e];
});
let count=0;
for(const file of await readdir(root)){
 if(!file.endsWith('.html'))continue;
 const path=root+file,source=await readFile(path,'utf8');
 const highlighted=source.replace(/<pre data-lang="(python|powershell)"[^>]*><code>([\s\S]*?)<\/code><\/pre>/g,(_,lang,encoded)=>{
  count++;
  return highlighter.codeToHtml(decode(encoded),{lang,theme:'one-dark-pro'})
    .replace('<pre ','<pre data-lang="'+lang+'" aria-label="โค้ด '+lang+' เลื่อนอ่านได้" ');
 });
 if(highlighted!==source)await writeFile(path,highlighted);
}
highlighter.dispose();
console.log(`Highlighted ${count} code blocks with Shiki / one-dark-pro.`);
