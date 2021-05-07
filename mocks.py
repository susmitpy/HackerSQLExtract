from base_classes import ImagesProvider, OCR

import os
from PIL import Image
import pandas as pd

class ImagesExtractorMock(ImagesProvider):
    def get_images(self, url):
        input_data = []
        input_data_path = "./images/input/"
        for file in os.listdir(input_data_path):
            name = file.split(".")[0]
            img = Image.open(input_data_path + file)
            obj = {"name" : name, "img":img}
            input_data.append(obj)

        format_data = []
        format_data_path = "./images/format/"
        for file in os.listdir(format_data_path):
            name = file.split(".")[0]
            img = Image.open(format_data_path + file)
            obj = {"name" : name, "img":img}
            format_data.append(obj)
        
        return input_data, format_data

class ImgToDFMock(OCR):
    def convert(self, img, what="Data"):
        if what == "Data":
            return (
                pd.DataFrame({
                    "lead_manager_code" : ["LM1", "LM2"],
                    "company_code" : ["1", "2"]
                })
            )
        return (
            pd.DataFrame({
                "Column" : ["lead_manager_code", "company_code"],
                "Type" : ["String", "Integer"]
            })
        )