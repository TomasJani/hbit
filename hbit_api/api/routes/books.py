from typing import Any

import svcs
from fastapi import APIRouter
from starlette import status

from hbit_api.api import deps
from hbit_api.domain import commands

router = APIRouter()


@router.post("/")
def create_book(
    *,
    services: svcs.fastapi.DepContainer,
    current_user: deps.CurrentUser,
    create_book: commands.CreateBook,
) -> Any:
    """
    Create new book.
    """
    bus = services.get(deps.MessageBusDep)
    bus.handle(message=create_book)
    return status.HTTP_200_OK
