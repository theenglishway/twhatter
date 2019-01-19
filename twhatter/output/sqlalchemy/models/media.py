from dataclasses import asdict

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from twhatter.output.sqlalchemy.db import Base


class Media(Base):
    __tablename__ = 'medias'

    id = Column(Integer, primary_key=True)
    _images_list = Column("images_list", String)

    @hybrid_property
    def images_list(self):
        return self._images_list.split(',')

    @images_list.setter
    def images_list(self, value):
        self._images_list = ','.join(value)

    @images_list.expression
    def images_list(cls):
        return cls._images_list
