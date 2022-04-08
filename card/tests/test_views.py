import os
import shutil
import tempfile
from PIL import Image

from django.test import override_settings, tag, TransactionTestCase

from pop_final_project.settings import BASE_DIR, MEDIA_ROOT
from card.services.message_service import get_msg, all_list_msg
from card.services.gift_service import create_gift
from card.models import Gift, Message, Decoration
from user.models import User
from asgiref.sync import sync_to_async, async_to_sync

# view get,post,etc 정상작동 확인 

TEST_DIR = os.path.join(BASE_DIR, "test_data")


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

@tag("view")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestCardView(TransactionTestCase):
    reset_sequences = True

    def test_GET_No_User_card_write(self):
        response = self.client.get('/card/write/1')
        self.assertEqual(response.status_code, 404)


    def test_GET_No_id_card_write(self):
        response = self.client.get('/card/write/')
        self.assertEqual(response.status_code, 404)


    def test_GET_card_write(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        user1 = User.objects.create(username="username1", profile_img=test_image, email="test1@email.com")
        response = self.client.get(f"/card/write/{user1.id}")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "장식 선택하기")
            self.assertContains(response, "메시지 쓰기")
            self.assertContains(response, "선물 고르기")
            self.assertContains(response, "완성 페이지")
        finally:
            tearDownModule()


    def test_POST_card_write(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        user1 = User.objects.create(username="username1", profile_img=test_image, email="test1@email.com")
        gift1 = async_to_sync(create_gift)(gift_name="gift_name", gift_img=test_image, gift_desc="gift_desc", tags="다이어트")
        m_list1 = async_to_sync(all_list_msg)()
        self.assertEqual(len(m_list1), 0)
        response = self.client.post(
            f"/card/write/{user1.id}",
            data={
                "to_user_id" : user1.id,
                "gift_id" : gift1.id,
                "msg" : "this is test msg",
                "deco" : "deco_url", 
                "title" : "test_title",
                "author" : "tester"
            },
        )
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["server"], "저장 완료!")
            m_list2 = async_to_sync(all_list_msg)()
            self.assertEqual(len(m_list2), 1)
            new_msg = async_to_sync(get_msg)(id = 1)
            self.assertEqual(new_msg.to_user_id, user1.id)
            self.assertEqual(new_msg.gift_id, gift1.id)
            self.assertEqual(new_msg.msg, "this is test msg")
            self.assertEqual(new_msg.deco, "deco_url")            
            self.assertEqual(new_msg.title, "test_title")            
            self.assertEqual(new_msg.author, "tester")            
            
        finally:
            tearDownModule()



    def test_Wrong_card_write(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        user1 = User.objects.create(username="username1", profile_img=test_image, email="test1@email.com")
        response = self.client.get(f"/card/write/{user1.id + 100}")
        try:
            self.assertEqual(response.status_code, 404)
        finally:
            tearDownModule()



def tearDownModule():
    # print("\n Deleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass