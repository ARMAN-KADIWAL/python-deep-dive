"""Regression tests for the five lab tasks and comprehensive cleaning."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from pandas_lab import (
    EDUCATION_MAP, convert_sales_types, comprehensive_data_cleaning,
    employee_dataset, fill_student_missing, handle_categorical_data,
    min_max_normalize, parse_boolean, product_dataset, robust_scale,
    run_all, sales_dataset, student_dataset, survey_dataset, z_score_standardize,
)


class Lab61Tests(unittest.TestCase):
    def test_students_shape(self):
        self.assertEqual(student_dataset().shape, (10, 6))

    def test_missing_before(self):
        self.assertEqual(int(student_dataset().isna().sum().sum()), 10)

    def test_fill_all_missing(self):
        self.assertFalse(fill_student_missing(student_dataset()).isna().any().any())

    def test_fill_preserves_original(self):
        df = student_dataset()
        fill_student_missing(df)
        self.assertTrue(pd.isna(df.loc[2, 'name']))

    def test_fill_median_age(self):
        self.assertEqual(fill_student_missing(student_dataset()).loc[3, 'age'], 21.5)

    def test_dropna_variants(self):
        df = student_dataset()
        self.assertLess(len(df.dropna()), len(df))
        self.assertEqual(len(df.dropna(how='all')), len(df))
        self.assertIn('student_id', df.dropna(axis=1))

    def test_duplicate_rows(self):
        self.assertEqual(int(product_dataset().duplicated().sum()), 3)

    def test_duplicate_id(self):
        self.assertEqual(int(product_dataset().duplicated('product_id').sum()), 3)

    def test_drop_duplicate_ids(self):
        self.assertEqual(len(product_dataset().drop_duplicates('product_id')), 7)

    def test_converted_types(self):
        df = convert_sales_types(sales_dataset())
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['order_date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['amount']))
        self.assertTrue(pd.api.types.is_integer_dtype(df['order_id']))

    def test_boolean_false_is_false(self):
        self.assertEqual(parse_boolean(pd.Series(['False', 'True'])).tolist(), [False, True])

    def test_boolean_rejects_invalid(self):
        with self.assertRaises(ValueError):
            parse_boolean(pd.Series(['maybe']))

    def test_invalid_numeric_coerces_to_nan(self):
        self.assertTrue(pd.isna(pd.to_numeric(pd.Series(['invalid']), errors='coerce').iloc[0]))

    def test_min_max_range(self):
        scaled = min_max_normalize(employee_dataset()['salary'])
        self.assertAlmostEqual(scaled.min(), 0)
        self.assertAlmostEqual(scaled.max(), 1)

    def test_standardization(self):
        scaled = z_score_standardize(employee_dataset()['salary'])
        self.assertAlmostEqual(scaled.mean(), 0)
        self.assertAlmostEqual(scaled.std(), 1)

    def test_robust_median(self):
        self.assertAlmostEqual(robust_scale(employee_dataset()['salary']).median(), 0)

    def test_constant_scaling_safe(self):
        for f in (min_max_normalize, z_score_standardize, robust_scale):
            self.assertEqual(f(pd.Series([5., 5., 5.])).tolist(), [0, 0, 0])

    def test_ordinal_mapping(self):
        result = handle_categorical_data(survey_dataset(), {'education_level': EDUCATION_MAP})
        self.assertEqual(result.loc[0, 'education_level_encoded'], 0)
        self.assertEqual(result.loc[3, 'education_level_encoded'], 3)

    def test_nominal_one_hot(self):
        result = handle_categorical_data(survey_dataset(), nominal_cols=['department'])
        self.assertIn('department_IT', result)
        self.assertEqual(result.loc[0, 'department_IT'], 1)
        self.assertEqual(result.loc[1, 'department_IT'], 0)

    def test_frequency_encoding(self):
        result = handle_categorical_data(survey_dataset(), high_card_cols=['department'])
        self.assertEqual(result.loc[0, 'department_frequency'], 5)

    def test_pipeline_dedup_and_nullable_bool(self):
        df = pd.DataFrame({'name': ['a', 'a', 'b'], 'active': ['False', 'False', 'True']})
        result = comprehensive_data_cleaning(df, {'duplicates': {'method': 'all'},
                                                  'data_types': {'active': 'boolean'}})
        self.assertEqual(len(result), 2)
        self.assertEqual(result['active'].tolist(), [False, True])

    def test_pipeline_values_and_scaling(self):
        df = pd.DataFrame({'age': [10., None, 30.], 'name': ['a', None, 'b']})
        result = comprehensive_data_cleaning(df, {'missing_values': {'age': 'median',
                                                                      'name': 'value:Unknown'},
                                                  'normalization': {'age': 'min_max'}})
        self.assertEqual(result['name'].tolist(), ['a', 'Unknown', 'b'])
        self.assertEqual(result['age_normalized'].tolist(), [0, .5, 1])

    def test_pipeline_coerce_invalid(self):
        df = pd.DataFrame({'value': ['1', 'bad']})
        result = comprehensive_data_cleaning(df, {'data_types': {'value': 'numeric'}})
        self.assertTrue(pd.isna(result.loc[1, 'value']))

    def test_pipeline_invalid_config(self):
        with self.assertRaises(ValueError):
            comprehensive_data_cleaning(pd.DataFrame({'x': [1]}),
                                        {'normalization': {'x': 'unknown'}})

    def test_all_tasks_and_csv_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_all(tmp)
            csvs = list(Path(tmp).glob('*.csv'))
            self.assertEqual(len(csvs), 11)
            self.assertEqual(pd.read_csv(Path(tmp) / 'students_cleaned.csv').shape, (10, 6))
            self.assertTrue((Path(tmp) / 'complete_pipeline.csv').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)