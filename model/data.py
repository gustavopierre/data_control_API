from sqlalchemy import Column, String, DateTime, Boolean, Integer
from datetime import datetime
from typing import Union
from model import Base


class Data(Base):
    __tablename__ = 'data'

    id = Column("pk_data", Integer, primary_key=True, autoincrement=True)
    name = Column(String(140), unique=True)
    area = Column(String(140))
    description = Column(String(255))
    source = Column(String(140))
    creator = Column(String(140))
    permitted = Column(Boolean, default=True, nullable=False)
    copyright = Column(String(140))
    link = Column(String(140))
    info = Column(String(255))
    coordinate_system = Column(String(140), nullable=False)
    creation_date = Column(String(10))
    update_date = Column(String(10))
    format = Column(String(150), nullable=False)
    check_date = Column(DateTime, default=datetime.now())

    def __init__(self,
                 name: str,
                 area: str,
                 description: str,
                 source: str,
                 creator: str,
                 permitted: bool,
                 copyright: str,
                 link: str,
                 info: str,
                 coordinate_system: str,
                 creation_date: str,
                 update_date: str,
                 format: str,
                 check_date: Union[DateTime, None] = None
                 ):
        """
        Creates a data

        Arguments:
            name {str} -- name of the data
            area {str} -- area of the data
            description {str} -- description of the data
            source {str} -- source of the data (where it was originally
                    obtained)
            creator {str} -- creator of the data
            permitted {bool} -- if thedata is permitted to be used
            copyright {str} -- copyright
            link {str} -- link to the data (directory, link of webserver,
                    link api, etc)
            info {str} -- additional information
            coordinate_system {str} -- coordinate system of the data
            creation_date {str} -- date of the creation of the data
            update_date {str} -- date of the last update of the data
            format {str} -- format of the data (shapefile, geopackage, etc)
            check_date {Union[DateTime, None]} -- date of the check of the data
        """
        self.name = name
        self.area = area
        self.description = description
        self.source = source
        self.creator = creator
        self.permitted = permitted
        self.copyright = copyright
        self.link = link
        self.info = info
        self.coordinate_system = coordinate_system
        self.creation_date = creation_date
        self.update_date = update_date
        self.format = format
        # se não for informada, será o data exata da inserção no banco
        if check_date:
            self.check_date = check_date
