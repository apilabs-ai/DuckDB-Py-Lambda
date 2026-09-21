import json

import duckdb
import pandas as pd


def lambda_handler(event, context):
    pandas_code = event.get('pandas_code')

    if not pandas_code:
        return {
            'statusCode': 400,
            'body': json.dumps('No Pandas code provided.')
        }

    try:
        # A shared namespace is required for DuckDB replacement scans to find
        # DataFrames created by the supplied code.
        local_env = {"pd": pd, "duckdb": duckdb}
        exec(pandas_code, local_env, local_env)
        result = local_env.get('result', 'No result variable found.')

        return {
            'statusCode': 200,
            'body': json.dumps(str(result))
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error executing code: {str(e)}')
        }
