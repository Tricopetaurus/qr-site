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

c = Config('', [])

def load_config(config_file: Path):
    global c
    log.info(f'Loading config file {config_file.absolute()}...')
    if not config_file.exists():
        log.error('Config file not found')
        return

    config = None
    with open(config_file, 'r') as f:
        parsed_obj = json.load(f)
        config = Config(**parsed_obj)

    if not config:
        log.error('Unknown error when parsing config file')

    log.info(f'Successfully loaded {config_file.absolute()}')
    c = config