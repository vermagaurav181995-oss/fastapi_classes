from pydantic import BaseModel


class UserCreate(BaseModel):
    pass


class UserOut(BaseModel):
    pass


class Token(BaseModel):
    pass


class NoteCreate(BaseModel):
    pass


class NoteUpdate(BaseModel):
    pass


class NoteOut(BaseModel):
    pass
