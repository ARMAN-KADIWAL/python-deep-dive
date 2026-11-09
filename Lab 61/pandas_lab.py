"""Lab 61: Data Cleaning with Pandas — Handling Missing Data.

Run: python pandas_lab.py [--output-dir output]
Each task reproduces the supplied lab's datasets and demonstrates its operations.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def student_dataset():
    return pd.DataFrame({
        'student_id': list(range(1, 11)),
        'name': ['Alice Johnson', 'Bob Smith', None, 'Diana Prince', 'Eve Adams',
                 'Frank Miller', None, 'Grace Lee', 'Henry Ford', 'Ivy Chen'],
        'age': [20, 22, 21, None, 23, 19, 24, None, 20, 22],
        'grade': [85.5, 92., None, 88.5, None, 76., 94.5, 89., None, 91.5],
        'major': ['Computer Science', 'Mathematics', 'Physics', None, 'Chemistry',
                  'Computer Science', 'Biology', None, 'Mathematics', 'Physics'],
        'gpa': [3.4, 3.8, 3.2, 3.6, None, 2.9, 3.9, 3.5, 3.1, 3.7],
    })


def fill_student_missing(df):
    result = df.copy()
    result['name'] = result['name'].fillna('Unknown Student')
    result['age'] = result['age'].fillna(result['age'].median())
    result['grade'] = result['grade'].fillna(result['grade'].mean())
    result['major'] = result['major'].fillna(result['major'].mode().iloc[0])
    result['gpa'] = result['gpa'].ffill().bfill()
    return result


def task_1_missing_values(output):
    print('\nTASK 1 — Missing values, fillna and dropna')
    df = student_dataset()
    missing = pd.DataFrame({'count': df.isna().sum(), 'percent': df.isna().mean() * 100})
    print('Missing values by column:\n', missing)
    print('Missing pattern:\n', df.isna())
    df.info()
    filled = fill_student_missing(df)
    print('Filled missing count:', filled.isna().sum().sum())
    print('Drop any:', df.dropna().shape,
          'drop all:', df.dropna(how='all').shape,
          'drop name or age:', df.dropna(subset=['name', 'age']).shape,
          'drop incomplete columns:', df.dropna(axis=1).shape)
    df.to_csv(output / 'students_original.csv', index=False)
    filled.to_csv(output / 'students_cleaned.csv', index=False)
    return {'original': df, 'filled': filled, 'missing': missing}


def product_dataset():
    return pd.DataFrame({
        'product_id': [101, 102, 103, 104, 102, 105, 103, 106, 107, 104],
        'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Mouse',
                         'Headphones', 'Keyboard', 'Webcam', 'Speaker', 'Monitor'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics',
                     'Accessories', 'Accessories', 'Accessories', 'Electronics',
                     'Electronics', 'Electronics'],
        'price': [999.99, 25.50, 75., 299.99, 25.50, 89.99, 75., 45.99, 129.99, 299.99],
        'stock': [50, 200, 150, 75, 200, 100, 150, 80, 60, 75],
    })


def task_2_duplicates(output):
    print('\nTASK 2 — Duplicate identification and removal')
    df = product_dataset()
    print('Full duplicates:', df.duplicated().sum())
    print('Duplicate IDs:', df.duplicated(subset=['product_id']).sum())
    print('All duplicate-ID rows:\n', df[df.duplicated('product_id', keep=False)])
    print('Keep first:\n', df.duplicated('product_id', keep='first'))
    print('Keep last:\n', df.duplicated('product_id', keep='last'))
    unique = df.drop_duplicates(subset=['product_id'], keep='first')
    print('Unique complete rows:', len(df.drop_duplicates()),
          'unique IDs:', len(unique),
          'unique name/category:', len(df.drop_duplicates(['product_name', 'category'], keep='last')))
    df.to_csv(output / 'products_original.csv', index=False)
    unique.to_csv(output / 'products_deduplicated.csv', index=False)
    return {'original': df, 'unique': unique}


def sales_dataset():
    return pd.DataFrame({
        'order_id': ['1001', '1002', '1003', '1004', '1005', '1006'],
        'customer_id': [501, 502, 503, 504, 505, 506],
        'order_date': ['2023-01-15', '2023-01-16', '2023-01-17', '2023-01-18', '2023-01-19', '2023-01-20'],
        'amount': ['150.50', '275.00', '89.99', '450.25', '125.75', '320.00'],
        'quantity': ['2', '1', '3', '1', '4', '2'],
        'discount_percent': ['10.5', '15.0', '5.5', '20.0', '8.5', '12.0'],
        'is_premium': ['True', 'False', 'True', 'False', 'True', 'False'],
        'rating': ['4.5', '3.8', '4.9', '4.2', '3.5', '4.7'],
    })


def parse_boolean(series):
    """Unlike astype(bool), correctly handles the string 'False' as False."""
    lookup = {'true': True, 'false': False, '1': True, '0': False,
              'yes': True, 'no': False}
    normalized = series.astype('string').str.strip().str.lower()
    unknown = normalized.notna() & ~normalized.isin(lookup)
    if unknown.any():
        raise ValueError('Unrecognized boolean values: ' + repr(normalized[unknown].unique().tolist()))
    return normalized.map(lookup).astype('boolean')


def convert_sales_types(df):
    result = df.copy()
    for column in ['order_id', 'amount', 'quantity', 'discount_percent', 'rating']:
        result[column] = pd.to_numeric(result[column], errors='raise')
    result['is_premium'] = parse_boolean(result['is_premium'])
    result['order_date'] = pd.to_datetime(result['order_date'], errors='raise')
    return result


def task_3_conversions(output):
    print('\nTASK 3 — Type conversions and invalid input')
    df = sales_dataset()
    cleaned = convert_sales_types(df)
    print('Before:\n', df.dtypes, '\nAfter:\n', cleaned.dtypes)
    problematic = pd.DataFrame({'id': ['1', '2', '3', '4', '5'],
                                'value': ['100', '200.5', 'invalid', '300', 'N/A'],
                                'score': ['85', '92', '78', 'missing', '88']})
    problematic['value_numeric'] = pd.to_numeric(problematic['value'], errors='coerce')
    problematic['score_numeric'] = pd.to_numeric(problematic['score'], errors='coerce')
    # Retain original values as the safe equivalent of deprecated errors='ignore'.
    problematic['value_original'] = problematic['value']
    print('Problematic conversions:\n', problematic)
    cleaned.to_csv(output / 'sales_converted.csv', index=False)
    problematic.to_csv(output / 'conversion_errors.csv', index=False)
    return {'original': df, 'converted': cleaned, 'problematic': problematic}


def employee_dataset():
    return pd.DataFrame({
        'employee_id': range(1, 11),
        'salary': [45000, 65000, 55000, 85000, 72000, 48000, 95000, 58000, 67000, 78000],
        'age': [25, 35, 28, 42, 38, 26, 45, 30, 33, 40],
        'years_experience': [2, 8, 4, 15, 12, 3, 18, 6, 9, 14],
        'performance_score': [7.5, 8.9, 6.8, 9.2, 8.1, 7.0, 9.5, 7.8, 8.3, 8.7],
        'projects_completed': [5, 15, 8, 25, 20, 6, 30, 10, 16, 22],
    })


def min_max_normalize(series):
    span = series.max() - series.min()
    return (series - series.min()) / span if pd.notna(span) and span != 0 else series * 0.0


def z_score_standardize(series):
    std = series.std(ddof=1)
    return (series - series.mean()) / std if pd.notna(std) and std != 0 else series * 0.0


def robust_scale(series):
    iqr = series.quantile(.75) - series.quantile(.25)
    return (series - series.median()) / iqr if pd.notna(iqr) and iqr != 0 else series * 0.0


def task_4_scaling(output):
    print('\nTASK 4 — Min-max, Z-score, robust scaling')
    df = employee_dataset()
    columns = ['salary', 'age', 'years_experience', 'performance_score', 'projects_completed']
    normalized = df.copy()
    for col in columns:
        normalized[col + '_normalized'] = min_max_normalize(df[col])
        normalized[col + '_standardized'] = z_score_standardize(df[col])
        normalized[col + '_robust'] = robust_scale(df[col])
    print('Salary scaling comparison:\n', normalized[
        ['salary', 'salary_normalized', 'salary_standardized', 'salary_robust']])
    for col in columns:
        print(f"{col}: min={normalized[col+'_normalized'].min():.3f}, "
              f"max={normalized[col+'_normalized'].max():.3f}, "
              f"z-mean={normalized[col+'_standardized'].mean():.3f}, "
              f"z-std={normalized[col+'_standardized'].std():.3f}")
    normalized.to_csv(output / 'employees_scaled.csv', index=False)
    return {'original': df, 'normalized': normalized}


def survey_dataset():
    return pd.DataFrame({
        'respondent_id': range(1, 16),
        'education_level': ['High School', 'Bachelor', 'Master', 'PhD', 'High School',
                            'Bachelor', 'Master', 'Bachelor', 'PhD', 'High School',
                            'Master', 'Bachelor', 'PhD', 'Master', 'Bachelor'],
        'satisfaction': ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Satisfied',
                         'Satisfied', 'Very Satisfied', 'Neutral', 'Satisfied', 'Dissatisfied',
                         'Very Satisfied', 'Satisfied', 'Neutral', 'Very Satisfied', 'Satisfied'],
        'department': ['IT', 'HR', 'Finance', 'IT', 'Marketing', 'HR', 'IT', 'Finance',
                       'Marketing', 'HR', 'IT', 'Finance', 'Marketing', 'IT', 'HR'],
        'employment_type': ['Full-time', 'Part-time', 'Full-time', 'Full-time', 'Part-time',
                            'Full-time', 'Full-time', 'Contract', 'Full-time', 'Part-time',
                            'Full-time', 'Contract', 'Full-time', 'Full-time', 'Part-time'],
        'salary_range': ['50-60k', '60-70k', '70-80k', '80-90k', '50-60k',
                         '60-70k', '80-90k', '70-80k', '90-100k', '50-60k',
                         '80-90k', '70-80k', '90-100k', '80-90k', '60-70k'],
    })


EDUCATION_MAP = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
SATISFACTION_MAP = {'Dissatisfied': 0, 'Neutral': 1, 'Satisfied': 2, 'Very Satisfied': 3}


def handle_categorical_data(df, ordinal_cols=None, nominal_cols=None, high_card_cols=None):
    result = df.copy()
    for col, mapping in (ordinal_cols or {}).items():
        result[col + '_encoded'] = result[col].map(mapping)
    for col in (nominal_cols or []):
        dummies = pd.get_dummies(result[col], prefix=col, dtype=int)
        result = pd.concat([result, dummies], axis=1)
    for col in (high_card_cols or []):
        result[col + '_frequency'] = result[col].map(result[col].value_counts())
    return result


def task_5_categorical(output):
    print('\nTASK 5 — Categorical and high-cardinality encoding')
    survey = survey_dataset()
    survey['education_level_encoded'] = survey['education_level'].map(EDUCATION_MAP)
    survey['satisfaction_encoded'] = survey['satisfaction'].map(SATISFACTION_MAP)
    survey['education_level_label'] = LabelEncoder().fit_transform(survey['education_level'])
    # LabelEncoder uses alphabetical order, NOT domain-defined ordinal order.
    departments = pd.get_dummies(survey['department'], prefix='dept', dtype=int)
    employment = pd.get_dummies(survey['employment_type'], prefix='emp_type', dtype=int)
    encoded = pd.concat([survey, departments, employment], axis=1)
    print('Ordinal labels:\n', survey[['education_level', 'education_level_encoded',
                                      'satisfaction', 'satisfaction_encoded']].head())
    print('One-hot columns:', list(departments.columns) + list(employment.columns))
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
              'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
              'Seattle', 'Denver', 'Boston']
    purchases = [150, 200, 175, 300, 125, 250, 180, 220, 190, 275,
                 160, 210, 185, 240, 195, 320, 170, 230, 205, 280]
    high = pd.DataFrame({'customer_id': range(1, 21), 'city': cities,
                         'purchase_amount': purchases})
    high['city_frequency'] = high['city'].map(high['city'].value_counts())
    high['city_mean_encoded'] = high['city'].map(
        high.groupby('city')['purchase_amount'].mean())
    # The sample has one customer per city: training-set target encoding leaks each target.
    print('High-cardinality sample:\n', high.head())
    pipeline = handle_categorical_data(survey_dataset(),
                                       {'education_level': EDUCATION_MAP,
                                        'satisfaction': SATISFACTION_MAP},
                                       ['department', 'employment_type'])
    encoded.to_csv(output / 'survey_encoded.csv', index=False)
    high.to_csv(output / 'cities_encoded.csv', index=False)
    pipeline.to_csv(output / 'survey_pipeline.csv', index=False)
    return {'survey': survey, 'encoded': encoded, 'high_cardinality': high,
            'pipeline': pipeline}


def comprehensive_data_cleaning(df, config):
    """Config-driven cleaning; never changes the original DataFrame.

    Steps: missing_values, duplicates, data_types, normalization, categorical.
    Boolean conversions reject unknown strings; zero-variance scaling returns 0.
    """
    result = df.copy()
    for col, strategy in config.get('missing_values', {}).items():
        if strategy == 'drop':
            result = result.dropna(subset=[col])
        elif strategy in ('mean', 'median'):
            value = getattr(result[col], strategy)()
            result[col] = result[col].fillna(value)
        elif strategy == 'mode':
            modes = result[col].mode(dropna=True)
            if modes.empty:
                raise ValueError(f'Cannot fill {col}: no mode')
            result[col] = result[col].fillna(modes.iloc[0])
        elif isinstance(strategy, str) and strategy.startswith('value:'):
            result[col] = result[col].fillna(strategy.partition(':')[2])
        else:
            raise ValueError(f'Unknown missing-value strategy: {strategy}')
    dup = config.get('duplicates')
    if dup:
        if dup['method'] == 'all':
            result = result.drop_duplicates()
        elif dup['method'] == 'subset':
            result = result.drop_duplicates(subset=dup['columns'])
        else:
            raise ValueError('Unknown duplicates method')
    for col, dtype in config.get('data_types', {}).items():
        if dtype == 'numeric':
            result[col] = pd.to_numeric(result[col], errors='coerce')
        elif dtype == 'datetime':
            result[col] = pd.to_datetime(result[col], errors='coerce')
        elif dtype == 'boolean':
            result[col] = parse_boolean(result[col])
        else:
            raise ValueError(f'Unknown data type: {dtype}')
    scaling = {'min_max': ('normalized', min_max_normalize),
               'z_score': ('standardized', z_score_standardize),
               'robust': ('robust', robust_scale)}
    for col, method in config.get('normalization', {}).items():
        if method not in scaling:
            raise ValueError(f'Unknown normalization method: {method}')
        suffix, func = scaling[method]
        result[col + '_' + suffix] = func(result[col])
    categorical = config.get('categorical', {})
    if categorical:
        result = handle_categorical_data(result, categorical.get('ordinal'),
                                         categorical.get('nominal'),
                                         categorical.get('high_cardinality'))
    return result


def pipeline_demo(output):
    print('\nFINAL — Complete data-cleaning pipeline')
    demo = pd.DataFrame({'id': [1, 2, 2, 3, 4],
                         'age': [20, None, None, 40, 30],
                         'city': ['Surat', 'Mumbai', 'Mumbai', 'Delhi', 'Surat'],
                         'active': ['True', 'False', 'False', 'True', 'False'],
                         'score': ['10', '25', '25', '40', 'invalid']})
    config = {'missing_values': {'age': 'median'},
              'duplicates': {'method': 'all'},
              'data_types': {'score': 'numeric', 'active': 'boolean'},
              'normalization': {'age': 'min_max'},
              'categorical': {'nominal': ['city'], 'high_cardinality': ['city']}}
    clean = comprehensive_data_cleaning(demo, config)
    print(clean.to_string(index=False))
    clean.to_csv(output / 'complete_pipeline.csv', index=False)
    return clean


def run_all(output_dir='output'):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    print('Lab 61: Data Cleaning with Pandas | Pandas', pd.__version__,
          '| NumPy', np.__version__)
    results = (task_1_missing_values(output), task_2_duplicates(output),
               task_3_conversions(output), task_4_scaling(output),
               task_5_categorical(output), pipeline_demo(output))
    print('\nLAB 61 COMPLETED — files saved to', output.resolve())
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', default='output', help='Output CSV folder')
    args = parser.parse_args()
    run_all(args.output_dir)