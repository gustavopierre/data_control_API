from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime
from typing import Union
from model import Base


class Data(Base):
    __tablename__ = 'data'

    name = Column(String(140), primary_key=True)
    area = Column(String(140))
    description = Column(String(255))
    source = Column(String(140))
    creator = Column(String(140))
    permitted = Column(Boolean, default=True, nullable=False)
    copyright = Column(String(140))
    link = Column(String(140))
    info = Column(String(255))
    coordinate_system = Column(String(140))
    creation_date = Column(DateTime)
    update_date = Column(DateTime)
    check_date = Column(DateTime, default=datetime.now(), nullable=False)
    format = Column(String(150), nullable=False)
    

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
                 check_date: DateTime,
                 format: str,
                 creation_date: Union[DateTime, None] = None,
                 update_date: Union[DateTime, None] = None,
                 ):
        """
        Creates a data

        Arguments:
            name {str} -- name of the data
            area {str} -- area of the data
            description {str} -- description of the data
            source {str} -- source of the data (where it was originally obtained)
            creator {str} -- creator of the data
            permitted {bool} -- if thedata is permitted to be used
            copyright {str} -- copyright
            link {str} -- link to the data (directory, link of webserver, link api, etc)
            info {str} -- additional information
            coordinate_system {str} -- coordinate system of the data
            creation_date {Union[DateTime, None]} -- date of the creation of the data (default: {None})
            update_date {Union[DateTime, None]} -- date of the last update of the data (default: {None})
            check_date {DateTime} -- date of the last check
            format {str} -- format of the data (default: {"shp"})            
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
        # se não for informada, será o data exata da inserção no banco
        if creation_date:
            self.creation_date = creation_date

        if update_date:
            self.update_date = update_date

        if check_date:
            self.check_date = check_date
        self.format = format
