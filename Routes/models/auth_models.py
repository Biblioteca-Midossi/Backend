import typing
from datetime import datetime
from fastapi import Response
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserProfileUpdate(BaseModel):
    nome: Optional[str]
    cognome: Optional[str]
    email: Optional[EmailStr]
    bio: Optional[str]
    istituto: Optional[int]


class UserProfile(BaseModel):
    id_utente: int
    username: str
    email: EmailStr
    nome: str
    cognome: str
    istituto: str
    ruolo: str
    bio: Optional[str] = None
    profle_picture: Optional[str] = None
    last_login: Optional[datetime] = None


class UserForm(BaseModel):
    nome: str
    cognome: str
    username: str
    email: EmailStr
    password: str
    istituto: str | int


class LoginForm(BaseModel):
    username: str
    password: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(Response):
    def init_headers(self, headers: typing.Mapping[str, str] | None = None) -> None:
        super().init_headers()
        self.scope = {'response': self}
