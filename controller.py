from base_classes import ImagesProvider, OCR

from mocks import ImagesExtractorMock, ImgToDFMock
from images_extractor import ImagesExtractor
from img_to_df import ImgToDF
import sqlite3
from string import ascii_letters
from random import choices

from sys import argv

class Controller:
    def __init__(self, images_provider  : ImagesProvider = ImagesExtractor(), ocr : OCR = ImgToDF()):
        self.images_provider = images_provider
        self.ocr = ocr

    def create_db(self):
        DB_PATH = f"./dbs/{''.join(choices(list(ascii_letters),k=7))}.db"
        conn = sqlite3.connect(DB_PATH)

        return conn, DB_PATH

    def get_db(self, url):
        input_data, format_data = self.images_provider.get_images(url)
        input_data, format_data = self.objs_to_df(input_data), self.objs_to_df(format_data,what="Format")
        format_data = {k:self.get_cols_dtype(v) for k,v in format_data.items()}
        input_data = {k:self.apply_format_to_df(v,format_data.get(k,None)) for k,v in input_data.items()}
        
        conn, db_path = self.create_db()
        for k, v in input_data.items():
            v.to_sql(k,con=conn,index=False)
        conn.close()

        return db_path
        
    def apply_format_to_df(self, df, df_format):
        if df_format:
            for k, v in df_format.items():
                if k in df:
                    if v == "String":
                        df[k] = df[k].map(lambda x: str(x) if x else None)
                    elif v == "Integer":
                        df[k] = df[k].map(lambda x: int(x) if x else None)
                    elif v == "Float":
                        df[k] = df[k].map(lambda x: float(x) if x else None)
            return df
        return df

    def objs_to_df(self, data,what="Data"):
        return {i["name"]:self.ocr.convert(i["img"],what) for i in data}

    def get_cols_dtype(self, df):
        d=df.set_index("Column").to_dict()
        return d[list(d.keys())[0]]

    

if __name__ == "__main__":
    c = Controller(ImagesExtractorMock(),ImgToDFMock())
   # db_path = c.get_db("https://www.hackerrank.com/challenges/the-company/problem")
    db_path = c.get_db(argv[1])
    print(f"DB created and stored at {db_path}")
