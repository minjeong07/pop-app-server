from typing import cast, List

from card.models import Gift, Message, Decoration
from asgiref.sync import sync_to_async

async def create_deco(deco_name, deco_img):
    result = await sync_to_async(Decoration.objects.create)(deco_name=deco_name, deco_img=deco_img)
    return cast(Decoration, result)

@sync_to_async
def get_deco(*args, **kwargs):
    return Decoration.objects.get(*args, **kwargs)


@sync_to_async
def all_list_deco():
    return list(Decoration.objects.all())


async def delete_deco(id):
    msg = await get_deco(id=id)
    await sync_to_async(msg.delete)()