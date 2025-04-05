from pydantic import BaseModel
from typing import Optional, List, Union

from model.data import Data


class DataSchema(BaseModel):
    """ Defines how new data to be inserted should be represented
    """
    name: str = "Ireland County Boundaries"
    area: str = "All Ireland"
    description: str = "Ireland County Boundaries"
    source: str = "https://data.gov.ie/dataset/counties-\
        national-statutory-boundaries-2019"

    creator: Optional[str] = "Tailte Éireann – Surveying"
    permitted: bool = True
    copyright: Optional[str] = "Creative Commons Attribution 4.0"
    link: str = "\\Dataset\\Ireland\\Counties"
    info: Optional[str] = "None"
    coordinate_system: str = "ITM"
    creation_date: Union[str, None] = "01/01/2019"
    update_date: Union[str, None] = "01/01/2019"
    format: str = "SHP"
    # update frequency and bounding box
    update_frequency_days: Optional[int] = 90
    bounding_box: Optional[str] = None


class DataSearchSchema(BaseModel):
    """Define how a search should be represented. 
        That will be done based on the name of the data.
    """
    name: str = "Teste"


class AreaSearchSchema(BaseModel):
    """ Define how a search should be represented.
    """
    area: str = "Teste"


class ListDatasetSchema(BaseModel):
    """ Define how a list of data should be returned.
    """
    dataset: List[DataSchema]


def show_dataset(dataset: List[Data]):
    """ Returns a representation of the data following the schema defined in DataViewSchema.
    """
    result = []
    for data in dataset:
        result.append({
            "name": data.name,
            "area": data.area,
            "description": data.description,
            "source": data.source,
            "creator": data.creator,
            "permitted": data.permitted,
            "copyright": data.copyright,
            "link": data.link,
            "info": data.info,
            "coordinate_system": data.coordinate_system,
            "creation_date": data.creation_date,
            "update_date": data.update_date,
            "format": data.format,
            "check_date": data.check_date,
            # update frequency and bounding box
            "update_frequency_days": data.update_frequency_days,
            "bounding_box": data.bounding_box
        })

    return {"dataset": result}


class DataViewSchema(BaseModel):
    """ Define how a data is returned.
    """
    id: int = 1
    name: str = "Ireland County Boundaries"
    area: str = "All Ireland"
    description: str = "Ireland County Boundaries"
    source: Optional[str] =\
        "https://data.gov.ie/dataset/\
        counties-national-statutory-boundaries-2019"
    creator: Optional[str] = "Tailte Éireann – Surveying"
    permitted: bool = True
    copyright: Optional[str] = "Creative Commons Attribution 4.0"
    link: str = "\\Dataset\\Ireland\\Counties"
    info: Optional[str] = "None"
    coordinate_system: str = "ITM"
    creation_date: Union[str, None] = "01/01/2019"
    update_date: Union[str, None] = "01/01/2019"
    format: str = "SHP"
    # update frequency and bounding box
    update_frequency_days: Optional[int] = 90
    bounding_box: Optional[str] = None


class DataDelSchema(BaseModel):
    """ Define how should be the structure of the data returned after a removal request. 
    """
    message: str
    name: str


def show_data(data: Data):
    """ Returns a representation of the data following the schema 
    defined in DataViewSchema.
    """
    return {
        "id": data.id,
        "name": data.name,
        "area": data.area,
        "description": data.description,
        "source": data.source,
        "creator": data.creator,
        "permitted": data.permitted,
        "copyright": data.copyright,
        "link": data.link,
        "info": data.info,
        "coordinate_system": data.coordinate_system,
        "creation_date": data.creation_date,
        "update_date": data.update_date,
        "format": data.format,
        "check_date": data.check_date,
        # update frequency and bounding box
        "update_frequency_days": data.update_frequency_days,
        "bounding_box": data.bounding_box
    }
