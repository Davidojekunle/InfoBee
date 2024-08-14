from sqlmodel import SQLModel, create_engine, Field

db = "postgresql://datahive_user:zWypeCCigUzMZsdCSVujxnv409UEciIU@dpg-cqh167ks1f4s73bhcr60-a.virginia-postgres.render.com/datahive"
engine = create_engine(db)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)


class Hero(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=10, default=None)

create_db_and_table()



