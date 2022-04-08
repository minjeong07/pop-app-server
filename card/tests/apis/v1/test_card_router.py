import os
import shutil
import tempfile
from PIL import Image

from django.test import TestCase, override_settings, tag
from pop_final_project.settings import BASE_DIR, MEDIA_ROOT



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
        pass

    def test_deco_move(self):
        pass



def tearDownModule():
    # print("\n Deleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
