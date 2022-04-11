import os
import shutil
import tempfile
from PIL import Image

from asgiref.sync import async_to_sync
from django.test import TestCase, override_settings, tag

from card.services.card_service import *
from card.services.gift_service import create_gift
from card.services.message_service import create_msg
from user.models import User
from pop_final_project.settings import BASE_DIR, MEDIA_ROOT

TEST_DIR = os.path.join(BASE_DIR, "test_data")


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

@tag("service")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestCardService(TestCase):
    def test_recommend_gift_list(self):
        pass

    
    def test_search_gift_list_service(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        async_to_sync(create_gift)(gift_name="닭가슴살", gift_img=test_image, gift_desc="gift_desc", tags="다이어트")
        async_to_sync(create_gift)(gift_name="페라리", gift_img=test_image, gift_desc="gift_desc", tags="자동차")
        async_to_sync(create_gift)(gift_name="람보르기니", gift_img=test_image, gift_desc="gift_desc", tags="자동차")
        async_to_sync(create_gift)(gift_name="와인", gift_img=test_image, gift_desc="gift_desc", tags="술")
        try:
            with self.assertNumQueries(5):
                status1, list1 = async_to_sync(search_gift_list_service)(keyword="다이어트")
                status2, list2 = async_to_sync(search_gift_list_service)(keyword="자동차")
                status3, list3 = async_to_sync(search_gift_list_service)(keyword="람보르기니")
                status4, list4 = async_to_sync(search_gift_list_service)(keyword="gift_desc")
                status5, err_msg1 = async_to_sync(search_gift_list_service)(keyword="asdasd")
                status6, err_msg2 = async_to_sync(search_gift_list_service)()
                self.assertEqual(len(list1), 1)
                self.assertEqual(len(list2), 2)
                self.assertEqual(len(list3), 1)
                self.assertEqual(len(list4), 4)
                self.assertEqual(status1, 200)
                self.assertEqual(status2, 200)
                self.assertEqual(status3, 200)
                self.assertEqual(status4, 200)
                self.assertEqual(status5, 202)
                self.assertEqual(status6, 202)
                self.assertEqual(err_msg1["err_msg"], "검색 결과가 없습니다.")
                self.assertEqual(err_msg2["err_msg"], "검색어를 입력하세요.")
        finally:
            tearDownModule()


    def test_decoration_move_service(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        User.objects.create(username="username", profile_img=test_image, email="test@email.com")
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg1", deco="deco", author="author", title="title", top=0, left=0)
        try:
            with self.assertNumQueries(7):
                new_msg = async_to_sync(get_msg)(id=1)
                self.assertEqual(new_msg.top, 0)
                self.assertEqual(new_msg.left, 0)
                status1, url1 = async_to_sync(decoration_move_service)(id=1, top=0, left=0)
                self.assertEqual(status1, 200)
                self.assertEqual(url1, {"url": "/card/read/1"})
                new_msg1 = async_to_sync(get_msg)(id=1)
                self.assertEqual(new_msg1.top, 0)
                self.assertEqual(new_msg1.left, 0)
                status2, url2 = async_to_sync(decoration_move_service)(id=1, top=100, left=100)
                self.assertEqual(status2, 204)
                self.assertEqual(url2, None)
                new_msg2 = async_to_sync(get_msg)(id=1)
                self.assertEqual(new_msg2.top, 100)
                self.assertEqual(new_msg2.left, 100)
        finally:
            tearDownModule()



def tearDownModule():
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass