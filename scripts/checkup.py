"""Offline PoC acceptance checks. No external, paid or distribution calls."""
import datetime,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
checks=[]
def command(name,args,cwd=ROOT):
    result=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    checks.append({'name':name,'passed':result.returncode==0,'exit_code':result.returncode,'output':(result.stdout+result.stderr).strip()})
    if result.returncode:raise RuntimeError(name+' failed')
def main():
    command('Public data and four-followup validation',[sys.executable,'scripts/validate.py'])
    command('Six budget, concurrency, resume and channel guard tests',[sys.executable,'-m','unittest','discover','-s','integrations','-p','test_*.py'])
    command('Dashboard JavaScript syntax',['node','--check','dist/app.js'])
    command('Actual local replay and projection',[sys.executable,'scripts/record_execution.py'])
    js="""
const fs=require('fs'),vm=require('vm');const s=fs.readFileSync('dist/app.js','utf8');
const ctx={console,URL,Date,URLSearchParams,window:{projectionSource:'Local preview data'},location:{hash:'#diagnostics',search:'?local=1'}};
vm.createContext(ctx);vm.runInContext(s.slice(0,s.indexOf("$('#week').onchange="))+s.slice(s.indexOf('let selectedRunId=')),ctx);
vm.runInContext('data='+fs.readFileSync('dist/data.json','utf8')+';week=data.runs[0].week;',ctx);
for(const f of ['overview','tenderView','partnerView','outreachView','contentView','integrationsView','diagnosticsView']){
 if(!vm.runInContext(f+'()',ctx).length)throw Error(f);console.log(f+': rendered');}
vm.runInContext("week='2099-W01'",ctx);if(!vm.runInContext('diagnosticsView()',ctx).includes('No execution record'))throw Error('Missing empty-week message');
console.log('Empty week: no fabricated run');
"""
    command('All seven views and empty-week diagnostics',['node','-e',js])
    with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
        isolated=pathlib.Path(directory)/'project'
        shutil.copytree(ROOT,isolated,ignore=shutil.ignore_patterns('.git','__pycache__','source.tar.gz','qa','*.zip'))
        (isolated/'config/readiness.json').write_text('invalid-json')
        result=subprocess.run([sys.executable,'scripts/record_execution.py'],cwd=isolated,capture_output=True,text=True)
        latest=max((json.loads(p.read_text()) for p in (isolated/'executions').glob('*/*.json')),key=lambda r:r['started_at'])
        passed=result.returncode==1 and latest['status']=='FAILED'
        checks.append({'name':'Injected projection failure retains FAILED run and nonzero exit','passed':passed,'exit_code':result.returncode,'output':'Isolated test; not inserted into business run history.'})
        if not passed:raise RuntimeError('Failure reporting test failed')
    required=['AGENTS.md','HANDOVER.md','JUDGES.md','PUBLISH.md','.github/workflows/weekly-demo.yml','dist/judges.html','integrations/connector-contracts.json']
    assert all((ROOT/p).is_file() for p in required)
    checks.append({'name':'Handover, judge guide and workflow files present','passed':True})
if __name__=='__main__':
    error=None
    try:main()
    except Exception as exc:error=str(exc)[:1500]
    report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'OFFLINE_POC_ACCEPTANCE','passed':error is None and all(x['passed'] for x in checks),'provider_calls':0,'clay_data_credits':0,'checks':checks,'error':error,'not_verified':['GitHub publication / remote Actions','Scheduled fresh research completion','Live MCP adapter round trips','Deliverability or distribution','Browser interactions / mobile layout','Tender eligibility and partner willingness']}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/checks.json').write_text(json.dumps(report,indent=2)+'\n')
    text='# PoC checkup report\n\nChecked: '+report['checked_at']+'\n\nResult: **'+('PASS' if report['passed'] else 'FAIL')+' for offline PoC checks**. This is not end-to-end production certification.\n\n'
    text+='\n'.join('- '+('PASS' if c['passed'] else 'FAIL')+': '+c['name'] for c in checks)
    text+='\n\nNo provider calls, paid enrichment or distribution occurred. Six guard tests are included within the check groups. Raw output: `qa/checks.json`. Reproduce: `python scripts/checkup.py`.\n\nNot verified:\n\n'+'\n'.join('- '+x for x in report['not_verified'])+'\n'
    if error:text+='\nError: '+error+'\n'
    (ROOT/'QA_REPORT.md').write_text(text)
    print(json.dumps({'passed':report['passed'],'check_groups':len(checks),'error':error}))
    sys.exit(0 if report['passed'] else 1)
