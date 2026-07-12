from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class NDADocument(SQLModel, table=True):
    __tablename__ = "nda_documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    party_a_name: str
    party_a_company: Optional[str] = None
    party_a_address: str
    party_b_name: str
    party_b_company: Optional[str] = None
    party_b_address: str
    effective_date: str
    jurisdiction: str
    term: str
    purpose: Optional[str] = None

    filled_text: Optional[str] = None
