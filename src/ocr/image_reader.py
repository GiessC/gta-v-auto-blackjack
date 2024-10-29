from typing import Tuple
import pytesseract
from PIL import Image


class ImageReader:
    def read_image(self, img_path: str, crop_area: Tuple[int, int, int, int]) -> str:
        img = Image.open(img_path)
        img = img.crop(crop_area)
        img.show()
        return pytesseract.image_to_string(img, config='--psm 6')