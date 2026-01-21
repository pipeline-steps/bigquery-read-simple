import timeit

import pandas as pd
from google.cloud import bigquery
from steputil import StepArgs, StepArgsBuilder


def main(step: StepArgs):
    # setting up client
    project = step.config.billingProject
    print(f"Setting up bigquery client for project {project}")
    client = bigquery.Client(project=project)

    # executing query
    start_time = timeit.default_timer()
    query = step.config.query
    if not query:
        query = f"SELECT * FROM {step.config.inputTable}"
    print(f"Reading data using this query: {query}")
    df = client.query(query=query).to_dataframe()
    execution_time = timeit.default_timer() - start_time
    print(f"Read {len(df.columns)} columns and {len(df)} rows in {execution_time:.1f} seconds.")

    # Convert non-JSON-compatible values to strings for JSON serialization if configured
    if step.config.convertNonJsonValues:
        def is_json_compatible(val):
            """Check if a value is JSON-compatible."""
            if val is None or isinstance(val, (bool, int, float, str)):
                return True
            if isinstance(val, (list, dict)):
                return True
            return False

        for col in df.columns:
            # Convert datetime columns (pandas datetime64)
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
            # Convert timedelta columns
            elif pd.api.types.is_timedelta64_dtype(df[col]):
                df[col] = df[col].astype(str)
            # Convert object columns - check each value for JSON compatibility
            elif df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: x if is_json_compatible(x) else str(x))

    # store to output file
    step.output.writeJsons(df.to_dict('records'))

    print(f"Done")


def validate_config(config):
    """Validation function that checks config rules."""
    if config.query and config.inputTable:
        print("Cannot specify parameters `query` and `input_table` at the same time")
        return False
    if not config.query and not config.inputTable:
        print("Have to specify either parameter `query` or `input_table`")
        return False
    return True


if __name__ == "__main__":
    main(StepArgsBuilder()
         .output()
         .config("billingProject")
         .config("query", optional=True)
         .config("inputTable", optional=True)
         .config("convertNonJsonValues", optional=True, default_value=True)
         .validate(validate_config)
         .build()
         )
