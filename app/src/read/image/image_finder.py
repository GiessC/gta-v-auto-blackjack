from typing import Tuple
import pyautogui


class Position:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

class ImageFinder:
    def find_image(self, image_path: str, confidence: float = 0.6) -> Position | None:
        try:
            loc = pyautogui.locateOnScreen(image_path, grayscale=True, confidence=confidence)
            return (int(loc.left), int(loc.top), int(loc.left) + int(loc.width), int(loc.top) + int(loc.height))
        except pyautogui.ImageNotFoundException:
            print(f'Could not find {image_path} on screen')
            return None
