import copy
import json
import unittest
from budget import estimate

class BudgetTests(unittest.TestCase):
    def setUp(self):
        with open('scenario.json') as f: self.config=json.load(f)
    def test_sample_total(self):
        result=estimate(self.config)
        self.assertEqual(result['subtotal'],'54.50')
        self.assertEqual(result['projected_total'],'62.68')
        self.assertFalse(result['over_budget'])
    def test_over_budget(self):
        self.config['monthly_budget']='50';self.assertTrue(estimate(self.config)['over_budget'])
    def test_exact_budget(self):
        self.config['headroom_percent']=0;self.config['monthly_budget']='54.50'
        self.assertFalse(estimate(self.config)['over_budget'])
    def test_negative_quantity(self):
        self.config['services'][0]['quantity']=-1
        with self.assertRaises(ValueError): estimate(self.config)
    def test_nan_rejected(self):
        self.config['monthly_budget']='NaN'
        with self.assertRaises(ValueError): estimate(self.config)
    def test_unknown_unit(self):
        self.config['services'][0]['unit']='second'
        with self.assertRaises(ValueError): estimate(self.config)
    def test_duplicate_service(self):
        self.config['services'].append(copy.deepcopy(self.config['services'][0]))
        with self.assertRaises(ValueError): estimate(self.config)
    def test_rounding_only_at_reporting_boundary(self):
        self.config.update(headroom_percent=0,services=[{'name':'a','quantity':3,'unit_price':'0.005','unit':'month'}])
        self.assertEqual(estimate(self.config)['subtotal'],'0.02')

if __name__=='__main__': unittest.main()
