from typing import Optional
from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = ''
    genre: str


movie_list = [
    {'id': 1, 'title': 'title1', 'description': 'description1', 'genre': 'genre1'},
    {'id': 2, 'title': 'title2', 'description': 'description2', 'genre': 'genre2'},
    {'id': 3, 'title': 'title3', 'description': 'description3', 'genre': 'genre3'},
    {'id': 4, 'title': 'title4', 'description': 'description4', 'genre': 'genre4'},
    {'id': 5, 'title': 'title5', 'description': 'description5', 'genre': 'genre1'},
    {'id': 6, 'title': 'title6', 'description': 'description6', 'genre': 'genre1'},
    {'id': 7, 'title': 'title7', 'description': 'description7', 'genre': 'genre2'},
    {'id': 8, 'title': 'title8', 'description': 'description8', 'genre': 'genre4'},
]

