from datetime import datetime
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Data
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="DataControl API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentation",
    description="Documentation Selection: Swagger, Redoc ou RapiDoc"
    )
data_tag = Tag(
    name="Data",
    description="Adding, Viewing and Removing Data to/from the Database"
    )


@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, where it allows the choice of documentation style.
    """
    return redirect('/openapi')


@app.post('/data', tags=[data_tag],
          responses={
              "200": DataViewSchema,
              "409": ErrorSchema,
              "400": ErrorSchema
              })
def add_data(form: DataSchema):
    """Add a new Data to the database

    Returns a representation of the data.
    """
    data = Data(
        name=form.name,
        area=form.area,
        description=form.description,
        source=form.source,
        creator=form.creator,
        permitted=form.permitted,
        copyright=form.copyright,
        link=form.link,
        info=form.info,
        coordinate_system=form.coordinate_system,
        creation_date=form.creation_date,
        update_date=form.update_date,
        format=form.format)

    logger.debug(f"Adding Data named: '{data.name}'")
    try:
        # creating a connection with the database
        session = Session()
        # adding data to the session
        session.add(data)
        # effectively executing the command to add new data to the table
        session.commit()
        logger.debug(f"Added Data named: '{data.name}'")
        return show_data(data), 200

    except IntegrityError:
        # name duplicity is the likely reason for the IntegrityError
        error_msg = "Data has same name as one saved on the database :/"
        logger.warning(f"Error to add data '{data.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        # caso um erro fora do previsto
        error_msg = "It is not possible to save new data :/"
        logger.warning(f"Error to add data '{data.name}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/dataset', tags=[data_tag],
         responses={"200": ListDatasetSchema, "404": ErrorSchema})
def get_dataset():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug("Coletando dados ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    dataset = session.query(Data).all()

    if not dataset:
        # se não há produtos cadastrados
        return {"Dataset": []}, 200
    else:
        logger.debug(f"{len(dataset)} data found")
        # retorna a representação de produto
        print(dataset)
        return show_dataset(dataset), 200


@app.get('/data', tags=[data_tag],
         responses={"200": DataViewSchema, "404": ErrorSchema})
def get_data(query: DataSearchSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    data_name = query.name
    logger.debug(f"Coletando dados sobre produto #{data_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # se o produto não foi encontrado
        error_msg = "Dado não encontrado na base :/"
        logger.warning(f"Erro ao buscar dado '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Dado econtrado: '{data.name}'")
        # retorna a representação de produto
        return show_data(data), 200


@app.patch('/data', tags=[data_tag],
            responses={"200": DataViewSchema, "404": ErrorSchema})
def patch_data(query: DataSearchSchema):
    """Atualiza o check_date, com a dta corrente, de um Produto a partir do 
    nome de produto informado """
    data_name = query.name
    logger.debug(f"Coletando dados sobre produto #{data_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # se o produto não foi encontrado
        error_msg = "Dado não encontrado na base :/"
        logger.warning(f"Erro ao buscar dado '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Dado econtrado: '{data.name}'")
        data.check_date = datetime.now()
        session.commit()
        logger.debug(f"Dado alterado: '{data.name}'")
        # retorna a representação de produto
        return show_data(data), 200


@app.put('/data', tags=[data_tag],
            responses={"200": DataViewSchema, "404": ErrorSchema})
def update_data(query: DataSearchSchema, form: DataSchema):
    """Atualiza um Produto a partir do nome de produto informado

    Retorna uma representação do produto atualizado.
    """
    data_name = query.name
    logger.debug(f"Coletando dados sobre produto #{data_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # se o produto não foi encontrado
        error_msg = "Dado não encontrado na base :/"
        logger.warning(f"Erro ao buscar dado '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Dado encontrado: '{data.name}'")
        try:
            # atualizando os dados
            data.name = form.name
            data.area = form.area
            data.description = form.description
            data.source = form.source
            data.creator = form.creator
            data.permitted = form.permitted
            data.copyright = form.copyright
            data.link = form.link
            data.info = form.info
            data.coordinate_system = form.coordinate_system
            data.creation_date = form.creation_date
            data.update_date = form.update_date
            data.format = form.format
            data.check_date = datetime.now()
            session.commit()
            logger.debug(f"Dado atualizado: '{data.name}'")
            # retorna a representação de produto
            return show_data(data), 200
        
        except IntegrityError:
            # name duplicity is the likely reason for the IntegrityError
            error_msg = "Data has same name as one saved on the database :/"
            logger.warning(f"Error to add data '{data.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        except Exception:
            # caso um erro fora do previsto
            error_msg = "It is not possible to save new data :/"
            logger.warning(f"Error to add data '{data.name}', {error_msg}")
            return {"message": error_msg}, 400


@app.delete('/data', tags=[data_tag],
            responses={"200": DataDelSchema, "404": ErrorSchema})
def del_data(query: DataSearchSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    data_name = unquote(unquote(query.name))
    logger.debug(f"Deletando dados sobre produto #{data_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Data).filter(Data.name == data_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado dado #{data_name}")
        return {"message": "Dado removido", "id": data_name}
    else:
        # se o produto não foi encontrado
        error_msg = "Dado não encontrado na base :/"
        logger.warning(f"Erro ao deletar dado #'{data_name}', {error_msg}")
        return {"message": error_msg}, 404
