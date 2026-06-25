"""
Reads and validates data/config.json.
"""


def load_config(config_path: str = "data/config.json") -> dict:
    # TODO: open and parse config_path as JSON
    # TODO: validate required fields: works[].id, works[].resources[].lang,
    #       works[].resources[].format, works[].resources[].path
    # TODO: resolve relative paths to absolute paths from repo root
    # TODO: return validated config dict
    pass


def get_work(config: dict, work_id: str) -> dict:
    # TODO: find and return the work entry with matching id
    # TODO: raise ValueError if not found
    pass
