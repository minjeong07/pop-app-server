import os
import shutil
import tempfile
from PIL import Image

from django.test import override_settings, TransactionTestCase, tag

from pop_final_project.settings import BASE_DIR, MEDIA_ROOT
from card.services.deco_service import *
from card.models import Gift, Message, Decoration
from asgiref.sync import sync_to_async, async_to_sync


TEST_DIR = os.path.join(BASE_DIR, "test_data")


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file



@tag("deco")
@override_settings(MEDIA_ROOT = (TEST_DIR + '/media'))
class TestDecorationService(TransactionTestCase):
    reset_sequences = True

    def test_create_deco(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        deco_name = "test_deco"
        deco_img = test_image
        try:
            with self.assertNumQueries(1):
                new_deco = async_to_sync(create_deco)(deco_name=deco_name, deco_img=deco_img)
                self.assertEqual(new_deco.deco_name, deco_name)
                self.assertEqual(new_deco.deco_img, deco_img)
                
        finally:
            tearDownModule()

    def test_get_deco(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        deco_img = test_image
        async_to_sync(create_deco)(deco_name="test_deco1", deco_img=deco_img)
        async_to_sync(create_deco)(deco_name="test_deco2", deco_img=deco_img)
        try:
            with self.assertNumQueries(2):
                new_deco1 = async_to_sync(get_deco)(id=1)
                new_deco2 = async_to_sync(get_deco)(id=2)
                self.assertEqual(new_deco1.deco_name, "test_deco1")
                self.assertEqual(new_deco1.deco_img, deco_img)
                self.assertEqual(new_deco2.deco_name, "test_deco2")
                self.assertEqual(new_deco2.deco_img, deco_img)
                
        finally:
            tearDownModule()

            
    def test_all_list_deco(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        deco_img = test_image
        async_to_sync(create_deco)(deco_name="test_deco1", deco_img=deco_img)
        async_to_sync(create_deco)(deco_name="test_deco2", deco_img=deco_img)
        try:
            with self.assertNumQueries(1):
                new_deco_list = async_to_sync(all_list_deco)()
                self.assertEqual(new_deco_list[0].deco_name, "test_deco1")
                self.assertEqual(new_deco_list[0].deco_img, deco_img)
                self.assertEqual(new_deco_list[1].deco_name, "test_deco2")
                self.assertEqual(new_deco_list[1].deco_img, deco_img)
                self.assertEqual(len(new_deco_list), 2)
                
        finally:
            tearDownModule()


    def test_delete_deco(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file).name
        deco_img = test_image
        async_to_sync(create_deco)(deco_name="test_deco1", deco_img=deco_img)
        async_to_sync(create_deco)(deco_name="test_deco2", deco_img=deco_img)
        async_to_sync(create_deco)(deco_name="test_deco3", deco_img=deco_img)
        async_to_sync(create_deco)(deco_name="test_deco4", deco_img=deco_img)
        try:
            with self.assertNumQueries(9):
                new_deco_list1 = async_to_sync(all_list_deco)()
                self.assertEqual(len(new_deco_list1), 4)
                async_to_sync(delete_deco)(id=1)
                new_deco_list2 = async_to_sync(all_list_deco)()
                self.assertEqual(len(new_deco_list2), 3)
                async_to_sync(delete_deco)(id=2)
                async_to_sync(delete_deco)(id=4)
                new_deco_list3 = async_to_sync(all_list_deco)()
                self.assertEqual(len(new_deco_list3), 1)
                
        finally:
            tearDownModule()


def tearDownModule():
    # print("\n Deleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
