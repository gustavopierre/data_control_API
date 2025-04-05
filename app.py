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

# defining tags
home_tag = Tag(
    name="Documentation",
    description="Documentation Selection: Swagger, Redoc ou RapiDoc"
    )
data_tag = Tag(
    name="Data",
    description="Searching, Adding, Viewing and Removing Data to/from the Database"
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
        format=form.format,
        # update frequency and bounding box
        update_frequency_days=form.update_frequency_days,
        bounding_box=form.bounding_box
        )

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
        # in case of a error out of the expected
        error_msg = "It is not possible to save new data :/"
        logger.warning(f"Error to add data '{data.name}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/dataset', tags=[data_tag],
         responses={"200": ListDatasetSchema, "404": ErrorSchema})
def get_dataset():
    """Search all Dataset.
    Returns a representation of the list of Data.
    """
    logger.debug("Collecting data from the database.")
    # creating a connection with the database
    session = Session()
    # searching
    dataset = session.query(Data).all()

    if not dataset:
        # if there are no registered data
        return {"Dataset": []}, 200
    else:
        logger.debug(f"{len(dataset)} data found")
        # returns the representation of data
        print(dataset)
        return show_dataset(dataset), 200


@app.get('/data', tags=[data_tag],
         responses={"200": DataViewSchema, "404": ErrorSchema})
def get_data(query: DataSearchSchema):
    """Search for a Data from the data name
    
    Returns a representation of the Data.
    """
    data_name = query.name
    logger.debug(f"Collecting data from the product: #{data_name}") 
    
    # creating a connection with the database
    session = Session()
    # searching
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # if the data was not found
        error_msg = "Data not found in the database :/"
        logger.warning(f"Error searching for data '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Data found: '{data.name}'")
        # returns the representation of data
        return show_data(data), 200


@app.get('/area', tags=[data_tag],
         responses={"200": ListDatasetSchema, "404": ErrorSchema})
def get_area(query: AreaSearchSchema):
    """ Search for a Data from the data area

    Returns a representation of the Data
    """
    data_area = query.area
    logger.debug(f"Collecting data from the area: #{data_area}")
    # creating a connection with the database
    session = Session()
    # searching
    dataset = session.query(Data).filter(Data.area == data_area).all()

    if not dataset:
        # if the data was not found
        error_msg = "Data not found in the database :/"
        logger.warning(f"Error searching for data '{data_area}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"{len(dataset)} data found")
        # returns the representation of data
        return show_dataset(dataset), 200


@app.patch('/data', tags=[data_tag],
           responses={"200": DataViewSchema, "404": ErrorSchema})
def patch_data(query: DataSearchSchema):
    """Update the check date, with the current date, of a specified Data by its name
    """
    data_name = query.name
    logger.debug(f"Collecting data from the product: #{data_name}")
    # creating a connection with the database
    session = Session()
    # searching
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # if the data was not found
        error_msg = "Data not found in the database :/"
        logger.warning(f"Error searching for data '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Data found: '{data.name}'")
        data.check_date = datetime.now()
        session.commit()
        logger.debug(f"Data changed: '{data.name}'")
        # returns the representation of data
        return show_data(data), 200


@app.put('/data', tags=[data_tag],
         responses={"200": DataViewSchema, "404": ErrorSchema})
def update_data(query: DataSearchSchema, form: DataSchema):
    """Update a Data from the informed name of the data
    
    Returns a representation of the updated data.
    """
    data_name = query.name
    logger.debug(f"Collecting data from the product: #{data_name}")
    # creating a connection with the database
    session = Session()
    # searching
    data = session.query(Data).filter(Data.name == data_name).first()

    if not data:
        # if the data was not found
        error_msg = "Data not found in the database :/"
        logger.warning(f"Error searching for data '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Data found: '{data.name}'")
        try:
            # updating the data
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
            # update frequency and bounding box
            data.update_frequency_days = form.update_frequency_days
            data.bounding_box = form.bounding_box
            
            # effectively executing the command to update the data in the table
            # and committing the changes to the database
            session.commit()
            logger.debug(f"Dado atualizado: '{data.name}'")
            # returns the representation of data
            return show_data(data), 200

        except IntegrityError:
            # name duplicity is the likely reason for the IntegrityError
            error_msg = "Data has same name as one saved on the database :/"
            logger.warning(f"Error to add data '{data.name}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception:
            # in case of a error out of the expected
            error_msg = "It is not possible to save new data :/"
            logger.warning(f"Error to add data '{data.name}', {error_msg}")
            return {"message": error_msg}, 400


@app.delete('/data', tags=[data_tag],
            responses={"200": DataDelSchema, "404": ErrorSchema})
def del_data(query: DataSearchSchema):
    """Delete a Data from the informed name of the data

    Returns a confirmation message of the removal.
    """
    data_name = unquote(unquote(query.name))
    logger.debug(f"Deleting data about product #{data_name}")
    # creating a connection with the database
    session = Session()
    # deleting
    count = session.query(Data).filter(Data.name == data_name).delete()
    session.commit()

    if count:
        # returns the representation of the confirmation message
        logger.debug(f"Deleted data #{data_name}")
        return {"message": "Data removed", "name": data_name}
    else:
        # if the data was not found
        error_msg = "Data not found in the database :/"
        logger.warning(f"Error searching for data '{data_name}', {error_msg}")
        return {"message": error_msg}, 404
