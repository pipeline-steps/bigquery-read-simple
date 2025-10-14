from json import load


class Config:
    def __init__(self, input_table, query, billing_project):
        self.input_table = input_table
        self.query = query
        self.billing_project = billing_project
        if query and input_table:
            raise ValueError("Cannot specify parameters `query` and `input_table` at the same time")
        if not query and not input_table:
            raise ValueError("Have to specify either parameter `query` or `input_table`")


def create_config(config_path: str):
    # read config json into a dict
    with open(config_path) as f:
        config = load(f)
    return Config( config.get("inputTable"), config.get("query"), config["billingProject"])
