from pydantic import BaseModel


class RecordCreate(BaseModel):
    location: str
    startDate: str
    endDate: str


class RecordUpdate(BaseModel):
    location: str | None = None
    startDate: str | None = None
    endDate: str | None = None
