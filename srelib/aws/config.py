from dataclasses import dataclass

import srelib


@dataclass
class Config:

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_profile: str

    def __init__(self):
        our_config = srelib.config.get('aws', {})
        self.aws_profile = our_config.get('aws_profile')
        self.aws_access_key_id = our_config.get('aws_access_key_id')
        self.aws_secret_access_key = our_config.get('aws_secret_access_key')