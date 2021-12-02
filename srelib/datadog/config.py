from dataclasses import dataclass

import srelib


@dataclass
class Config:

    api_key: str
    application_key: str

    def __init__(self):
        our_config = srelib.config.get('datadog', {})
        self.api_key = our_config.get('api-key')
        self.application_key = our_config.get('application-key')
