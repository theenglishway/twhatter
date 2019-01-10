from dataclasses import Field, InitVar
from typing import Any

from bs4 import BeautifulSoup


class ExtractableMixin:
    """Mixin to extract values from soup"""
    def __post_init__(self, soup: BeautifulSoup):
        self.soup = soup

    @classmethod
    def _extract_value(cls, soup: BeautifulSoup, data_field: Field) -> Any:
        fn = getattr(cls, "extract_{}".format(data_field.name), None)
        if not fn:
            raise NotImplementedError(
                "Extract function for field '{}' is not "
                "implemented".format(data_field.name)
            )

        return fn(soup)

    @staticmethod
    def _extract_from_div(soup, div_class, data_kw):
        kw = "data-{}".format(data_kw)
        return(
            soup.find('div', class_=div_class, attrs={kw: True})[kw]
        )

    @staticmethod
    def _extract_from_span(soup, distinct_span, data_kw):
        return (
            soup.find('span', distinct_span)
                .find('span', attrs={data_kw: True})
            [data_kw]
        )

    @staticmethod
    def extract_soup(soup):
        return soup
