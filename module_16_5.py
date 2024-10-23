from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI(title='CRUD FastApi')
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    user_id: int = None
    username: str
    age: int

@app.get('/')
async def all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def all_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id - 1]})

@app.post('/user/{username}/{age}')
async def add_user(user: User) -> User:
    user.user_id = len(users) + 1
    users.append(user)
    return users[-1]

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str,  age: int) -> User:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete('/user/{user_id}')
async def del_user(user_id: int) -> User:
    try:
        if users[user_id - 1].user_id == user_id:
            del_user = users.pop(user_id - 1)
        else:
            raise HTTPException(status_code=404, detail='User was not found')
        return del_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

# if __name__ == '__main__':
