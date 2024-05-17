import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

log = logging.getLogger('FileLogger')

token_router = APIRouter(
    responses = {
        404: {
            "description": "Not found"
        }
    }
)

router = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)

# In production:
# On linux or a linux-like enviroment, regenerate this using:
# openssl rand -hex 32
# Also should put this block inside `.env` and pass it over enviroments.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$gbGdR75xExfDiGLHUTj8/.lPCxgNWkU3BhNwecacHHiBHX2qyxRBq",
        "disabled": False,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        log.info(f"User {username} tried to login but no account was found!")
        return False
    if not verify_password(password, user.hashed_password):
        log.info(f'User {username} tried to login but got the password wrong')
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exeption = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credntials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exeption
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exeption
    user = get_user(fake_users_db, username = token_data.username)
    if user is None:
        raise credentials_exeption
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        log.info(f"User {current_user.username} tried to login while inactive")
        raise HTTPException(status_code = 400, detail = "Inactive user")
    return current_user


@token_router.post("/token")
async def login_for_token_access(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 Token Login
    
    **Path**: `/token`
    
    **Method**: `POST`
    
    **Description**:
    OAuth2 compatible token login, get an access token for future requests.
    
    **Arguments**:
    - `form_data`: Form data containing the username and password.
    
    **Returns**:
    - `Token`: A token object containing the access token and token type.
    
    **Raises**:
    - `HTTPException`: If authentication fails.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        log.info(f'User {form_data.username} tried to login but failed')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta = access_token_expires
    )
    return Token(access_token = access_token, token_type = "bearer")


@router.get("/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get Current User Information
    
    **Path**: `/users/me`
    
    **Method**: `GET`
    
    **Description**:
    Retrieve the current user's information.
    
    **Arguments**:
    - `current_user`: The current active user.
    
    **Returns**:
    - `User`: The current user's information.
    """
    return current_user


@router.get("/me/items")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get Current User's Items
    
    **Path**: `/users/me/items`
    
    **Method**: `GET`
    
    **Description**:
    Retrieve items owned by the current user.
    
    **Arguments**:
    - `current_user`: The current active user.
    
    **Returns**:
    - `List[Dict]`: A list of items owned by the current user.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]
