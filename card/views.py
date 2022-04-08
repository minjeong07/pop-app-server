from asgiref.sync import sync_to_async, async_to_sync

from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from card.services.message_service import create_msg, delete_msg, get_msg
from card.services.deco_service import all_list_deco

from card.models import Message, Gift
from user.models import User
import random

# Create your views here.
async def card_write(request:HttpRequest, id:int):
    try:
        user = await sync_to_async(get_object_or_404)(User, id=id)
        if request.method == "POST":
            to_user_id = request.POST.get("to_user_id")
            gift_id = request.POST.get("gift_id")
            msg = request.POST.get("msg")
            deco = request.POST.get("deco")
            title = request.POST.get("title")
            author = request.POST.get("author")
            top = random.randrange(0,420)
            left = random.randrange(0,300)
            # await create_msg(to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author)
            await create_msg(
                to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author, top=top, left=left)
            return JsonResponse({"server":"저장 완료!"})
        deco_list = await all_list_deco()
        return await sync_to_async(render)(request, "card/card_write.html", {"to_user_id":id, "deco_list":deco_list})
    except User.DoesNotExist:        
        raise Http404("존재하지 않는 유저입니다.")



async def card_read(request:HttpRequest, message_id:int) -> Message:
    card = await get_msg(id=message_id)
    gift = card.gift
    return await sync_to_async(render)(request, "card/card_read.html", {"card" : card, "gift":gift})


async def card_delete(request:HttpRequest, message_id:int):
    msg = await get_msg(id=message_id)
    name = msg.to_user.username
    await delete_msg(message_id)
    return redirect(f'/{name}')


def read_or_unread(request: HttpRequest, message_id:int):
    msg = async_to_sync(get_msg)(id=message_id)
    click_user = request.user
    if msg.read != 1 and click_user.id == msg.to_user_id:
        msg.read = 1
        msg.save()
    return redirect(f'/{msg.to_user.username}')