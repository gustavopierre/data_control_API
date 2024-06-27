from pydantic import BaseModel
from typing import Optional, List

from model.data import Data


class DataSchema(BaseModel):
    """ Define como um novo dado a ser inserido deve ser representado
    """
    name: str = "Ireland County Boundaries"
    area: str = "All Ireland"
    description: str = "Ireland County Boundaries"
    source: str =\
        "https://data.gov.ie/dataset/\
        counties-national-statutory-boundaries-2019"
    creator: Optional[str] = "Tailte Éireann – Surveying"
    permitted: bool = True
    copyright: Optional[str] = "Creative Commons Attribution 4.0"
    link: str = "\\Dataset\\Ireland\\Counties"
    info: Optional[str] = "None"
    coordinate_system: str = "ITM"
    creation_date: Optional[str] = "01/01/2019"
    update_date: Optional[str] = "01/01/2019"
    format: str = "shapefile"


class DataSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na area do dado.
    """
    name: str = "Teste"


class ListDatasetSchema(BaseModel):
    """ Define como uma listagem de dados será retornada.
    """
    dataset: List[DataSchema]


def show_dataset(dataset: List[Data]):
    """ Retorna uma representação do dado seguindo o schema definido em
        DataViewSchema.
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
        })

    return {"dataset": result}


class DataViewSchema(BaseModel):
    """ Define how a data is returned.
    """
    id: int = 1
    name: str = "Ireland County Boundaries"
    area: str = "All Ireland"
    description: str = "Ireland County Boundaries"
    source: str =\
        "https://data.gov.ie/dataset/\
        counties-national-statutory-boundaries-2019"
    creator: Optional[str] = "Tailte Éireann – Surveying"
    permitted: bool = True
    copyright: Optional[str] = "Creative Commons Attribution 4.0"
    link: str = "\\Dataset\\Ireland\\Counties"
    info: Optional[str] = "None"
    coordinate_system: str = "ITM"
    creation_date: Optional[str] = "01/01/2019"
    update_date: Optional[str] = "01/01/2019"
    format: str = "shapefile"


class DataDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str


def show_data(data: Data):
    """ Retorna uma representação do dado seguindo o schema definido em
        DataViewSchema.
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
        "check_date": data.check_date
    }
