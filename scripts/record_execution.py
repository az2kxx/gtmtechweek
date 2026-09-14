"""Record an actual local validation/rebuild run, never fabricate provider activity."""
import datetime,json,os,sys,subprocess
from pathlib import Path
from validate import validate
from build_dashboard import build
ROOT=Path(__file__).resolve().parents[1]
now=datetime.datetime.now(datetime.timezone.utc)
iso=now.isocalendar();week=f'{iso.year}-W{iso.week:02d}'
attempt=os.environ.get('GITHUB_RUN_ATTEMPT','1')
run_id=(os.environ['GITHUB_RUN_ID']+'-attempt-'+attempt) if os.environ.get('GITHUB_RUN_ID') else now.strftime('local-%Y%m%dT%H%M%S%fZ')
evidence_dates=[json.loads(p.read_text()).get('evidence_date') for p in (ROOT/'tenders').glob('*/tender.json')]
dataset_as_of=max((d for d in evidence_dates if d),default=None)
run={'id':run_id,'week':week,'started_at':now.isoformat(),'kind':'REPOSITORY_POC_REPLAY','trigger':'github_actions' if os.environ.get('GITHUB_ACTIONS') else 'local','status':'RUNNING','dataset_as_of':dataset_as_of,'evidence_dates_mixed':True,'clay_data_credits':0,'clay_basis':'No Clay calls in this local replay','distribution_calls':0,'stages':[]}
run['source_revision']=os.environ.get('GITHUB_SHA')
run['actions_url']=('https://github.com/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID']) if os.environ.get('GITHUB_RUN_ID') else None
run['attempt']=attempt
target=ROOT/'executions'/week/f'{run_id}.json';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(run,indent=2)+'\n')
try:
    run['stages'].append({'name':'Public data validation','state':'RUNNING','detail':'Checking identity links, privacy boundary and draft completeness'})
    counts=validate();run['counts']=counts
    subprocess.run(['node','--check','dist/app.js'],cwd=ROOT,check=True,capture_output=True,text=True)
    run['stages']=[{'name':'Tender inputs','state':'CACHED','detail':f"{counts['tenders']} research snapshots; no new scraping in this run"},{'name':'Partner mapping','state':'VALIDATED','detail':f"{counts['partners']} companies / {counts['actors']} actors; existing hypotheses"},{'name':'Enrichment','state':'SKIPPED','detail':'Cached professional profiles; no billable requests'},{'name':'Outreach drafts','state':'VALIDATED','detail':f"{counts['actor_tender_packets']} actor/tender packets; email and LinkedIn plus four followups"},{'name':'Blog content','state':'DRAFT_ONLY','detail':'Technology/use-case editorial draft, not published'},{'name':'Attio mirror','state':'PRESERVED','detail':'Integration retained; no CRM write in replay'},{'name':'Distribution','state':'DISABLED','detail':'PoC only; HeyReach trial expired'},{'name':'Repository projection','state':'COMPLETED','detail':'Generated dashboard data from canonical dossiers'}]
    run['status']='COMPLETED';run['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    build(run_override=run)  # Publish projection before committing canonical success.
except Exception as e:
    run['stages'].append({'name':'Validation / build','state':'FAILED','detail':'Input or JavaScript validation failed; inspect Actions logs','error':str(e)[:1500]})
    run['status']='FAILED';run['error']=str(e)[:1500];run['completed_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
target.write_text(json.dumps(run,indent=2)+'\n')
if run['status']=='FAILED':
    try:build(run_override=run)
    except Exception as projection_error:
        print('Failure record retained; projection unavailable:',str(projection_error)[:500],file=sys.stderr)
print(json.dumps({'run_id':run_id,'week':week,'status':run['status']}))
if run['status']=='FAILED':sys.exit(1)
