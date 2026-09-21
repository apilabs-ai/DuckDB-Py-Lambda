import json

import duckdb
import pandas as pd

from lambda_function import lambda_handler


def invoke(code):
    return lambda_handler({"pandas_code": code}, None)


def test_duckdb_version_is_pinned_to_lts():
    assert duckdb.sql("SELECT version()").fetchone()[0] == "v1.4.5"


def test_dataframe_sql_analytics():
    response = invoke(
        """
df = pd.DataFrame({
    'category': ['alpha', 'alpha', 'beta', 'beta'],
    'amount': [10.25, 5.75, 20.0, None],
    'recorded_at': pd.to_datetime([
        '2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'
    ])
})
result = duckdb.sql('''
    SELECT category, COUNT(*) AS records, SUM(amount) AS total
    FROM df GROUP BY category ORDER BY category
''').df().to_dict(orient='records')
"""
    )

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "'category': 'alpha'" in body
    assert "'records': 2" in body
    assert "'total': 16.0" in body
    assert "'category': 'beta'" in body
    assert "'total': 20.0" in body


def test_pandas_version_is_on_compatibility_line():
    assert pd.__version__ == "2.3.3"


def test_missing_code_returns_400():
    response = lambda_handler({}, None)
    assert response["statusCode"] == 400


def test_invalid_sql_returns_500():
    response = invoke("result = duckdb.sql('SELECT missing_column').fetchall()")
    assert response["statusCode"] == 500
    assert "missing_column" in json.loads(response["body"])


def test_missing_result_has_clear_message():
    response = invoke("value = 42")
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == "No result variable found."
