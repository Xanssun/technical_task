from http import HTTPStatus
from typing import Annotated

from core.tokens import security_refresh_token
from fastapi import APIRouter, Depends, HTTPException, Response
from models.entity import RefreshToken
from schemas.entity import Result, UserCreate, UserInDB, UserSignIn
from services.auth import AuthService, get_auth_service

router = APIRouter()


@router.post(
    '/register',
    response_model=UserInDB,
    status_code=HTTPStatus.CREATED,
    summary='Регистрация пользователя',
    description='Регистрация пользователя',
)
async def singup(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.signup(user_create)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Already exists user with such username',
        )
    return user

@router.post(
    '/login',
    response_model=UserInDB,
    status_code=HTTPStatus.CREATED,
    summary='Вход пользователя',
    description='Вход пользователя',
)
async def signin(
    response: Response,
    user_signin: UserSignIn,
    auth_service: AuthService = Depends(get_auth_service),
):
    tokens = await auth_service.signin(user_signin, check_pass=True)
    if not tokens:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Invalid username or password',
        )
    response.headers['X-Access-Token'] = tokens['token']
    response.headers['X-Refresh-Token'] = tokens['refresh_token']

    return tokens['user']


@router.post(
    '/refresh',
    response_model=UserInDB,
    status_code=HTTPStatus.OK,
    summary='Обновить токен',
    description='Обновить токен',
)
async def refresh_token(
    response: Response,
    refresh_token: Annotated[RefreshToken, Depends(security_refresh_token)],
    auth_service: AuthService = Depends(get_auth_service),
):
    tokens = await auth_service.refresh_token(refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Unauthorized',
        )
    response.headers['X-Access-Token'] = tokens['token']
    response.headers['X-Refresh-Token'] = tokens['refresh_token']

    return tokens['user']


@router.post(
    '/logout',
    response_model=Result,
    status_code=HTTPStatus.OK,
    summary='Выход',
    description='Выход',
)
async def logout(
    refresh_token: Annotated[RefreshToken, Depends(security_refresh_token)],
    auth_service: AuthService = Depends(get_auth_service),
) -> Result:
    result = await auth_service.logout(refresh_token=refresh_token)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Токен аннулирован"
        )
    return Result(success=False)
