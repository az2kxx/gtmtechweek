"""Validate identities, draft coverage and the public publication boundary."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate():
    contacts={json.loads(p.read_text())['id'] for p in (ROOT/'partners').glob('*/contacts/*.json')}
    companies={json.loads(p.read_text())['id'] for p in (ROOT/'partners').glob('*/company.json')}
    tenders=list((ROOT/'tenders').glob('*/tender.json'))
    assert tenders,'No tenders'
    n=0
    for path in tenders:
        t=json.loads(path.read_text());assert path.parent.name==t['id']
        assert set(t['actor_ids'])<=contacts
        for cid in t['actor_ids']:
            p=json.loads((path.parent/'actors'/cid/'outreach.json').read_text())
            assert p['actor_id']==cid and p['tender_id']==t['id']
            assert p['send_authorized'] is False
            assert len(p['email']['followups'])==len(p['linkedin']['followups'])==4
            assert p['email']['initial'] and p['linkedin']['initial'];n+=1
    for p in (ROOT/'partners').glob('*/contacts/*.json'):
        assert json.loads(p.read_text())['company_id'] in companies
    for folder in ['tenders','partners','content','executions','dist']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and p.suffix in ['.json','.md','.html']:
                text=p.read_text()
                assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text),f'Direct email in public data: {p}'
                assert not re.search(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b',text),f'Private UUID in {p}'
    return {'tenders':len(tenders),'partners':len(companies),'actors':len(contacts),'actor_tender_packets':n,'email_drafts':n*5,'linkedin_sequences':n}
if __name__=='__main__':print(json.dumps(validate()))
