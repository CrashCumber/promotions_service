from typing import Optional, List, Union

from pydantic import BaseModel


class PromoSchemaRequest(BaseModel):
    name: str
    description: Optional[str] = None


class PromoSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class PrizeSchema(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


class PrizeSchemaRequest(BaseModel):
    description: str


class ParticipantSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ParticipantSchemaRequest(BaseModel):
    name: str


class PromoSchemaFull(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    prizes: List[PrizeSchema]
    participants: List[ParticipantSchema]

    class Config:
        orm_mode = True


class PromoSchemaModify(BaseModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
