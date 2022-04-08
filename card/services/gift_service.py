from typing import cast, List

from django.db.models import Q
from card.models import Gift, Message
from asgiref.sync import sync_to_async


@sync_to_async
def create_gift(gift_name, gift_img, gift_desc="", tags=None):
    result = Gift.objects.create(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc)
    if tags:
        tag_slugs_list = list(map(lambda x: x.strip(), tags.strip().split(",")))
        result.tags.add(*tag_slugs_list)
        result.save()
    return result

@sync_to_async
def get_gift(*args, **kwargs):
    return Gift.objects.get(*args, **kwargs)


@sync_to_async
def all_list_gift():
    return list(Gift.objects.all())


@sync_to_async
def filter_list_gift(*args, **kwargs):
    return list(Gift.objects.filter(*args, **kwargs).distinct())


@sync_to_async
def search_list_gift(keyword):
    return list(Gift.objects.filter(Q(gift_name__icontains=keyword) | Q(gift_desc__icontains=keyword) | Q(tags__name=keyword)).distinct())

@sync_to_async
def search_list_coupon(array):
    res = []
    for i in array:
        res.append(Gift.objects.get(gift_desc=str(i)))
    return res

async def update_gift(id, gift_name = None, gift_img = None, gift_desc = None, tags = None):
    gift = await get_gift(id=id)
    if gift_name:
        gift.gift_name = gift_name
    if gift_img:
        gift.gift_img = gift_img
    if gift_desc:
        gift.gift_desc = gift_desc
    if tags:
        tag_slugs_list = list(map(lambda x: x.strip(), tags.strip().split(",")))
        await sync_to_async(gift.tags.clear)()        
        await sync_to_async(gift.tags.add)(*tag_slugs_list)
    await sync_to_async(gift.save)()


async def delete_gift(id):
    gift = await get_gift(id=id)
    await sync_to_async(gift.delete)()

