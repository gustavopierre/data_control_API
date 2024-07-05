from sqlalchemy import Column, String, DateTime, Boolean, Integer
from datetime import datetime
from typing import Union, Optional
from model import Base


class Data(Base):
    __tablename__ = 'data'

    id = Column("pk_data", Integer, primary_key=True, autoincrement=True)
    name = Column(String(140), unique=True)
    area = Column(String(20), nullable=False)
    description = Column(String(255))
    source = Column(String(140))
    creator = Column(String(140))
    permitted = Column(Boolean, default=True, nullable=False)
    copyright = Column(String(140))
    link = Column(String(140), nullable=False)
    info = Column(String(255))
    coordinate_system = Column(String(6), nullable=False)
    creation_date = Column(String(10))
    update_date = Column(String(10))
    format = Column(String(4), nullable=False)
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
                 check_date: datetime = datetime.now()
                 ):
        """
        Creates a data

        Arguments:
            name {str} -- name of the data
            area {str} -- area of the data. It must be: All Ireland,
                ROI - All, Carlow, Cavan, Clare, Cork, Donegal, Dublin,
                Galway, Kerry, Kildare, Kilkenny, Laois, Leitrim,
                Limerick, Longford, Louth, Mayo, Meath, Monaghan,
                Offaly, Roscommon, Sligo, Tipperary, Waterford,
                Westmeath, Wexford, Wicklow, UK - All, England,
                Scotland, Wales, or Northern Ireland.
            description {str} -- data description (Optional)
            source {str} -- data source, where it was originally 
                obtained (Optional)
            creator {str} -- data creator (Optional)
            permitted {bool} -- if the data is permitted to be used
            copyright {str} -- data license (Optional)
            link {str} -- link to the data (directory, link of webserver,
                link api, etc)
            info {str} -- additional information about the data (Optional)
            coordinate_system {str} -- coordinate system of the data.
                It must be Irish Transverse Mercator (ITM), British National
                Grid (BNG), or World Geodetic System 1984(WGS84)
            creation_date {str} -- date of the data creation (Optional)
            update_date {str} -- date of the last data update (Optional)
            format {str} -- format of the data It must be: Shapefile (SHP),
                Geodatabase (GDB), Common Separated Values (CSV), Web Feature
                Service (WFS), or Web Map Service (WMS).
            check_date {DateTime} -- date of the check of the data
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
        # if the check_date is not informed, it will be the exact date 
        # of the insertion in the database
        if check_date:
            self.check_date = check_date
