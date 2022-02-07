import scrapy
import base64
from scrapy_splash import SplashRequest
import os
import shutil
import glob
# import shadow_useragent
from datetime import date, datetime, timezone
import numpy as np
# from psycopg2.extensions import register_adapter, AsIs
import uuid
from bs4 import BeautifulSoup
from ..spider_functions import *
import user_agent

class PeterParkerItem(scrapy.Item):
    output_id = scrapy.Field()
    url = scrapy.Field()
    input_id = scrapy.Field()
    response_code = scrapy.Field()
    page_content = scrapy.Field()
    scan_time = scrapy.Field()
    screenshot_dir = scrapy.Field()
    reason = scrapy.Field()
    keyword_matched = scrapy.Field()
    pass


# Handle numpy int64 conflict with psycopg2
register_adapter(np.float64, adapt_numpy_float64)
register_adapter(np.int64, adapt_numpy_int64)

# Global vars for screenshots directory
scan_date = date.today().strftime('%Y-%m-%d')
img_dir = 'screenshots/peter_parker/'

# Create directory for screenshots
try:
    screenshots_dir = "{0}".format(img_dir) + scan_date
    os.makedirs(screenshots_dir)
except FileExistsError:
    pass


class PeterParkerSpider(scrapy.Spider):
    name = 'peter_parker'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_app.pipelines.PeterParkerPipeline': 300,
        }
    }

    api_key = '9646e7b9071ea0c807e47dac6df542ba2243b6bfc42c7c431031f2a33e8e37a2'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method

        self.input_id = kwargs.get('input_id')
        super().__init__(**kwargs)

    def start_requests(self):
        # Create engine
        search_term_result = generateSearchTerm(self.input_id)
        search_term = search_term_result[0]
        keyword_logic = search_term_result[1]
        keywords_input = search_term_result[2]

        merchant_urls = generateMerchantUrls(site=search_term, api_key=self.api_key)[0:100]
        # Random user-agent
        # avoid bot

        # ua = shadow_useragent.ShadowUserAgent()
        # random_user_agent = ua.random_nomobile
        script = """function main(splash, args)
                            assert(splash:go(args.url))
                            assert(splash:wait(5))
                            splash:set_viewport_full()
                            splash:set_user_agent('"""+user_agent.generate_user_agent()+"""')
                            return {
                            html = splash:html(),
                            jpeg = splash:jpeg{scale_method='raster', quality=75,render_all=true},
                                    }
                        end"""
        for url in merchant_urls:
            meta_dict = {"keyword_logic": keyword_logic,
                         "keywords_input": keywords_input}
            yield SplashRequest(url=url, callback=self.parse
                                , endpoint='execute', args={'lua_source': script}, meta=meta_dict)

    def parse(self, response):
        # scan_datetime = datetime.now()
        # timezone = datetime.now().astimezone().tzname()
        # start_url = response.url
        # uuid_ = str(uuid.uuid4()).replace('-', '')  # genUUID(scan_datetime)
        # domain = self.domain

        scan_datetime = datetime.now(timezone.utc)
        start_url = response.url
        uuid_ = str(uuid.uuid4()).replace('-', '')
        input_id = self.input_id
        keywords_input = response.meta['keywords_input']
        keyword_logic = response.meta['keyword_logic']

        if response.status != 200:
            # Pass results to pipeline
            result = PeterParkerItem()
            result['output_id'] = uuid_
            result['url'] = start_url
            result['input_id'] = input_id
            result['page_content'] = None
            result['scan_time'] = scan_datetime
            result['response_code'] = response.status
            result['screenshot_dir'] = None
            result['reason'] = matchResponseCode(response.status)
            result['keyword_matched'] = 0
        else:
            # Take screenshot
            imgdata = base64.b64decode(response.data['jpeg'])
            filename = strip_hostname(start_url) + strip_uri_path(start_url) + '.jpeg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            file_loc = img_dir + '/' + str(scan_date) + '/' + filename

            # Clean HTML by textpipe
            text = response.body
            soup = BeautifulSoup(text)
            clean_text_lvl1 = soup.get_text()
            clean_text_lvl2 = cleanHtml(clean_text_lvl1)

            # Pass results to pipeline
            result = PeterParkerItem()
            result['output_id'] = uuid_
            result['url'] = response.url
            result['input_id'] = input_id
            result['page_content'] = clean_text_lvl2
            result['scan_time'] = scan_datetime
            result['response_code'] = response.status
            result['screenshot_dir'] = file_loc
            result['reason'] = matchReason(clean_text_lvl2)
            result['keyword_matched'] = keywordMatcher(keyword_logic, keywords_input, clean_text_lvl2)
            # Move screenshots to directory
            for img_file in glob.iglob('*.jpeg'):
                try:
                    shutil.move(img_file, os.path.join(screenshots_dir, img_file))
                except FileNotFoundError:
                    continue

        pass
        yield result

        ######################################################

        # print("THIS IS result url_id:", result['url_id'])
        # print("THIS IS result response code:", result['response_code'])
        # print("THIS IS THE result page content: ", result['page_content'])
        # print("THIS IS THE result page domain: ", result['domain'])
        # print("THIS IS THE result page screenshot: ", result['screenshot'])

        # filename = response.url.split("/")[2]  + '.txt'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
