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

    # Convert to records and handle non-JSON types (temporary until steputil is fixed)
    records = df.to_dict('records')
    for record in records:
        for key, value in record.items():
            if not isinstance(value, (type(None), bool, int, float, str, list, dict)):
                record[key] = str(value)

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
         .validate(validate_config)
         .build()
         )
