"""Local, provider-neutral scaffolding. No network calls or credentials.

All deployed workers must share this SQLite database on one durable host.
For multi-host workers, replace SQLite with a transactional shared database.
"""
import json
import sqlite3
from decimal import Decimal

LIMIT = 299_000  # thousandths of a Clay DATA credit

def units(value):
    amount = Decimal(str(value)) * 1000
    if not amount.is_finite() or amount < 0 or amount != amount.to_integral_value():
        raise ValueError('Use nonnegative DATA credits with at most 3 decimal places')
    return int(amount)

class Ledger:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=30)
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, halted INTEGER NOT NULL DEFAULT 0);
          CREATE TABLE IF NOT EXISTS jobs (
            run TEXT, key TEXT, reserved INTEGER NOT NULL, actual INTEGER,
            task_id TEXT, PRIMARY KEY(run,key));
        ''')

    def reserve(self, run, key, upper_bound, unit='DATA_CREDITS'):
        if not run or not key or upper_bound is None or unit != 'DATA_CREDITS':
            raise ValueError('COST_REVIEW_REQUIRED: run, stable job key and bounded DATA cost required')
        cost = units(upper_bound)
        try:
            self.db.execute('BEGIN IMMEDIATE')
            self.db.execute('INSERT OR IGNORE INTO runs(id) VALUES (?)', (run,))
            previous = self.db.execute('SELECT reserved,actual,task_id FROM jobs WHERE run=? AND key=?', (run,key)).fetchone()
            if previous:
                self.db.commit()
                return {'submit': False, 'reason': 'RESUME_EXISTING_JOB', 'task_id': previous[2]}
            halted = self.db.execute('SELECT halted FROM runs WHERE id=?',(run,)).fetchone()[0]
            used = self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM jobs WHERE run=?',(run,)).fetchone()[0]
            if halted or used + cost > LIMIT:
                self.db.commit()
                return {'submit':False,'reason':'ENRICHMENT_BUDGET_HOLD'}
            self.db.execute('INSERT INTO jobs(run,key,reserved) VALUES (?,?,?)',(run,key,cost))
            self.db.commit()
            return {'submit':True,'reserved_data_credits':cost/1000}
        except Exception:
            self.db.rollback()
            raise

    def bind_task(self, run, key, task_id):
        if not task_id:
            raise ValueError('Missing provider task ID')
        with self.db:
            row = self.db.execute('SELECT task_id FROM jobs WHERE run=? AND key=?',(run,key)).fetchone()
            if row is None or (row[0] and row[0] != task_id):
                raise ValueError('Unknown reservation or conflicting provider task')
            self.db.execute('UPDATE jobs SET task_id=? WHERE run=? AND key=?',(task_id,run,key))

    def reconcile(self, run, key, actual_data_credits):
        # Call ONLY for provider-confirmed final charge. Timeouts retain reservation.
        actual = units(actual_data_credits)
        try:
            self.db.execute('BEGIN IMMEDIATE')
            row = self.db.execute('SELECT reserved,actual FROM jobs WHERE run=? AND key=?',(run,key)).fetchone()
            if row is None:
                raise ValueError('Unknown reservation')
            if row[1] is not None and row[1] != actual:
                raise ValueError('Conflicting final billing result; manual reconciliation required')
            self.db.execute('UPDATE jobs SET actual=? WHERE run=? AND key=?',(actual,run,key))
            if actual > row[0]:
                self.db.execute('UPDATE runs SET halted=1 WHERE id=?',(run,))
            self.db.commit()
            return {'halted':actual > row[0]}
        except Exception:
            self.db.rollback()
            raise

    def status(self, run):
        spent,reserved = self.db.execute('SELECT COALESCE(SUM(actual),0),COALESCE(SUM(CASE WHEN actual IS NULL THEN reserved ELSE 0 END),0) FROM jobs WHERE run=?',(run,)).fetchone()
        row = self.db.execute('SELECT halted FROM runs WHERE id=?',(run,)).fetchone()
        return {'spent':spent/1000,'reserved':reserved/1000,'remaining':max(0,LIMIT-spent-reserved)/1000,'halted':bool(row and row[0])}

def dialogue_route(option):
    if option.get('eligibility') != 'PASS' or option.get('scope_evidence') != 'CONFIRMED':
        return 'QUALIFICATION_HOLD'
    if option.get('delivery_route') == 'SINGLE_E2E':
        return 'TENDER_DIALOGUE_DRAFT'
    if option.get('delivery_route') == 'CONSORTIUM' and option.get('counterpart_ids'):
        return 'PARTNERSHIP_DIALOGUE_DRAFT'
    return 'NO_PAIR_FOUND'

def channel_gate(contact, channel, connected=False):
    if not connected:
        return 'CONNECTION_REQUIRED'
    if contact.get('suppressed') or contact.get('reply_pending'):
        return 'CONTACT_HOLD'
    if contact.get('pause_sync_pending'):
        return 'FEEDBACK_SYNC_HOLD'
    if contact.get('active_channel') not in (None, channel):
        return 'OTHER_CHANNEL_ACTIVE'
    return 'DRAFT_ONLY'  # scaffold never grants permission to send

class MCPAdapter:
    """Bind discovered provider tools here AFTER account and draft tests.

    Names in connector-contracts.json are logical operations, NOT MCP tool names.
    Do not guess URLs, tool schemas, credential formats or native CRM support.
    """
    def __init__(self, provider):
        self.provider = provider

    def call(self, operation, payload):
        raise RuntimeError(f'{self.provider}: CONNECTION_REQUIRED; {operation} is not bound')

if __name__ == '__main__':
    print(json.dumps({'mode':'SCAFFOLD_ONLY','clay_data_credit_ceiling':299,
      'connectors':['mentic','surferseo','heyreach'],'live_actions_enabled':False}))
