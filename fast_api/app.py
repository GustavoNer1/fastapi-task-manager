import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

from fast_api.router import auth, todos, users

app = FastAPI(title='Minha API Teste')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/test')
def get_api():
    return {'text': 'Hello World'}
