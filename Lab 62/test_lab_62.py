"""Regression tests for all Lab 62 Pandas exercises."""
from __future__ import annotations

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from lab_62 import run_lab


class Lab62Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.data = run_lab()

    def test_inner_join_has_all_six_orders(self):
        self.assertEqual(len(self.data['inner_merged']), 6)
        self.assertSetEqual(set(self.data['inner_merged'].order_id), set(range(1001, 1007)))

    def test_left_join_keeps_all_customers(self):
        left = self.data['left_merged']
        self.assertEqual(len(left), 7)
        self.assertTrue(left.loc[left.customer_id.eq(105), 'order_id'].isna().all())

    def test_right_join_keeps_all_orders(self):
        self.assertEqual(len(self.data['right_merged']), 6)
        self.assertTrue(self.data['right_merged']['customer_name'].notna().all())

    def test_outer_join_keeps_unmatched_customer(self):
        outer = self.data['outer_merged']
        self.assertEqual(len(outer), 7)
        self.assertIn(105, outer.customer_id.to_numpy())

    def test_join_columns_do_not_use_handout_placeholders(self):
        self.assertIn('customer_id', self.data['inner_merged'].columns)
        self.assertNotIn('col1', self.data['inner_merged'].columns)

    def test_vertical_concatenation_has_nine_months(self):
        joined = self.data['yearly_sales']
        self.assertEqual(joined.shape, (9, 3))
        self.assertEqual(joined.month.tolist(), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep'])

    def test_horizontal_concatenation_removes_duplicate_month_column(self):
        joined = self.data['financial_data_clean']
        self.assertEqual(joined.columns.tolist(), ['month','revenue','expenses'])
        self.assertEqual(joined.shape, (3, 3))

    def test_concatenation_with_keys_has_two_index_levels(self):
        self.assertEqual(self.data['sales_with_keys'].index.nlevels, 2)
        self.assertEqual(set(self.data['sales_with_keys'].index.get_level_values(0)), {'Quarter1','Quarter2','Quarter3'})

    def test_grouping_sums_by_person(self):
        totals = self.data['sales_by_person']
        self.assertEqual(int(totals['John']), 5700)
        self.assertEqual(int(totals['Sarah']), 2500)
        self.assertEqual(int(totals['Mike']), 6100)

    def test_grouping_total_preserved(self):
        self.assertEqual(int(self.data['sales_summary']['sum'].sum()), int(self.data['sales_data'].sales_amount.sum()))

    def test_grouping_multiple_levels(self):
        self.assertEqual(self.data['region_product_sales'].index.nlevels, 2)

    def test_custom_aggregation_present(self):
        self.assertIn('performance', self.data['custom_agg'].columns)
        self.assertEqual(self.data['custom_agg'].loc['John', 'performance'], 'High')

    def test_basic_pivot_reconciles_total(self):
        pivot = self.data['basic_pivot_filled']
        self.assertAlmostEqual(float(pivot.to_numpy().sum()), float(self.data['sales_data'].sales_amount.sum()))

    def test_multiple_value_pivot(self):
        pivot = self.data['multi_value_pivot']
        self.assertIn('sales_amount', pivot.columns.get_level_values(0))
        self.assertIn('units_sold', pivot.columns.get_level_values(0))

    def test_multiple_aggregates_pivot(self):
        pivot = self.data['multi_agg_pivot']
        self.assertSetEqual(set(pivot.columns.get_level_values(0)), {'sum','mean','count'})

    def test_pivot_margins_grand_total(self):
        pivot = self.data['pivot_with_totals']
        self.assertEqual(pivot.loc['Total', 'Total'], self.data['sales_data'].sales_amount.sum())

    def test_monthly_pivot_rows_are_hierarchical(self):
        self.assertEqual(self.data['monthly_pivot'].index.nlevels, 2)

    def test_multiindex_has_named_levels(self):
        self.assertEqual(self.data['sales_multi'].index.names, ['Store','Department'])

    def test_multiindex_total_electronics(self):
        self.assertEqual(self.data['sales_multi'].loc[('Store A', 'Electronics'), 'Total_Sales'], 66000)

    def test_multiindex_xs_selects_store_a(self):
        self.assertEqual(self.data['store_a'].shape[0], 3)
        self.assertIn('Books', self.data['store_a'].index)

    def test_multiindex_store_totals(self):
        self.assertEqual(self.data['store_totals'].loc['Store A', 'Total_Sales'], 122500)

    def test_multiindex_stack_unstack(self):
        self.assertEqual(self.data['stacked'].index.nlevels, 3)
        self.assertEqual(self.data['unstacked'].columns.nlevels, 2)

    def test_multiindex_pivot_with_regions(self):
        self.assertEqual(self.data['pivot_multi'].index.nlevels, 2)
        self.assertIn('North', self.data['pivot_multi'].index.get_level_values('region'))

    def test_retail_exercise_contains_100_transactions(self):
        self.assertEqual(self.data['retail_data'].shape[0], 100)
        self.assertEqual(self.data['complete_data'].shape[0], 100)

    def test_retail_demo_has_no_missing_demographics(self):
        complete = self.data['complete_data']
        self.assertTrue(complete[['age_group','gender','membership_level']].notna().all().all())

    def test_retail_dataset_is_reproducible(self):
        with contextlib.redirect_stdout(io.StringIO()):
            again = run_lab()
        assert_frame_equal(self.data['complete_data'], again['complete_data'])

    def test_retail_total_matches_grouped_totals(self):
        expected = round(self.data['complete_data'].sales_amount.sum(), 2)
        actual = round(self.data['summary_analysis'][('sales_amount','sum')].sum(), 2)
        self.assertAlmostEqual(expected, actual, places=2)

    def test_retail_pivot_has_grand_total(self):
        pivot = self.data['comprehensive_pivot']
        self.assertIn('All', pivot.index.get_level_values(0))

    def test_months_in_calendar_order(self):
        self.assertEqual(self.data['monthly_trends'].index.tolist(), ['Jan','Feb','Mar','Apr','May','Jun'])

    def test_monthly_totals_match_retail_totals(self):
        self.assertAlmostEqual(self.data['monthly_trends'].to_numpy().sum(), self.data['complete_data'].sales_amount.sum(), places=2)

    def test_customer_segment_counts_sum_to_100(self):
        self.assertEqual(int(self.data['customer_analysis'].Transaction_Count.sum()), 100)

    def test_exports_all_nine_csv_files(self):
        with tempfile.TemporaryDirectory() as td:
            with contextlib.redirect_stdout(io.StringIO()):
                run_lab(output_dir=td)
            files = list(Path(td).glob('*.csv'))
            self.assertEqual(len(files), 9)
            self.assertEqual(len(pd.read_csv(Path(td) / 'complete_data.csv')), 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
