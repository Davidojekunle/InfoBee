from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .dataAnalysis import DataAnalysis


class Visualization(SQLModel, table=True):
    __tablename__ = "visualizations"

    visualization_id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="data_analysis.analysis_id")
    visualization_type: str
    parameters: str  
    image_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    analysis: Optional[DataAnalysis] = Relationship(back_populates="visualizations")