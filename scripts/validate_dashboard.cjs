// Offline projection render checks. Does not create a replay or call providers.
const fs=require('fs'),vm=require('vm');
const source=fs.readFileSync('dist/app.js','utf8');
const ctx={console,URL,Date,URLSearchParams,window:{projectionSource:'Local validation'},location:{hash:'#diagnostics',search:'?local=1'}};
vm.createContext(ctx);
vm.runInContext(source.slice(0,source.indexOf("$('#week').onchange="))+source.slice(source.indexOf('let selectedRunId=')),ctx);
vm.runInContext('data='+fs.readFileSync('dist/data.json','utf8')+';week=data.runs.map(r=>r.week).sort().at(-1);',ctx);
for(const f of ['overview','tenderView','partnerView','outreachView','contentView','integrationsView','diagnosticsView']){
  if(!vm.runInContext(f+'()',ctx).length)throw Error(f);
  console.log(f+': rendered');
}
vm.runInContext("show=(title,html)=>{if(!html.length)throw Error(title);return html;};data.tenders.forEach(t=>openTender(t.id));",ctx);
console.log('All tender dialogs rendered');
vm.runInContext("week='2099-W01'",ctx);
if(!vm.runInContext('diagnosticsView()',ctx).includes('No execution record'))throw Error('Empty-week guard');
console.log('Future week: no fabricated execution');
