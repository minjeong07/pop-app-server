from typing import Any, List, Optional
from ninja import Schema
from asgiref.sync import sync_to_async


class CardResponse(Schema):
    id: int
    gift_name: str
    gift_desc: str
    gift_img: str
    # gift_tags: List[str]


class ErrorMessage(Schema):
    err_msg: str


class RedirectUrl(Schema):
    url: str