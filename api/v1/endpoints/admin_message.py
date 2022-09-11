from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from models import User
from schemas.message_type import MessageTypeResponse
from schemas.user import UserResponse
from schemas.user_message import UserMessageCreate, UserMessageCreateDB, UserMessageUpdate, UserMessageResponse, UserMessageList, \
    UserMessageResponseFull
from services.user_message import user_message_service
from services.user import user_service

admin_router = APIRouter(
    prefix='/admin/user/messages',
    tags=['message administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)

authorized_router = APIRouter(
    prefix="/user",
    tags=['user messages'],
)


@admin_router.get('', response_model=UserMessageList)
def get_all_messages(db: Session = Depends(dependencies.get_db)):
    message_models = user_message_service.get_all(db)
    message_responses = []
    for message_model in message_models:
        message_type_response = MessageTypeResponse(**message_model.message_type.__dict__)
        user_response = UserResponse(**message_model.user.__dict__)
        message_response = UserMessageResponseFull(
            text=message_model.text,
            type_id=message_model.type_id,
            user_id=message_model.user_id,
            id=message_model.id,
            created_date=message_model.created_date,
            read=message_model.read,
            read_date=message_model.read_date,
            message_type=message_type_response,
            user=user_response
        )
        message_responses.append(message_response)
    messages_response = UserMessageList(messages=message_responses)
    return messages_response


@admin_router.post('', response_model=UserMessageList)
def create_message(message_create_input: UserMessageCreate, db: Session = Depends(dependencies.get_db)):
    if message_create_input.all_users:
        user_models = user_service.get_all(db)
        message_create_input.user_ids = [user_model.id for user_model in user_models]

    user_message_responses = []
    for user_id in message_create_input.user_ids:
        message_create_db_input = UserMessageCreateDB(
            text=message_create_input.text,
            type_id=message_create_input.type_id,
            user_id=user_id
        )
        message_model = user_message_service.create_message(db, message_create_db_input)
        message_type_response = MessageTypeResponse(
            **message_model.message_type.__dict__
        )
        user_response = UserResponse(**message_model.user.__dict__)
        message_response = UserMessageResponseFull(
            text=message_model.text,
            type_id=message_model.type_id,
            user_id=message_model.user_id,
            id=message_model.id,
            created_date=message_model.created_date,
            read=message_model.read,
            read_date=message_model.read_date,
            message_type=message_type_response,
            user=user_response
        )
        user_message_responses.append(message_response)

    user_messages_response = UserMessageList(messages=user_message_responses)
    return user_messages_response


@authorized_router.get('/{user_id}/messages/unread', response_model=UserMessageList)
def get_unread_messages(
        user_id: str,
        db: Session = Depends(dependencies.get_db),
        current_user = Depends(dependencies.get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot mark another users messages as read")

    message_models = user_message_service.get_unread_for_user_id(db, user_id)
    message_responses = []
    for message_model in message_models:
        message_type_response = MessageTypeResponse(
            **message_model.message_type.__dict__
        )
        user_response = UserResponse(**message_model.user.__dict__)
        message_response = UserMessageResponseFull(
            text=message_model.text,
            type_id=message_model.type_id,
            user_id=message_model.user_id,
            id=message_model.id,
            created_date=message_model.created_date,
            read=message_model.read,
            read_date=message_model.read_date,
            message_type=message_type_response,
            user=user_response
        )
        message_responses.append(message_response)
    messages_response = UserMessageList(messages=message_responses)
    return messages_response


@authorized_router.put('/{user_id}/messages/{message_id}', response_model=UserMessageResponseFull)
def update_read(
        user_id: str,
        message_id: UUID,
        user_message_update_input: UserMessageUpdate,
        current_user: User = Depends(dependencies.get_current_user),
        db: Session = Depends(dependencies.get_db)
                ):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot mark another users messages as read")

    message_model = user_message_service.get_by_id(db, message_id)
    if message_model.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Message does not belong to current user")

    if user_message_update_input.read:
        user_message_update_input.read_date = datetime.utcnow()
    else:
        user_message_update_input.read_date = None

    message_model = user_message_service.update_message(db, message_id, user_message_update_input)
    message_type_response = MessageTypeResponse(
        **message_model.message_type.__dict__
    )
    user_response = UserResponse(**message_model.user.__dict__)
    message_response = UserMessageResponseFull(
        text=message_model.text,
        type_id=message_model.type_id,
        user_id=message_model.user_id,
        id=message_model.id,
        created_date=message_model.created_date,
        read=message_model.read,
        read_date=message_model.read_date,
        message_type=message_type_response,
        user=user_response
    )
    return message_response

