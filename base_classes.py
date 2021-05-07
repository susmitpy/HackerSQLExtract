from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple
from PIL import Image
from pandas import DataFrame

class ImagesProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_images(self, url : str) -> Tuple[List[Dict[str,object]],List[Dict[str,object]]]:
        pass

class OCR(metaclass=ABCMeta):
    @abstractmethod
    def convert(self, img : Image) -> DataFrame:
        pass