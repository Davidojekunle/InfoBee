# database.py
from sqlmodel import create_engine, SQLModel, Session
from models import Admin, DataAnalysis, Files, Notification, Payment, UserManagement, Visualization, SubscriptionPlan
# Import all models to ensure they are registered with SQLModel's metadata
# from models.admin import Admin
# from models.dataAnalysis import DataAnalysis
# from models.files import File
# from models.notifications import Notification
# from models.payment import Payment
# from models.subscription import SubscriptionPlan
# from models.usermanagements import UserManagement
# from models.visualizations import Visualization

# Define the database URL and create the engine
sql_url = "sqlite:///Archive.db"
engine = create_engine(sql_url, echo=True)

def create_db_and_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



create_db_and_tables()
sql_url = "postgresql://datahive_user:zWypeCCigUzMZsdCSVujxnv409UEciIU@dpg-cqh167ks1f4s73bhcr60-a.virginia-postgres.render.com/datahive"