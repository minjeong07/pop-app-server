from random import shuffle
from django.shortcuts import redirect
from card.models import Gift, Message
from user.models import User
from .gift_service import all_list_gift, search_list_gift, filter_list_gift, search_list_coupon
from .message_service import update_msg, get_msg
from asgiref.sync import sync_to_async
import httpx


async def use_api_reco(msg:str):
    data = {"msg": msg}
    url = "http://3.37.15.2:8000/api/v1/"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, data=data, timeout=None)
        jsondata = r.json()
        tag = jsondata["tag"]
        array = jsondata["index"]
        return tag, array


async def recommend_gift_list(id: int, msg: str = ""):
    # 메시지 분석 후 추천 부분
    msg_response, index_array = await use_api_reco(msg)
    msg_request = await search_list_coupon(index_array)

    # 유저 선호 태그 리스트
    user_tag = []
    user = await sync_to_async(User.objects.get)(id=id)
    tag_list = await sync_to_async(list)(user.tag.names())
    if tag_list:
        for tag in tag_list:
            tag_result = await search_list_gift(tag)
            tag_result = tag_result[:10]
            user_tag += tag_result
        shuffle(user_tag)
        user_tag = user_tag[:8]
    return msg_request + user_tag


async def search_gift_list_service(keyword: str = None):
    if not keyword:
        return 202, {"err_msg": "검색어를 입력하세요."}
    else:
        glist = await search_list_gift(keyword)
        if glist:
            if len(glist) > 10:
                glist = glist[-10:]
            glist.reverse()
            return 200, glist
        else:
            return 202, {"err_msg": "검색 결과가 없습니다."}


async def decoration_move_service(id: int, top: int, left: int):
    msg1 = await get_msg(id=id)
    if msg1.top == top and msg1.left == left:
        return 200, {"url": f"/card/read/{id}"}
    else:
        await update_msg(id=id, top=top, left=left)
        return 204, None