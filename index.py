from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.urls import node


app = FastAPI();
app.include_router(node)
app.mount("/static", StaticFiles(directory='static'), name='static');