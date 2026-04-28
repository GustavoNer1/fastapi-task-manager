from fastapi import FastAPI

from fast_api.router import auth, users

app = FastAPI(title='Minha API Teste')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/test')
def get_api():
    return {'text': 'Hellow World'}
