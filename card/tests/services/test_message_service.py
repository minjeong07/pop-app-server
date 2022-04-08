import os
import shutil
import tempfile
from PIL import Image

from django.test import TestCase, override_settings, TransactionTestCase, tag
from django.core.files.uploadedfile import SimpleUploadedFile,UploadedFile
from asgiref.sync import sync_to_async, async_to_sync

from card.services.message_service import *
from card.services.gift_service import create_gift
from user.models import User
from card.models import Gift, Message
from pop_final_project.settings import BASE_DIR, MEDIA_ROOT

# CRUD - create,get,filter,update,delete
TEST_DIR = os.path.join(BASE_DIR, "test_data")

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file


@tag("message", "msg")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestMessageService(TransactionTestCase):
    reset_sequences = True

    def test_create_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        user1 = User.objects.create(username="username2", profile_img=test_image, email="test2@email.com")
        gift1 = async_to_sync(create_gift)(gift_name="gift_name", gift_img=test_image, gift_desc="gift_desc", tags="다이어트")
        to_user_id = user1.id
        gift_id = gift1.id
        msg = "test_msg"
        deco = "1"
        title = "title"
        author = "author"
        top = 0
        left = 0
        try:
            with self.assertNumQueries(6):
                new_message = async_to_sync(create_msg)(to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author, top=top, left=left)
                self.assertEqual(new_message.to_user, user1)
                self.assertEqual(new_message.gift, gift1)
                self.assertEqual(new_message.msg, msg)
                self.assertEqual(new_message.deco, deco)            
        
        finally:
            tearDownModule()


    def test_get_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        user1 = User.objects.create(username="username2", profile_img=test_image, email="test2@email.com")
        gift1 = async_to_sync(create_gift)(gift_name="gift_name", gift_img=test_image, gift_desc="gift_desc", tags="다이어트")
        to_user_id = user1.id
        gift_id = gift1.id
        msg = "test_msg"
        deco = "1"
        title = "title"
        author = "author"
        top = 0
        left = 0
        new_message = async_to_sync(create_msg)(to_user_id=to_user_id, gift_id=gift_id, msg=msg, deco=deco, title=title, author=author, top=top, left=left)

        try:
            with self.assertNumQueries(1):
                new_message = async_to_sync(get_msg)(id = 1)
                self.assertEqual(new_message.to_user, user1)
                self.assertEqual(new_message.gift, gift1)
                self.assertEqual(new_message.msg, msg)
                self.assertEqual(new_message.deco, deco)            
                self.assertEqual(new_message.title, title)            
                self.assertEqual(new_message.author, author)            
                
        finally:
            tearDownModule()


    def test_all_list_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,6):
            User.objects.create(username="username{}".format(i), profile_img=test_image, email="test{}@email.com".format(i))
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        for i in range(2,6):
            async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")
        
        try:
            with self.assertNumQueries(1):
                msg_list = async_to_sync(all_list_msg)()
                self.assertEqual(len(msg_list), 4)
                self.assertEqual(msg_list[3].author, "author5")
                self.assertEqual(msg_list[3].msg, "msg5")
        finally:
            tearDownModule()


    def test_filter_list_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,6):
            User.objects.create(username="username{}".format(i), profile_img=test_image, email="test{}@email.com".format(i))
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_gift)(gift_name="gift_name2", gift_img=test_image, gift_desc="gift_desc2", tags="골프")
        for i in range(2,6):
            async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")
        for i in range(1,4):
            async_to_sync(create_msg)(to_user_id=5, gift_id=2, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")

        try:
            with self.assertNumQueries(2):
                msg_list1 = async_to_sync(filter_list_msg)(to_user_id=1)
                msg_list2 = async_to_sync(filter_list_msg)(gift_id=2)
                self.assertEqual(len(msg_list1), 4)
                self.assertEqual(msg_list1[3].author, "author5")
                self.assertEqual(msg_list1[3].msg, "msg5")
                self.assertEqual(len(msg_list2), 3)
                self.assertEqual(msg_list2[1].author, "author2")
                self.assertEqual(msg_list2[1].msg, "msg2")
        finally:
            tearDownModule()


    def test_list_to_user_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,6):
            User.objects.create(username="username{}".format(i), profile_img=test_image, email="test{}@email.com".format(i))
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_gift)(gift_name="gift_name2", gift_img=test_image, gift_desc="gift_desc2", tags="골프")
        for i in range(2,6):
            async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")
        for i in range(1,4):
            async_to_sync(create_msg)(to_user_id=5, gift_id=2, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")

        try:
            with self.assertNumQueries(2):
                msg_list1 = async_to_sync(list_to_user_msg)(1)
                msg_list2 = async_to_sync(list_to_user_msg)(5)
                self.assertEqual(len(msg_list1), 4)
                self.assertEqual(msg_list1[3].author, "author5")
                self.assertEqual(msg_list1[3].msg, "msg5")
                self.assertEqual(len(msg_list2), 3)
                self.assertEqual(msg_list2[1].author, "author2")
                self.assertEqual(msg_list2[1].msg, "msg2")
        finally:
            tearDownModule()


    def test_update_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,6):
            User.objects.create(username="username{}".format(i), profile_img=test_image, email="test{}@email.com".format(i))
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_gift)(gift_name="gift_name2", gift_img=test_image, gift_desc="gift_desc2", tags="골프")
        for i in range(2,6):
            async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")
        for i in range(1,4):
            async_to_sync(create_msg)(to_user_id=5, gift_id=2, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")

        try:
            with self.assertNumQueries(4):
                before_msg = async_to_sync(get_msg)(id=2)
                async_to_sync(update_msg)(id=2, to_user_id=3, gift_id=2, msg="changed", deco="deco3", author="author1", title="title1", top=50, left=50)
                after_msg = async_to_sync(get_msg)(id=2)
                self.assertEqual(before_msg, after_msg)
                self.assertEqual(before_msg.author, "author3")
                self.assertEqual(after_msg.author, "author1")
                self.assertNotEqual(before_msg.to_user_id, after_msg.to_user_id)
                self.assertNotEqual(before_msg.gift_id, after_msg.gift_id)
                self.assertNotEqual(before_msg.msg, after_msg.msg)
                self.assertNotEqual(before_msg.deco, after_msg.deco)
                self.assertNotEqual(before_msg.author, after_msg.author)
                self.assertNotEqual(before_msg.title, after_msg.title)
                self.assertNotEqual(before_msg.top, after_msg.top)
                self.assertNotEqual(before_msg.left, after_msg.left)
        finally:
            tearDownModule()


    def test_delete_msg(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        # test_image = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,6):
            User.objects.create(username="username{}".format(i), profile_img=test_image, email="test{}@email.com".format(i))
        async_to_sync(create_gift)(gift_name="gift_name1", gift_img=test_image, gift_desc="gift_desc1", tags="다이어트")
        async_to_sync(create_gift)(gift_name="gift_name2", gift_img=test_image, gift_desc="gift_desc2", tags="골프")
        for i in range(2,6):
            async_to_sync(create_msg)(to_user_id=1, gift_id=1, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")
        for i in range(1,4):
            async_to_sync(create_msg)(to_user_id=5, gift_id=2, msg="msg{}".format(i), deco="deco", author=f"author{i}", title=f"title{i}")

        try:
            with self.assertNumQueries(6):
                list1 = async_to_sync(all_list_msg)()
                self.assertEqual(len(list1), 7)
                async_to_sync(delete_msg)(id=1)
                list2 = async_to_sync(all_list_msg)()
                self.assertEqual(len(list2), 6)
        finally:
            tearDownModule()


def tearDownModule():
    # print("\n Deleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass