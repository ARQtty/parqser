from typing import Dict, Any
from parqser.scrapper.states import DownloadState


class BasePage:
    def __init__(self, source_html: str, status: DownloadState):
        self.source_html = source_html
        self.status = status
        self._parse_results = {}

    def get_source(self) -> str:
        return self.source_html

    def add_parsed_parameter(self, param_name: str, param_value: Any):
        if param_name in self._parse_results.keys():
            raise AttributeError(f'Parameter {param_name} has already parsed')
        self._parse_results[param_name] = param_value

    def to_dict(self) -> Dict[str, Any]:
        return self._parse_results
