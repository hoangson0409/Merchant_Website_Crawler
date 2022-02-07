import scrapy
# import pandas as pd
import base64
from scrapy_splash import SplashRequest
import os
import shutil
import glob
# import shadow_useragent
from datetime import date, datetime, timezone
import numpy as np
import uuid
from bs4 import BeautifulSoup
from ..spider_functions import *
import user_agent

class MaryJanesItem(scrapy.Item):
    output_id = scrapy.Field()
    url = scrapy.Field()
    scan_time = scrapy.Field()
    response_code = scrapy.Field()
    screenshot_dir = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant_name = scrapy.Field()
    project_id = scrapy.Field()
    project_name = scrapy.Field()
    pw_product = scrapy.Field()
    merchant_url = scrapy.Field()
    page_content = scrapy.Field()
    input_id = scrapy.Field()
    reason = scrapy.Field()
    scheduled_counter = scrapy.Field()
    keyword_matched = scrapy.Field()
    pass


register_adapter(np.float64, adapt_numpy_float64)
register_adapter(np.int64, adapt_numpy_int64)

# Global vars for screenshots directory
scan_date = date.today().strftime('%Y-%m-%d')
img_dir = 'screenshots/mary_janes/'

# Create directory for screenshots
try:
    screenshots_dir = "{0}".format(img_dir) + scan_date
    os.makedirs(screenshots_dir)
except FileExistsError:
    pass


class MaryJanesSpider(scrapy.Spider):
    name = 'mary_janes'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_app.pipelines.MaryJanesPipeline': 300,
        }
    }
    #97b7218f612297fbedf58e2f0b94c2b6e0d3a89df602023eb5edc3a13766d3a7
    api_key = '9646e7b9071ea0c807e47dac6df542ba2243b6bfc42c7c431031f2a33e8e37a2'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method

        self.input_id = kwargs.get('input_id')
        super().__init__(**kwargs)

    def start_requests(self):

        merchant_data_raw = loadMerchantData()
        merchant_data_raw_result = filterMerchant(self.input_id, merchant_data_raw)
        merchant_data = merchant_data_raw_result[0]
        is_scheduled = merchant_data_raw_result[1]
        keyword_logic = merchant_data_raw_result[2]
        keywords_input = merchant_data_raw_result[3]

        if is_scheduled == 'scheduled':
            scheduled_counter = getRunTimeCount(self.input_id)
        else:
            scheduled_counter = 0

        for i in range(len(merchant_data)):
            domain = merchant_data['domain'][i]
            keywords = merchant_data['keywords'][i]
            search_term = 'site:' + domain + ' ' + keywords
            try:
                merchant_urls = generateMerchantUrls(site=search_term, api_key=self.api_key)
            except:
                continue

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
                meta_dict = {"merchant_id": merchant_data['merchant_id'][i],
                             "merchant_name": merchant_data['merchant_name'][i],
                             "merchant_url": merchant_data['merchant_url'][i],
                             "product": merchant_data['product'][i],
                             "project_id": merchant_data['project_id'][i],
                             "project_name": merchant_data['project_name'][i],
                             "scheduled_counter": scheduled_counter,
                             "keyword_logic": keyword_logic,
                             "keywords_input": keywords_input
                             }

                yield SplashRequest(url=url, callback=self.parse
                                    , endpoint='execute', args={'lua_source': script},
                                    meta=meta_dict)

    def parse(self, response):
        scan_datetime = datetime.now(timezone.utc)
        scanned_url = response.url
        uuid_ = str(uuid.uuid4()).replace('-', '')
        input_id = self.input_id
        merchant_url = response.meta['merchant_url']
        merchant_id = response.meta['merchant_id']
        merchant_name = response.meta['merchant_name']
        pw_product = response.meta['product']
        project_id = response.meta['project_id']
        project_name = response.meta['project_name']
        scheduled_counter = response.meta['scheduled_counter']
        keyword_logic = response.meta['keyword_logic']
        keywords_input = response.meta['keywords_input']

        if response.status != 200:
            # Pass results to pipeline
            result = MaryJanesItem()
            result['output_id'] = uuid_
            result['url'] = scanned_url
            result['page_content'] = None
            result['scan_time'] = scan_datetime
            result['response_code'] = response.status
            result['screenshot_dir'] = None
            result['merchant_url'] = merchant_url
            result['input_id'] = input_id
            result['merchant_id'] = merchant_id
            result['merchant_name'] = merchant_name
            result['pw_product'] = pw_product
            result['project_id'] = project_id
            result['project_name'] = project_name
            result['reason'] = matchResponseCode(response.status)
            result['scheduled_counter'] = scheduled_counter
            result['keyword_matched'] = 0

        else:
            # Take screenshot
            imgdata = base64.b64decode(response.data['jpeg'])
            filename = strip_hostname(scanned_url) + strip_uri_path(scanned_url) + '.jpeg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            file_loc = img_dir + '/' + str(scan_date) + '/' + filename

            # Clean HTML
            text = response.body
            soup = BeautifulSoup(text)
            clean_text_lvl1 = soup.get_text()
            clean_text_lvl2 = cleanHtml(clean_text_lvl1)

            # Pass results to pipeline
            result = MaryJanesItem()
            result['output_id'] = uuid_
            result['url'] = scanned_url
            result['page_content'] = clean_text_lvl2
            result['scan_time'] = scan_datetime
            result['response_code'] = response.status
            result['screenshot_dir'] = file_loc
            result['merchant_url'] = merchant_url
            result['input_id'] = input_id
            result['merchant_id'] = merchant_id
            result['merchant_name'] = merchant_name
            result['pw_product'] = pw_product
            result['project_id'] = project_id
            result['project_name'] = project_name
            result['reason'] = matchReason(clean_text_lvl2)
            result['scheduled_counter'] = scheduled_counter
            result['keyword_matched'] = keywordMatcher(keyword_logic, keywords_input, clean_text_lvl2)
            # Move screenshots to directory
            for img_file in glob.iglob('*.jpeg'):
                try:
                    shutil.move(img_file, os.path.join(screenshots_dir, img_file))
                except FileNotFoundError:
                    continue

        pass
        yield result
