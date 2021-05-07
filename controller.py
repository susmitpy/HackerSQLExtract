from base_classes import ImagesProvider, OCR

from images_extractor_mock import ImagesExtractorMock
from images_extractor import ImagesExtractor
from img_to_df import ImgToDF


class Controller:
    def __init__(self, images_provider  : ImagesProvider = ImagesExtractor(), ocr : OCR = ImgToDF()):
        input_data, format_data = images_provider.get_images("https://www.hackerrank.com/challenges/the-company/problem")
        


if __name__ == "__main__":
    c = Controller(ImagesExtractorMock())
