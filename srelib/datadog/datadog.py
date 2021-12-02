# encoding: utf-8

import logging
import requests

from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import metrics_api

from .config import Config


class Datadog:
    def __init__(self):
        self.config = Config()

    def get_hosts(self, filter_=None):
        api_key = self.config.api_key
        application_key = self.config.application_key

        # TODO support site attribute (datadoghq.eu vs .com)
        api_url = "https://api.datadoghq.com/api/v1/hosts"
        parameters = f"?filter={filter_}&api_key={api_key}&application_key={application_key}"

        api_url += parameters

        logging.info(f"Datadog url: {api_url}")
        response = requests.get(api_url, timeout=10)
        return response.json()

    def _get_datadog_configuration(self):
        return Configuration(api_key={
            'apiKeyAuth': self.config.api_key,
            'appKeyAuth': self.config.application_key})

    def get_datadog_apiclient(self):
        return ApiClient(self._get_datadog_configuration())

    def list_metrics(self, query):
        """
        :param query: Query string to search metrics upon. Must be prefixed with `metrics:`.
        """
        with self.get_datadog_apiclient() as api_client:
            api_instance = metrics_api.MetricsApi(api_client)
            try:
                api_response = api_instance.list_metrics(query)
                return api_response
            except ApiException as e:
                print("Exception when calling MetricsApi->list_metrics: %s\n" % e)

    def get_metrics(self, metric_name: str, from_: int, to: int):
        """
        :param metric_name: Query string to search metrics upon. Must be prefixed with `metrics:`
        :param from_: unix epoch for the beginning of the period
        :param to: unix epoch for the end of the period
        """
        with self.get_datadog_apiclient() as api_client:
            api_instance = metrics_api.MetricsApi(api_client)
            try:
                api_response = api_instance.query_metrics(from_, to, metric_name)
                return api_response
            except ApiException as e:
                print("Exception when calling MetricsApi->list_metrics: %s\n" % e)

    def get_metric_datapoints_by_tag(self, datapoints):
        """
        Used to extract raw datapoints from a previous get_metrics() call

        :param datapoints:
        :return:
        """
        if 'series' not in datapoints:
            return None

        if 'status' not in datapoints or datapoints['status'] != 'ok':
            return None

        datapoints_by_tag = dict()

        for series in datapoints['series']:

            metric = series['metric']
            tags = series['tag_set']
            assert len(tags) == 1

            tag = tags[0]
            datapoints_by_tag[tag] = series['pointlist']

        return datapoints_by_tag
