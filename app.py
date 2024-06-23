from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from model import Session, Data
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="DataControl API", version="1.0.1")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc"
    )
data_tag = Tag(
    name="Dado",
    description="Adição, visualização e remoção de dado à/da base"
    )
"""comentario_tag = Tag(
    name="Comentario", 
    description="Adição de um comentário à um produtos cadastrado na base"
    )"""


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo
       de documentação.
    """
    return redirect('/openapi')


@app.post('/data', tags=[data_tag],
          responses={
              "200": DataViewSchema,
              "409": ErrorSchema,
              "400": ErrorSchema
              })
def add_data(form: DataSchema):
    """Adiciona um novo Dado à base de dados

    Retorna uma representação dos dados.
    """
    data = Data(
        name=form.name,
        description=form.description,
        check_date=form.check_date,
        creator=form.creator,
        permitted=form.permitted,
        copyright=form.copyright,
        link=form.link,
        info=form.info,
        coordinate_system=form.coordinate_system,
        area=form.area,
        creation_date=form.creation_date,
        update_date=form.update_date,
        format=form.format)

    logger.debug(f"Adicionando dado de nome: '{data.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando dado
        session.add(data)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado dado de nome: '{data.name}'")
        return show_data(data), 200

    except IntegrityError:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Dado de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar dado '{data.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo dado :/"
        logger.warning(f"Erro ao adicionar data '{data.name}', {error_msg}")
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
        logger.debug(f"{len(dataset)} dados encontrados")
        # retorna a representação de produto
        print(dataset)
        return show_dataset(dataset), 200


@app.get('/data', tags=[data_tag],
         responses={"200": DataViewSchema, "404": ErrorSchema})
def get_data(query: DataSearchSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    data_id = query.id
    logger.debug(f"Coletando dados sobre produto #{data_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    data = session.query(Data).filter(Data.id == data_id).first()

    if not data:
        # se o produto não foi encontrado
        error_msg = "Dado não encontrado na base :/"
        logger.warning(f"Erro ao buscar dado '{data_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Dado econtrado: '{data.name}'")
        # retorna a representação de produto
        return show_data(data), 200


@app.delete('/data', tags=[data_tag],
            responses={"200": DataDelSchema, "404": ErrorSchema})
def del_data(query: DataSearchSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    data_name = unquote(unquote(query.name))
    print(data_name)
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

'''
@app.post('/cometario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id  = form.produto_id
    logger.debug(f"Adicionando comentários ao produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{produto_id}")

    # retorna a representação de produto
    return apresenta_produto(produto), 200
'''
