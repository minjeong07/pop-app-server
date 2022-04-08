import os
import shutil
import tempfile
from PIL import Image

from django.test import TestCase, override_settings, TransactionTestCase, tag
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from pop_final_project.settings import BASE_DIR, MEDIA_ROOT
from card.services.gift_service import *
from card.models import Gift, Message
from asgiref.sync import sync_to_async, async_to_sync

# 제대로 된 값, 잘못된 값, 없는값 
# CRUD - create,get,filter,update,delete
TEST_DIR = os.path.join(BASE_DIR, "test_data")

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file



@tag("gift")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestGiftService(TransactionTestCase):
    reset_sequences = True

    def test_gift_create(self):
        gift_name = "sample_name"
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        gift_desc = "sample_description"
        tags = "다이어트, 요리, 골프" 
        
        try:
            with self.assertNumQueries(36):
                new_gift = async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
                
                self.assertEqual(new_gift.gift_name, gift_name)
                self.assertEqual(new_gift.gift_img, gift_img)
                self.assertEqual(new_gift.gift_desc, gift_desc)
                db_tags = list(new_gift.tags.names())
                self.assertEqual(len(db_tags), 3)
                tags_list = list(map(lambda x: x.strip(), tags.strip().split(",")))
                self.assertEqual(sorted(db_tags), sorted(tags_list))
        finally:
            tearDownModule()

    
    def test_gift_create_with_error(self):
        gift_name = "sample_name"
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        
        try:
            with self.assertRaises(TypeError):
                async_to_sync(create_gift)(gift_name=gift_name)
            with self.assertRaises(TypeError):
                async_to_sync(create_gift)(gift_img=gift_img)
            with self.assertRaises(TypeError):
                async_to_sync(create_gift)()    
        finally:
            tearDownModule()


    def test_gift_get(self):
        gift_name = "sample_name"
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        gift_desc = "sample_description"
        tags = "다이어트"
        async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(2):
                new_gift = async_to_sync(get_gift)(id=1)
                self.assertEqual(new_gift.gift_name, gift_name)
                self.assertEqual(new_gift.gift_img, gift_img)
                self.assertEqual(new_gift.gift_desc, gift_desc)
                db_tags = list(new_gift.tags.names())
                self.assertEqual(len(db_tags), 1)
                tags_list = list(map(lambda x: x.strip(), tags.strip().split(",")))
                self.assertEqual(sorted(db_tags), sorted(tags_list))
        finally:
            tearDownModule()


    def test_gift_get_with_error(self):
        gift_name = "sample_name"
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        gift_desc = "sample_description"
        tags = "다이어트"
        async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertRaises(Gift.DoesNotExist):
                new_gift = async_to_sync(get_gift)(id = 100)
            with self.assertRaises(Gift.MultipleObjectsReturned):
                new_gift = async_to_sync(get_gift)(gift_name = gift_name)
            with self.assertRaises(Gift.MultipleObjectsReturned):
                new_gift = async_to_sync(get_gift)()
            with self.assertRaises(ValueError):
                new_gift = async_to_sync(get_gift)(id="add")
        finally:
            tearDownModule()


    def test_gift_list_all(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(5):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(1):
                gift_list = async_to_sync(all_list_gift)()
                
                self.assertEqual(5, len(gift_list))
                for i in range(5):
                    self.assertEqual(gift_list[i].gift_name, "test{}".format(str(i)))
        finally:
            tearDownModule()

    
    def test_gift_list_all_with_error(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(5):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertRaises(TypeError):
                gift_list = async_to_sync(all_list_gift)(id=1)
        finally:
            tearDownModule()


    def test_gift_list_by_filter(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(3):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        for i in range(3,7):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "골프"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(3):
                gift_list_all = async_to_sync(filter_list_gift)(tags__name__in=["다이어트", "골프"])
                gift_list_1 = async_to_sync(filter_list_gift)(tags__name__in=["다이어트"])
                gift_list_2 = async_to_sync(filter_list_gift)(tags__name="골프")
                
                self.assertEqual(7, len(gift_list_all))
                self.assertEqual(3, len(gift_list_1))
                self.assertEqual(4, len(gift_list_2))
                for i in range(3):
                    self.assertEqual(gift_list_1[i].gift_name, "test{}".format(str(i)))
        finally:
            tearDownModule()


    def test_gift_list_by_search(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(3):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        for i in range(3,7):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "골프"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(3):
                gift_list_all = async_to_sync(search_list_gift)("test")
                gift_list_1 = async_to_sync(search_list_gift)("다이어트")
                gift_list_2 = async_to_sync(search_list_gift)("골프")
                
                self.assertEqual(7, len(gift_list_all))
                self.assertEqual(3, len(gift_list_1))
                self.assertEqual(4, len(gift_list_2))
                for i in range(3):
                    self.assertEqual(gift_list_1[i].gift_name, "test{}".format(str(i)))
        finally:
            tearDownModule()


    def test_gift_update(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,4):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(30):
                async_to_sync(update_gift)(id=2, gift_name="thisissecond")
                async_to_sync(update_gift)(id=3, tags="요리, 골프")

            gift1 = async_to_sync(get_gift)(id = 1)
            gift2 = async_to_sync(get_gift)(id = 2)
            gift3 = async_to_sync(get_gift)(id = 3)
            self.assertEqual(gift1.gift_name, "test1")
            self.assertEqual(gift2.gift_name, "thisissecond")
            self.assertEqual(gift3.gift_name, "test3")
            self.assertEqual(gift1.gift_desc, "sample_description")
            self.assertEqual(gift2.gift_desc, "sample_description")
            self.assertEqual(gift3.gift_desc, "sample_description")
            db_tags = list(gift2.tags.names())
            self.assertEqual(len(db_tags), 1)
            tags_list = list(map(lambda x: x.strip(), "다이어트".strip().split(",")))
            self.assertEqual(sorted(db_tags), sorted(tags_list))
            db_tags = list(gift3.tags.names())
            self.assertEqual(len(db_tags), 2)
            tags_list = list(map(lambda x: x.strip(), "요리, 골프".strip().split(",")))
            self.assertEqual(sorted(db_tags), sorted(tags_list))
        finally:
            tearDownModule()


    def test_gift_delete(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        gift_img = test_image
        # gift_img = SimpleUploadedFile(name='logo.png', content=open("./static/img/logo.png",'rb').read(), content_type='image/png')
        for i in range(1,4):
            gift_name = "test"+str(i)
            gift_desc = "sample_description"
            tags = "다이어트"
            async_to_sync(create_gift)(gift_name=gift_name, gift_img=gift_img, gift_desc=gift_desc, tags=tags)
        
        try:
            with self.assertNumQueries(6):
                async_to_sync(delete_gift)(id=2)
                gift_list = async_to_sync(all_list_gift)()
                self.assertEqual(len(gift_list), 2)
                
        finally:
            tearDownModule()


def tearDownModule():
    # print("\n Deleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass