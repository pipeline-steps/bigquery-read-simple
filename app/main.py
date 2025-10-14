import argparse
import sys
import timeit

from config import create_config
from google.cloud import bigquery


def main(config_path: str, output_path: str):
    """
    read configuration
    """
    config = create_config(config_path)

    # setting up client
    print(f"Setting up bigquery client for project {config.billing_project}")
    client = bigquery.Client(project=config.billing_project)

    # executing query
    print(f"Reading data from {config.input_table}")
    start_time = timeit.default_timer()
    if config.query:
        query = config.query
    else:
        query = f"SELECT * FROM {config.input_table}"
    df = client.query(query=query).to_dataframe()
    execution_time = timeit.default_timer() - start_time
    print(f"Read {len(df.columns)} columns and {len(df)} rows in {execution_time:.1f} seconds.")

    # store to output file
    print(f"Writing data to file {output_path}")
    df.to_json(path_or_buf=output_path, orient='records', lines=True)

    print(f"Done")


if __name__ == "__main__":
    if len(sys.argv) <= 1:  # no arguments besides script name, print README.md
        with open("/app/README.md", "r", encoding="utf-8") as file:
            content = file.read()
        # Print content to output
        print(content)
        sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = vars(parser.parse_args())
    main(
        config_path=args["config"],
        output_path=args["output"]
    )
