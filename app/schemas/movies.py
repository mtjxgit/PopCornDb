from pydantic import BaseModel

class Movie(BaseModel):
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
    
    