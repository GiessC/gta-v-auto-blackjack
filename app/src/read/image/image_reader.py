from typing import Tuple
import numpy as np
import pytesseract
import cv2
from PIL import Image

from read.settings.ocr_settings import OCRSettings


class ImageReader:
    settings: OCRSettings

    def __init__(self, settings: OCRSettings):
        self.settings = settings

    def debug_image(self, img, img_name: str = 'image'):
        if self.settings.debug:
            cv2.imshow(img_name, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows

    def crop_image(self, img, crop_area: Tuple[int, int, int, int]):
        cropped = img[crop_area[1]:crop_area[3], crop_area[0]:crop_area[2]]

        self.debug_image(cropped, 'cropped')

        return cropped

    def convert_image_to_grayscale(self, img):
        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        self.debug_image(grayscale, 'grayscale')

        return grayscale

    def apply_thresholding(self, grayscale_img):
        adaptive_thresh = cv2.adaptiveThreshold(
            grayscale_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        self.debug_image(adaptive_thresh, 'adaptive thresholding')

        return adaptive_thresh

    def add_dilation_and_erosion(self, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        processed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        self.debug_image(processed, 'morphological transformation')

        return processed

    def read_image(self, img_path: str):
        return cv2.imread(img_path)

    def read_int_from_image(self, image: Image) -> int:
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        img = self.convert_image_to_grayscale(img)
        img = self.add_dilation_and_erosion(img)
        img = self.apply_thresholding(img)

        text = pytesseract.image_to_string(img, lang='eng', config='--psm 6 -c tessedit_char_whitelist=0123456789')

        try:
            return int(text)
        except ValueError:
            return 0
