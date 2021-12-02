"""
# srelib.config

Provides library-wide configuration and secrets access

By default, the library searches for a configuration file called `srelib.yaml`.
This is an example of the contents of this configuration file:

    datadog:
      api-key: cee2...
      application-key: 09ff...

    aws:
      aws_profile: '<aws_profile_name>'
      aws_access_key_id: 'AKIA...'
      aws_secret_access_key: 'tPYI...'

"""

import os
import yaml


class Config:

    def __init__(self):
        self.config = None
        self.try_yaml_file()

    def try_yaml_file(self, filename: str = 'srelib.yaml') -> None:
        if os.path.exists(filename):
            with open(filename, 'r') as config_file:
                self.config = yaml.safe_load(config_file)

    def get(self, key: str, default_value=None):
        return self.config.get(key, default_value) \
            if self.config is not None \
            else default_value
