from pathlib import Path
from typing import List
from dataclasses import dataclass
import json

from .logs import get_logger
log = get_logger(__name__)

@dataclass
class Route:
    title: str
    route: str
    description: str

@dataclass
class Config:
    secret: str
    routes: List[Route]


__valid = False
c = Config('', [])

def is_valid():
    global __valid
    return __valid

def load_config(config_file: Path):
    global c
    global __valid
    log.info(f'Loading config file {config_file.absolute()}...')
    if not config_file.exists():
        log.error('Config file not found')
        return

    config = None
    with open(config_file, 'r') as f:
        parsed_obj = json.load(f)
        config = Config(**parsed_obj)

    # Easy check for uniqueness of routes.
    # Let's create a list, and a set. They should have the same length.
    all_routes = [r['route'] for r in config.routes]
    if len(all_routes) != len(set(all_routes)):
        __valid = False
        log.error(f'All routes must be unique! Check {config_file.absolute()}')
        return

    if not config:
        __valid = False
        log.error('Unknown error when parsing config file')
        return

    log.info(f'Successfully loaded {config_file.absolute()}')
    c = config
    __valid = True

