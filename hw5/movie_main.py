from fastapi import FastAPI, HTTPException
from .movie_orm import Movie, movie_list


intro = """ Создать API для получения списка фильмов по жанру.
    Приложение должно иметь возможность получать список фильмов по заданному жанру.
 Создайте модуль приложения и настройте сервер и маршрутизацию.
 Создайте класс Movie с полями id, title, description и genre.
 Создайте список movies для хранения фильмов.
 Создайте маршрут для получения списка фильмов по жанру (метод GET).
 Реализуйте валидацию данных запроса и ответа.
 """


app = FastAPI()


@app.get('/')
async def root():
    return {"mess": intro}


@app.get("/movie/", response_model=list[Movie])
async def get_mov(genre: str = None):
    if genre:
        return [mov for mov in movie_list if mov['genre'] == genre]
    return movie_list


@app.post('/movie/', response_model=Movie)
async def new_mov(movie: Movie):
    movie_list.append(movie)
    return movie


@app.put('/movie/')#, response_model=Movie) #TODO с ним почему-то не работает HTTPException
async def edit_mov(movie: Movie):
    for mov in movie_list:
        if mov['id'] == movie.id:
            mov['title'] = movie.title
            mov['description'] = movie.description
            mov['genre'] = movie.genre
            return movie
    return HTTPException(status_code=404, detail="object not found")


@app.delete('/movie/')#, response_model=str) #TODO с ним почему-то не работает HTTPException
async def delete_mov(movie: Movie):
    for i, mov in enumerate(movie_list):
        if mov['id'] == movie.id:
            del_title = mov['title']
            movie_list.pop(i)
            return del_title
    return HTTPException(status_code=404, detail="object not found")


