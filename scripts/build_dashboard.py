"""Build a read-only projection of the repository SSOT; no external services."""
from pathlib import Path
import json,hashlib,datetime

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def build(run_override=None):
    tenders=[read(p) for p in sorted((ROOT/'tenders').glob('*/tender.json'))]
    companies=[read(p) for p in sorted((ROOT/'partners').glob('*/company.json'))]
    contacts=[read(p) for p in sorted((ROOT/'partners').glob('*/contacts/*.json'))]
    packets=[read(p) for p in sorted((ROOT/'tenders').glob('*/actors/*/outreach.json'))]
    pairs={}
    for p in sorted((ROOT/'tenders').glob('*/delivery-options/*.json')):
        row=read(p);pairs[row['id']]=row
    runs=[read(p) for p in sorted((ROOT/'executions').glob('*/*.json'))]
    if run_override is not None:
        runs=[run_override if r['id']==run_override['id'] else r for r in runs]
    files=sorted([*(ROOT/'tenders').rglob('*.json'),*(ROOT/'partners').rglob('*.json')])
    digest=hashlib.sha256(b''.join(p.read_bytes() for p in files)).hexdigest()
    obj={'project':'gtmtechweek','data_as_of':'2026-09-04','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dataset_digest':digest,'config':read(ROOT/'config/demo.json'),'tenders':tenders,'partners':companies,'contacts':contacts,'pairs':list(pairs.values()),'outreach':packets,'runs':runs,'content':[{'id':'utility-integration-before-the-bid','title':'Connected utility projects succeed at the interfaces','state':'DRAFT_ONLY','body':(ROOT/'content/blog/utility-integration-before-the-bid.md').read_text()}]}
    obj['readiness']=read(ROOT/'config/readiness.json')
    (ROOT/'dist').mkdir(exist_ok=True)
    temporary=ROOT/'dist/data.json.tmp'
    temporary.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(ROOT/'dist/data.json')
    return obj
if __name__=='__main__':
    obj=build();print(f"Projection: {len(obj['tenders'])} tenders; {len(obj['contacts'])} actors; {len(obj['outreach'])} actor/tender packets; {len(obj['runs'])} observed runs")
