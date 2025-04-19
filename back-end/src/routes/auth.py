from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from ..database.connection import db_dependency
from ..database.models import User
from ..repository import users as repository_users
from ..schemas import (
    users as schema_users,
    token as schema_token
)
from ..services.auth import service_auth

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    body: schema_users.UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: db_dependency,
):
    exist_user_with_email: User = await repository_users.get_user_by_email(
        body.email, db
    )

    if exist_user_with_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {body.email} already exists",
        )

    exist_user_with_username: User = await repository_users.get_user_by_username(
        body.username, db
    )

    if exist_user_with_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with name: {body.username} already exists",
        )

    body.password = service_auth.get_password_hash(body.password)
    user = await repository_users.create_user(body, db)
    # background_tasks.add_task(
    #     service_email.send_email, user.email, user.username, request.base_url
    # )
    return {
        "user": user,
        "detail": f"User successfully created, please check your email << {user.email} >> for verification",
    }


@router.post(
    "/login",
    response_model=schema_token.TokenResponce,
    status_code=status.HTTP_202_ACCEPTED,
)
async def login(
    db: db_dependency, 
    body: OAuth2PasswordRequestForm = Depends()
):

    user = await repository_users.get_user_by_email(email=body.username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    
    banned = await repository_users.is_banned(user_id=user.user_id, db=db)
    if banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {user.email} banned. Please contact your administrator!",
        )
    
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email is not confirmed"
        )
    
    if not service_auth.verify_password(plain_password=body.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    
    access_token = await service_auth.create_access_token(data={"sub": user.email})
    refresh_token = await service_auth.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user=user, refresh_token=refresh_token, db=db)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

