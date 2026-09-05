import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from flow import Ledger, dialogue_route, channel_gate, MCPAdapter

class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name)/'ledger.sqlite')
        self.ledger = Ledger(self.path)
    def tearDown(self):
        self.ledger.db.close()
        self.tmp.cleanup()
    def test_boundary_and_resume(self):
        self.assertTrue(self.ledger.reserve('run1','person:email',299)['submit'])
        self.assertFalse(self.ledger.reserve('run1','another',0.001)['submit'])
        self.ledger.bind_task('run1','person:email','provider-task')
        self.assertFalse(self.ledger.reserve('run1','person:email',299)['submit'])
        reopened=Ledger(self.path)
        self.assertEqual(reopened.status('run1')['reserved'],299)
        reopened.db.close()
    def test_reconcile_and_overrun(self):
        self.ledger.reserve('r','a',100)
        self.ledger.reconcile('r','a',80)
        self.assertTrue(self.ledger.reserve('r','b',219)['submit'])
        self.assertTrue(self.ledger.reconcile('r','b',220)['halted'])
        self.assertFalse(self.ledger.reserve('r','c',0)['submit'])
    def test_unknown_cost(self):
        for cost,unit in [(None,'DATA_CREDITS'),(1,'ACTIONS'),(-1,'DATA_CREDITS')]:
            with self.assertRaises(ValueError): self.ledger.reserve('r','x',cost,unit)
    def test_concurrent_reservations(self):
        def reserve(key):
            x=Ledger(self.path)
            try: return x.reserve('shared',key,200)['submit']
            finally: x.db.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(reserve,['a','b'])),1)
    def test_e2e_does_not_require_pair(self):
        base={'eligibility':'PASS','scope_evidence':'CONFIRMED'}
        self.assertEqual(dialogue_route(dict(base,delivery_route='SINGLE_E2E')),'TENDER_DIALOGUE_DRAFT')
        self.assertEqual(dialogue_route(dict(base,delivery_route='CONSORTIUM')),'NO_PAIR_FOUND')
    def test_cross_channel_and_unbound(self):
        self.assertEqual(channel_gate({'active_channel':'woodpecker'},'heyreach',True),'OTHER_CHANNEL_ACTIVE')
        self.assertEqual(channel_gate({'suppressed':True},'heyreach',True),'CONTACT_HOLD')
        self.assertEqual(channel_gate({'reply_pending':True},'heyreach',True),'CONTACT_HOLD')
        self.assertEqual(channel_gate({'pause_sync_pending':True},'heyreach',True),'FEEDBACK_SYNC_HOLD')
        with self.assertRaises(RuntimeError): MCPAdapter('mentic').call('launch',{})

if __name__=='__main__': unittest.main()
