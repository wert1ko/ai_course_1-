from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.database import get_session
from app.models import NDADocument
from app.auth import get_user_from_token
from sqlalchemy import select

router = APIRouter(prefix="/nda", tags=["nda"])

COOKIE_NAME = "session"


class NDASaveRequest(BaseModel):
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


class NDADocumentResponse(BaseModel):
    id: int
    party_a_name: str
    party_a_company: Optional[str]
    party_a_address: str
    party_b_name: str
    party_b_company: Optional[str]
    party_b_address: str
    effective_date: str
    jurisdiction: str
    term: str
    purpose: Optional[str]
    filled_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


async def get_current_user_id(request: Request) -> int:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise Exception("Not authenticated")
    user_id = get_user_from_token(token)
    if not user_id:
        raise Exception("Invalid session")
    return user_id


@router.post("/documents", response_model=NDADocumentResponse)
async def save_document(
    body: NDASaveRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user_id = await get_current_user_id(request)

    doc = NDADocument(
        user_id=user_id,
        party_a_name=body.party_a_name,
        party_a_company=body.party_a_company,
        party_a_address=body.party_a_address,
        party_b_name=body.party_b_name,
        party_b_company=body.party_b_company,
        party_b_address=body.party_b_address,
        effective_date=body.effective_date,
        jurisdiction=body.jurisdiction,
        term=body.term,
        purpose=body.purpose,
        filled_text=body.filled_text,
    )
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc


@router.get("/documents", response_model=List[NDADocumentResponse])
async def list_documents(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user_id = await get_current_user_id(request)
    result = await session.execute(
        select(NDADocument)
        .where(NDADocument.user_id == user_id)
        .order_by(NDADocument.created_at.desc())
    )
    docs = result.scalars().all()
    return docs


@router.get("/documents/{doc_id}", response_model=NDADocumentResponse)
async def get_document(
    doc_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user_id = await get_current_user_id(request)
    doc = await session.get(NDADocument, doc_id)
    if not doc or doc.user_id != user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
