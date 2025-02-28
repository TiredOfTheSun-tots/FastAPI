
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db_queries.db_def import create_tables, insert_data, CardsOrm
from db_queries.db_engine import get_db
from typing import List
from random import choice
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить доступ с любого источника (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
insert_data()



class CardBase(BaseModel):
    title: str
    description: str

class CardResponse(CardBase):
    card_id: int

class Config:
    orm_mode = True

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/random_card", response_model=CardResponse)
async def get_random_card(db: Session = Depends(get_db)):
    random_card = choice(db.query(CardsOrm).all())
    if not random_card:
        raise HTTPException(status_code=404, detail="No cards found")
    return random_card


