from pydantic import BaseModel


class UserForm(BaseModel):
    nome: str
    cognome: str
    username: str
    email: str
    password: str
    istituto: str | int


class LoginForm(BaseModel):
    username: str
    password: str
