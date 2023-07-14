from pydantic import BaseModel


class TuneModel(BaseModel):
    class Config:
        orm_mode = True
