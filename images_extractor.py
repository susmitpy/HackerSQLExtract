import os
from selenium import webdriver
import sys
import io
import requests
from PIL import Image
import matplotlib.pyplot as plt  

from base_classes import ImagesProvider

class ImagesExtractor(ImagesProvider):
    def __get_driver(self):
        PATH = "./chromedriver"
        user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                    "Chrome/90.0.4430.93 Safari/537.36"
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=800,800")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        return webdriver.Chrome(PATH,options=options)

    def __init__(self):
        self.brow = self.__get_driver()
        

    def get_images(self, url):
        self.brow.get(url)
        elem = self.brow.find_element_by_class_name("ui-icon-cross")
        elem.click()
        sample_input_data = self.__get_name_img("challenge_sample_input")
        input_format_data = self.__get_name_img("challenge_input_format")

        for obj in sample_input_data:
            obj["img"].save(f"./images/input/{obj['name']}.png", "PNG")

        for obj in input_format_data:
            obj["img"].save(f"./images/format/{obj['name']}.png", "PNG")

        return (sample_input_data, input_format_data)

    def __get_name_img(self, class_name):
        sample_input = self.brow.find_element_by_class_name(class_name)
        table_names = [i.text for i in sample_input.find_elements_by_tag_name("em")]
        images = [i.get_attribute("src") for i in sample_input.find_elements_by_tag_name("img")]
        sample_input_data = [] # [ {"name":"table name", "img" : PIL.Image} ]
    
        table_name_idx = 0
        for image in images:
            data = requests.get(image).content
            obj, table_name_idx = self.process_img_data(data, table_name_idx,table_names)
            sample_input_data.append(obj)

        return sample_input_data
    
    def process_img_data(self,img,table_name_idx,table_names):
        img = Image.open(io.BytesIO(img)) 
        for i in range(table_name_idx,len(table_names)):
            table_name = table_names[i]
            if table_name[-1] == ":":
                table_name = table_name[:-1]
            table_name_idx += 1
            if table_name.istitle():
                break

        obj = {"name":table_name, "img":img}
        return obj, table_name_idx

if __name__ == '__main__':
    IE = ImagesExtractor()
    IE.get_images("https://www.hackerrank.com/challenges/the-company/problem")