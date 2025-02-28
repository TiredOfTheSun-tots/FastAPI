
from sqlalchemy import insert, text, Column, Integer, String, Table, MetaData, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from db_queries.db_engine import sync_engine, async_engine, Base, session_factory, async_session_factory

class CardsOrm(Base):
    __tablename__ = "cards"

    card_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = Column(String, index=True)
    description: Mapped[str] = Column(String)

def get_sync_engine():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")

async def get_async_engine():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")

def create_tables():
    sync_engine.echo=False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo=True

def insert_data():
    with session_factory() as session:
        card_vladick = CardsOrm(title="Vladick",description="pidoraqs")
        card_tulen = CardsOrm(title="Tulen",description="Vilnus")
        session.add_all([card_vladick, card_tulen])
        session.commit()

async def async_insert_data():
    async with async_session_factory() as session:
        card_vladick = CardsOrm(title="Vladick",description="pidoraqs")
        card_tulen = CardsOrm(title="Tulen",description="Vilnus")
        session.add_all([card_vladick, card_tulen])
        await session.commit()




def insert_data():
    with session_factory() as session:
        # Пример загрузки изображения
        with open("static/images/vladick.png", "rb") as f:
            image_vladick = f.read()  # Чтение изображения в бинарном формате

        # Создание объектов для вставки, включая изображения
        card_vladick = CardsOrm(title="Vladick", description="pidoraqs")
        card_tulen = CardsOrm(title="Tulen", description="Vilnus")

        session.add_all([card_vladick, card_tulen])
        session.commit()



# cards = Table(
#     "cards",
#     metadata_obj,
#     Column("card_id", Integer, primary_key=True),
#     Column("title", String),
#     Column("description", String)
# )

# def insert_data():
#     with sync_engine.connect() as conn:
#         stmt = insert(cards).values(
#             [
#                 {"title":"Vladick"},
#                 {"title":"Tulen"}
#             ]
#         )
#         conn.execute(stmt)
#         conn.commit()
