from typing import Tuple
import pyautogui


class ImageFinder:
    def find_image(self, image_path: str, confidence: float = 0.6) -> Tuple[int, int, int, int] | None:
        try:
            loc = pyautogui.locateOnScreen(image_path, grayscale=True, confidence=confidence)
            return (int(loc.left), int(loc.top), int(loc.left) + int(loc.width), int(loc.top) + int(loc.height))
        except pyautogui.ImageNotFoundException:
            print(f'Could not find {image_path} on screen')
            return None
