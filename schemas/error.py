from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Define how an error message should be represented
    """ 
    message: str
