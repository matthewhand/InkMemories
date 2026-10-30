import unittest
from common.image_processor import determine_central_crop_coordinates, central_crop

class TestImageProcessorDetermineCropCoordinates(unittest.TestCase):
    def test_determine_central_crop_coordinates_wide(self):
        expected_crop_coordinates = (250, 0, 750, 500)
        actual_crop_coordinates = determine_central_crop_coordinates(1000, 500, 1)
        self.assertEqual(expected_crop_coordinates, actual_crop_coordinates)
    
    def test_determine_central_crop_coordinates_square(self):
        expected_crop_coordinates = (0, 0, 1000, 1000)
        actual_crop_coordinates = determine_central_crop_coordinates(1000, 1000, 1)
        self.assertEqual(expected_crop_coordinates, actual_crop_coordinates)

    def test_determine_central_crop_coordinates_tall(self):
        expected_crop_coordinates = (0, 250, 500, 750)
        actual_crop_coordinates = determine_central_crop_coordinates(500, 1000, 1)
        self.assertEqual(expected_crop_coordinates, actual_crop_coordinates)

    def test_determine_central_crop_coordinates_wide_crop(self):
        expected_crop_coordinates = (0, 450, 1000, 550)
        actual_crop_coordinates = determine_central_crop_coordinates(1000, 1000, 10)
        self.assertEqual(expected_crop_coordinates, actual_crop_coordinates)


if __name__ == "__main__":
    unittest.main()


def test_pillow_exif_date_overlay():
    # Real Pillow >=13 image decoding and EXIF overlay; no Pi hardware needed.
    from io import BytesIO
    from PIL import Image
    from common.image_processor import burn_date_into_image

    photo = Image.new("RGB", (400, 240), "white")
    exif = Image.Exif()
    exif[306] = "2026:10:31 08:15:00"
    buffer = BytesIO()
    photo.save(buffer, format="JPEG", exif=exif)
    buffer.seek(0)
    with Image.open(buffer) as decoded:
        assert decoded.getexif().get(306) == "2026:10:31 08:15:00"
        overlaid = burn_date_into_image(decoded)
        assert overlaid.size == (400, 240)
