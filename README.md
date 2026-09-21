# DuckDB pandas Lambda

AWS Lambda function for running pandas code with DuckDB SQL analytics.

## Runtime versions

- DuckDB 1.4.5 LTS (Andium)
- pandas 2.3.3
- NumPy 2.2.6

Versions are pinned in `requirements.txt` and asserted by regression tests.

## Test locally

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

## Invoke

Pass Python code in the `pandas_code` property and assign the returned value to
`result`:

```json
{
  "pandas_code": "df = pd.DataFrame({'category': ['a', 'a', 'b'], 'amount': [10, 20, 5]})\nresult = duckdb.sql('SELECT category, SUM(amount) AS total FROM df GROUP BY category ORDER BY category').df()"
}
```

`pandas` is already available as `pd`, and `duckdb` is already available as
`duckdb`. A missing input returns HTTP-style status 400; execution errors return
status 500.

> **Security:** this example intentionally executes supplied Python code. Do not
> expose it to untrusted callers. Restrict invocation permissions and treat it as
> arbitrary code execution inside the Lambda role and network boundary.
