# from scrapy.utils.project import get_project_settings
import pymysql
from .settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
import numpy as np


class PeterParkerPipeline(object):
    def __init__(self):
        # Call DB settings from settings.py
        # settings = get_project_settings()
        # db = settings.get('SF_MYSQL')
        self.connection = pymysql.connect(host=DB_HOST,
                                          user=DB_USER,
                                          password=DB_PASS,
                                          database=DB_NAME,
                                          port=int(DB_PORT),
                                          charset='utf8mb4')
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """insert into main_outputpeter(output_id, input_id, url, page_content, response_code, scan_time, screenshot_dir,reason,keyword_matched) 
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (item['output_id'],
             item['input_id'],
             item['url'],
             item['page_content'],
             item['response_code'],
             item['scan_time'].strftime('%Y-%m-%d %H:%M:%S'),
             item['screenshot_dir'],
             item['reason'],
             item['keyword_matched']))
        self.connection.commit()

        return item


class MaryJanesPipeline(object):
    def __init__(self):
        # Call DB settings from settings.py
        # settings = get_project_settings()
        # db = settings.get('SF_MYSQL')
        pymysql.converters.encoders[np.int64] = pymysql.converters.escape_int
        pymysql.converters.conversions = pymysql.converters.encoders.copy()
        pymysql.converters.conversions.update(pymysql.converters.decoders)

        self.connection = pymysql.connect(host=DB_HOST,
                                          user=DB_USER,
                                          password=DB_PASS,
                                          database=DB_NAME,
                                          port=int(DB_PORT),
                                          charset='utf8mb4')
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """insert into main_outputmary(output_id,url, scan_time, response_code, screenshot_dir,
             merchant_url, page_content, input_id, merchant_id, merchant_name,pw_product, project_id, project_name,reason,scheduled_counter,keyword_matched) 
             values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (item['output_id'],
             item['url'],
             item['scan_time'].strftime('%Y-%m-%d %H:%M:%S'),
             item['response_code'],
             item['screenshot_dir'],
             item['merchant_url'],
             item['page_content'],
             item['input_id'],
             item['merchant_id'],
             item['merchant_name'],
             item['pw_product'],
             item['project_id'],
             item['project_name'],
             item['reason'],
             item['scheduled_counter'],
             item['keyword_matched']
             ))
        self.connection.commit()

        return item
