from asgiref.sync import sync_to_async, async_to_sync
from typing import cast, List
from django.db import transaction

from card.models import Gift, Message
from user.models import User

async def create_msg(to_user_id:int, gift_id:int, msg:str = "", deco:str = "1", title:str = "", author:str = "", top:int = 0, left:int = 0):
    new_msg = await sync_to_async(sync_create_msg)(to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author, top=top, left=left)
    return cast(Message, new_msg)


@transaction.atomic
def sync_create_msg(to_user_id:int, gift_id:int, msg:str = "", deco:str = "1", title:str = "", author:str = "", top:int = 0, left:int = 0):
    new_msg = Message.objects.create(to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author, top=top, left=left)
    user = User.objects.get(id=to_user_id)
    user.msg_count += 1
    user.save()
    return new_msg


@sync_to_async
def get_msg(*args, **kwargs):
    return Message.objects.select_related("to_user", "gift").get(*args, **kwargs)


@sync_to_async
def all_list_msg():
    return list(Message.objects.select_related("to_user", "gift").all())


@sync_to_async
def filter_list_msg(*args, **kwargs):
    return list(Message.objects.select_related("to_user", "gift").filter(*args, **kwargs).distinct())


@sync_to_async
def list_to_user_msg(to_user_id):
    return list(Message.objects.select_related("to_user", "gift").filter(to_user_id=to_user_id).distinct())


async def update_msg(id:int, to_user_id:int = None, gift_id:int = None, msg:str = None, deco:str = None, title:str = None, author:str = None, top:int = None, left:int = None):
    msg1 = await get_msg(id=id)
    if to_user_id:
        msg1.to_user_id = to_user_id
    if gift_id:
        msg1.gift_id = gift_id
    if msg:
        msg1.msg = msg
    if deco:
        msg1.deco = deco
    if title:
        msg1.title = title
    if author:
        msg1.author = author
    if top:
        msg1.top = top
    if left:
        msg1.left = left    
    await sync_to_async(msg1.save)()


async def delete_msg(id):
    await sync_to_async(sync_delete_msg)(id=id)


@transaction.atomic
def sync_delete_msg(id):
    msg = async_to_sync(get_msg)(id=id)
    user = msg.to_user
    user.msg_count -= 1
    user.save()
    msg.delete()

