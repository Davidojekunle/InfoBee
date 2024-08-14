from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Files(SQLModel, table=True):
    __tablename__ = "files"

    file_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    file_name: str
    file_path: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    status: str
    processed_data_path: Optional[str] = None

    user: Optional["User"] = Relationship(back_populates="files")
