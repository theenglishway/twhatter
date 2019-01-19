from datetime import datetime

from bs4 import BeautifulSoup
from dataclasses import dataclass, fields, InitVar, field
from typing import List, Optional

from .mixins import ExtractableMixin


@dataclass
class MediaBase(ExtractableMixin):
    #: Links to images contained in the media
    image_links: List[str]

    @staticmethod
    def extract_image_links(soup):
        if not soup:
            return []

        try:
            datakw = "data-image-url"
            return [
                div[datakw]
                for div in soup.find_all('div', attrs={datakw: True})
            ]
        except:
            raise

    #: The soup extracted from the raw HTML
    soup: InitVar[BeautifulSoup] = None

    #https: // pbs.twimg.com / media / DxNof6AXQAAu2oU.jpg


class MediaImage(MediaBase):
    @staticmethod
    def condition(kwargs):
        return kwargs['image_links']



def media_factory(soup: BeautifulSoup) -> Optional[MediaBase]:
    """
    :param soup: the soup extracted from the raw html for that media
    :return: a well-formatted Media
    """
    kwargs = {
        f.name: MediaBase._extract_value(soup, f) for f in fields(MediaBase)
    }

    for kls in MediaBase.__subclasses__():
        try:
            if kls.condition(kwargs):
                return kls(soup=soup, **kwargs)
        except NotImplementedError:
            continue

    return None
