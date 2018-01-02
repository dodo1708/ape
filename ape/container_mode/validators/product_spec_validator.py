from __future__ import unicode_literals, print_function
import codecs
import json

from typing import Dict, List
__all__ = ['ProductSpecValidator']


class ProductSpecValidator(object):
    def __init__(self, spec_path: str, product_name: str, feature_list: List[str]) -> None:
        """
        Constructor
        :param spec_path: file path to the product spec json
        :param product_name: the name of the product to extract the concrete spec
        :param feature_list: the list of features that will be checked
        """
        self.product_specs = self._read(spec_path, product_name)
        self.feature_list = feature_list
        self.errors_mandatory = []
        self.errors_never = []

    def is_valid(self) -> bool:
        """
        Checks the feature list product spec against.
        Checks if all mandartory features are contained;
        Checks that all "never" features are not contained
        :return: boolean
        """
        for spec in self.product_specs:

            for feature in spec.get('mandatory', []):
                if feature.replace('__', '.') not in self.feature_list:
                    self.errors_mandatory.append(feature)

            for feature in spec.get('never', []):
                if feature.replace('__', '.') in self.feature_list:
                    self.errors_never.append(feature)

        return not self.has_errors()

    def get_errors_mandatory(self) -> List[str]:
        """
        Returns the list of features that are mandatory but missing in the passed feature list.
        :return: list
        """
        return self.errors_mandatory

    def get_errors_never(self) -> List[str]:
        """
        Returns the list if featzres that are declaed as "never" but are contained in the feature list.
        :return:
        """
        return self.errors_never

    def has_errors(self) -> bool:
        """
        Returns true if any error occured.
        :return: boolean
        """
        return len(self.get_errors_mandatory()) > 0 or len(self.get_errors_never()) > 0

    def _read(self, spec_path: str, product_name: str) -> List[Dict[str, List[str]]]:
        """
        Reads the spec files and extracts the concrete product spec.
        :param spec_path:
        :param product_name:
        :return:
        """
        matches = []
        with codecs.open(spec_path, 'r') as f:
            for entry in json.loads(f.read()):
                if product_name in entry.get('products'):
                    matches.append(entry)
        return matches
