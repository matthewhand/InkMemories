"""Unit tests for image retriever."""
import logging
import pytest
import os

from common.image_retriever import ImageRetriever
from common.display_config import DisplayConfig


TEST_IMAGE_DIR = "./test-images"


@pytest.fixture()
def image_retriever():
    """TODO"""
    display_config = DisplayConfig(
        logging.getLogger(), './tests/test_display_config.json')
    yield ImageRetriever(logging.getLogger(), display_config)


class TestImageRetriever:
    """Unit test suite for the image retriever."""

    def test_image_extension_filtering(self):
        """TODO"""
        # TODO
        pass

    def test_get_all_image_paths(self, image_retriever):
        """TODO"""

        actual_images = set(image_retriever.get_path_of_all_images())

        all_files = os.listdir(TEST_IMAGE_DIR)
        expected_images = set(
            [f"{TEST_IMAGE_DIR}/{f}" for f in all_files if not os.path.isdir(f)])

        assert actual_images == expected_images

    def test_get_random_image(self, image_retriever):
        # Exercise real image decoding without GPIO / e-ink hardware.
        img = image_retriever.get_random_image()
        try:
            assert img.size[0] > 0 and img.size[1] > 0
            img.load()
        finally:
            image_retriever.clean_up_image(img)
            img.close()

    def test_get_random_images(self, image_retriever):
        images = image_retriever.get_random_images(2)
        try:
            assert len(images) == 2
            for img in images:
                assert img.size[0] > 0 and img.size[1] > 0
                img.load()
        finally:
            for img in images:
                image_retriever.clean_up_image(img)
                img.close()
