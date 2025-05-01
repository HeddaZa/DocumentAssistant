import yaml


def load_config():
    """
    Load configuration from the YAML file.

    Returns:
        dict: Parsed configuration as a dictionary.
    """
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config
