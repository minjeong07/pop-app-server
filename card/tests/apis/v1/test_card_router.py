import os
import shutil
import tempfile
from urllib import response
from PIL import Image

from asgiref.sync import async_to_sync
from django.test import TestCase, override_settings, tag
from pop_final_project.settings import BASE_DIR, MEDIA_ROOT
from user.models import User
from card.services.gift_service import create_gift
from card.services.message_service import create_msg, get_msg


TEST_DIR = os.path.join(BASE_DIR, "test_data")


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file



@tag("router")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestCardRouter(TestCase):
    def test_gift_list(self):
        pass

    def test_search_gift(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        async_to_sync(create_gift)(gift_name="닭가슴살", gift_img=test_image, gift_desc="gift_desc", tags="다이어트")
        async_to_sync(create_gift)(gift_name="페라리", gift_img=test_image, gift_desc="gift_desc", tags="자동차")
        async_to_sync(create_gift)(gift_name="람보르기니", gift_img=test_image, gift_desc="gift_desc", tags="자동차")
        async_to_sync(create_gift)(gift_name="와인", gift_img=test_image, gift_desc="gift_desc", tags="술")
        
        r_wine = self.client.post(
            f"/api/v1/card/search/",
            data={"keyword": "와인"},
        )
        r_car = self.client.post(
            f"/api/v1/card/search/",
            data={"keyword": "자동차"},
        )
        r_none = self.client.post(
            f"/api/v1/card/search/",
            data={"keyword": ""},
        )
        r_aaa = self.client.post(
            f"/api/v1/card/search/",
            data={"keyword": "aaa"},
        )
        try:
            self.assertEqual(r_wine.status_code, 200)
            self.assertEqual(r_car.status_code, 200)
            self.assertEqual(r_none.status_code, 202)
            self.assertEqual(r_aaa.status_code, 202)
            self.assertEqual(len(r_wine.json()), 1)
            self.assertEqual(len(r_car.json()), 2)
            self.assertEqual(r_none.json()["err_msg"], '검색어를 입력하세요.')
            self.assertEqual(r_aaa.json()["err_msg"], '검색 결과가 없습니다.')
        finally:
            tearDownModule()


    def test_deco_move(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        User.objects.create(username="username", profile_img=test_image, email="test@email.com")
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg1", deco="deco", author="author", title="title", top=0, left=0)
        try:
            new_msg = async_to_sync(get_msg)(id=1)
            self.assertEqual(new_msg.top, 0)
            self.assertEqual(new_msg.left, 0)

            response1 = self.client.post(
                f"/api/v1/card/deco/move/",
                data={"id": 1, "top": 0, "left": 0},
            )
            self.assertEqual(response1.status_code, 200)
            self.assertEqual(response1.json()["url"], '/card/read/1')

            response2 = self.client.post(
                f"/api/v1/card/deco/move/",
                data={"id": 1, "top": 100, "left": 100},
            )
            self.assertEqual(response2.status_code, 204)

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