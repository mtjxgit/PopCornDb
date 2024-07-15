"""
Module containing Pydantic BaseModel classes for movie-related data schemas.
"""
from pydantic import BaseModel

class Movie(BaseModel):
    """
    Represents a movie with its details.
    """
    title : str
    rating: str
    image_url : str
    desc:str
    ott:str
    ott_image:str
    year :str
    runtime : str
    certificate : str
    genre:str
    director: str
    writers:str
    stars: str
