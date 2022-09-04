from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import dependencies
from schemas.message_type import MessageTypeList, MessageTypeResponse, MessageTypeCreate, MessageTypeUpdate
from services.message_type import message_type_service

admin_router = APIRouter(
    prefix='/admin/message_types',
    tags=['message type administration'],
    dependencies=[Depends(dependencies.get_admin_user)]
)


@admin_router.get('', response_model=MessageTypeList)
def get_all(db: Session = Depends(dependencies.get_db)):
    message_type_models = message_type_service.get_all(db)
    message_type_responses = []
    for message_type_model in message_type_models:
        message_type_response = MessageTypeResponse(**message_type_model.__dict__)
        message_type_responses.append(message_type_response)

    message_types_response = MessageTypeList(message_types=message_type_responses)
    return message_types_response


@admin_router.post('', response_model=MessageTypeResponse)
def create_message_type(message_type_create_input: MessageTypeCreate, db: Session = Depends(dependencies.get_db)):
    message_type_model = message_type_service.create(db, message_type_create_input)
    message_type_response = MessageTypeResponse(**message_type_model.__dict__)
    return message_type_response


@admin_router.put('/{message_type_id}', response_model=MessageTypeResponse)
def update_message_type(message_type_id: UUID, message_type_update_input: MessageTypeUpdate, db: Session = Depends(dependencies.get_db)):
    message_type_model = message_type_service.update(db, message_type_id, message_type_update_input)
    message_type_response = MessageTypeResponse(**message_type_model.__dict__)
    return message_type_response







# NOT CURRENTLY IN USE