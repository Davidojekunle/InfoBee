from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
# from .visualizations import Visualization

class DataAnalysis(SQLModel, table=True):
    __tablename__ = "data_analysis"

    analysis_id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int = Field(foreign_key="files.file_id")
    summary_statistics: str  # Consider using JSON type if supported
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    
    visualizations: List["Visualization"] = Relationship(back_populates="analysis")