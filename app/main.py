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

    # Convert dataframe to records
    records = df.to_dict('records')

    # Convert non-JSON-compatible values to strings for JSON serialization if configured
    if step.config.convertNonJsonValues:
        def convert_value(val):
            """Convert non-JSON-compatible values to strings."""
            if val is None or isinstance(val, (bool, int, float, str, list, dict)):
                return val
            # Convert any other type to string
            return str(val)

        records = [
            {key: convert_value(value) for key, value in record.items()}
            for record in records
        ]

    # store to output file
    step.output.writeJsons(records)

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
