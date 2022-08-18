from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from models import User
from schemas.player_team import PlayerTeamResponse
from schemas.user import UserUpdate, UserExistsCheckResponse
from schemas.user_full import UserResponseFull, UsersListFull
from services.user import user_service

authorized_router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(dependencies.get_current_user)]
)

unauthorized_router = APIRouter(
    prefix='/user/exists',
    tags=['user existence']
)

admin_router = APIRouter(
    prefix='/admin/users',
    tags=['user administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@unauthorized_router.get('/', response_model=UserExistsCheckResponse)
def check_user_existence(email: str, provider: str, db: Session = Depends(dependencies.get_db)):
    user_model = user_service.get_by_email_and_provider(db=db, email=email, provider=provider)
    exists = True if user_model else False
    existence_model = UserExistsCheckResponse(exists=exists)
    return existence_model


@authorized_router.get('/{user_id}', response_model=UserResponseFull)
def get_user(user_id: UUID,
             db: Session = Depends(dependencies.get_db),
             current_user: User = Depends(dependencies.get_current_user)
             ):
    print(current_user.id)
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot retrieve another user's information")
    user_model = user_service.get_by_id(db, user_id)

    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find a user with that id")

    user_response = UserResponseFull(
        id=user_model.id,
        full_name=user_model.full_name,
        email=user_model.email,
        is_admin=user_model.is_admin,
        picture_url=user_model.picture_url,
        receive_notifications=user_model.receive_notifications,
        provider=user_model.provider,
        wins=user_model.wins,
        teams=[PlayerTeamResponse(**team.__dict__) for team in user_model.teams]
    )
    return user_response


@authorized_router.put('/{user_id}', response_model=UserResponseFull)
def update_user(
        user_id: UUID,
        user_update_input: UserUpdate,
        current_user: User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot retrieve another user's information")
    user_model = user_service.get_by_id(db, user_id)

    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find a user with that id")

    user_model = user_service.update_user(db, user_model, user_update_input)
    user_response = UserResponseFull(
        id=user_model.id,
        full_name=user_model.full_name,
        email=user_model.email,
        is_admin=user_model.is_admin,
        picture_url=user_model.picture_url,
        receive_notifications=user_model.receive_notifications,
        provider=user_model.provider,
        wins=user_model.wins,
        teams=[PlayerTeamResponse(**team.__dict__) for team in user_model.teams]
    )
    return user_response


@admin_router.get('/', response_model=UsersListFull)
def get_all_users(db: Session = Depends(dependencies.get_db)):
    user_models = user_service.get_all(db)
    user_responses = []
    for user_model in user_models:
        user_response = UserResponseFull(
            id=user_model.id,
            full_name=user_model.full_name,
            email=user_model.email,
            is_admin=user_model.is_admin,
            picture_url=user_model.picture_url,
            receive_notifications=user_model.receive_notifications,
            provider=user_model.provider,
            wins=user_model.wins,
            teams=[PlayerTeamResponse(**team.__dict__) for team in user_model.teams]
        )
        user_responses.append(user_response)

    users_response = UsersListFull(users=user_responses)
    return users_response






