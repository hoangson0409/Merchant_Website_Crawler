import time
# import requests
# import json
# import pymysql
from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import urlparse
from serpapi import GoogleSearch
from psycopg2.extensions import register_adapter, AsIs
from uritools import urisplit
from .settings import PW_CONNECTIONS, FP_CONNECTIONS, DB_CONNECTIONS
from http.client import responses
import re
from bs4 import BeautifulSoup


def sendRequestAndAppendURL(params: dict, url_list: list):
    try:
        search = GoogleSearch(params)
    except:
        print('Requests to SERPAPI could not be handled')

    results = search.get_dict()
    organic_results = results['organic_results']

    if 'serpapi_pagination' in results:
        page_count = len(results['serpapi_pagination']['other_pages'])
        is_multiple_page = True
        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            url_list.append(link)
        return is_multiple_page, url_list, page_count

    else:
        is_multiple_page = False
        for i in range(len(organic_results)):
            link = organic_results[i]['link']
            url_list.append(link)
        return is_multiple_page, url_list


def generateMerchantUrls(site: str, api_key: str):
    # FIRST SEND THE REQUEST FOR ONE PAGE
    merchant_urls = []
    params = {
        "engine": "google",
        "q": site,
        "google_domain": "google.com",
        "start": "0",
        "num": "1000",
        "device": "desktop",
        "api_key": api_key
    }
    result = sendRequestAndAppendURL(params, merchant_urls)
    is_multiple_page = result[0]
    merchant_urls = result[1]

    if is_multiple_page:
        page_count = result[2]

        # USE NUMBER OF PAGE TO KEEP LOOPING
        for i in range(page_count):
            params = {
                "engine": "google",
                "q": site,
                "google_domain": "google.com",
                "start": str(i * 100),
                "num": "1000",
                "device": "desktop",
                "api_key": api_key
            }
            try:
                sendRequestAndAppendURL(params, merchant_urls)
            except:
                print('Requests to SERPAPI could not be handled')
                break
            time.sleep(1)

        return merchant_urls
    else:

        return merchant_urls


def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


# Extract hostname from url
def strip_hostname(url):
    hostname = str(urisplit(url).authority)
    return hostname


# Extract path from url
def strip_uri_path(url):
    remove_chars = ['/', ':']
    uri_path = str(urisplit(url).path)
    for character in remove_chars:
        uri_path = uri_path.replace(character, '_')
    return uri_path


def pwDba3Connect():
    engine = create_engine(PW_CONNECTIONS)
    return engine


def fasterpayConnect():
    engine = create_engine(FP_CONNECTIONS)
    return engine


def filterTestMerchant(x):
    test_keywords = ["Paymentwall", "PaymentWall", "test", "vanya.codes", "Terminal3", "example",
                     "google", "facebook", "youtube", "gmail", "instagram", "mobiamo", "my project", "hotmail",
                     "fasterpay",
                     "testbed", "none"]
    for i in test_keywords:
        if i in x or i.lower() in x or i.upper() in x:
            return 1
        else:
            continue


def filterPlatformMerchantPW(x):
    platform_keywords = ["amember/payment/paymentwall", "/callback/gw/", "buycraft.net/ipn/paymentwall",
                         "index.php\\?dispatch=paymentwall.pingback",
                         "edd-listener=paymentwall",
                         "enjin.com/paymentwall.php",
                         "index.php\\?app=nexus&module=payments&section=receive&do=validate",
                         "index.php\\?app=nexus&module=checkout&controller=pwPingback",
                         "\\?paymentwallListener=paymentwall\\_IPN",
                         "/index.php/paymentwall/payment/ipn",
                         "/paymentwall/index/pingback",
                         "minecraftmarket.com/gateway/paymentwall",
                         "/index.php\\?route=checkout/pingback",
                         "\\?do=api/gateway/callback/paymentwall",
                         "modules/paymentwall/pingback.php",
                         "plugins/vmpayment/paymentwall/pingback.php",
                         "modules/gateways/callback/paymentwall.php",
                         "wc-api=paymentwall_gateway",
                         "source=stardekk",
                         "Shopify", "Xenforo", "vBulletin", "Xero", "Telegram", "Kigo", "Stardekk",
                         "modules/paymentwall/pingback.php"]
    for i in platform_keywords:
        if i in x or i.lower() in x or i.upper() in x:
            return 1
        else:
            continue


def genDomain(x):
    t = urlparse(x).netloc
    if 'www' in x:
        return '.'.join(t.split('.')[1:])
    else:
        return '.'.join(t.split('.')[0:])


def cleanedMerchantPW():
    pw_engine = pwDba3Connect()
    pw = pd.read_sql("""SELECT 
                        "pw" AS product,
                        a_id AS project_id,
                        a_name AS project_name,
                        a.d_id as merchant_id,
                        d_company as merchant_name,
                        ds.ds_name as source,
                        a_url AS merchant_url,
                        "app" AS merchant_url_type,
                        a_pingback_url,
                        CURRENT_TIMESTAMP() AS update_time,
                        @@system_time_zone AS timezone
                        from applications a 
                        left join developers d on a.d_id = d.d_id
                        left join devrise_source ds on a.a_ds_id = ds.ds_id
                        where a_live = 1 and a_url is not null and a_url != ''""", pw_engine, index_col=None)
    pw['source'] = pw['source'].fillna('')
    pw['is_test_1'] = pw.merchant_url.map(filterTestMerchant)
    pw['is_test_2'] = pw.project_name.map(filterTestMerchant)
    pw['is_test_3'] = pw.merchant_name.map(filterTestMerchant)
    pw['is_platform_1'] = pw.a_pingback_url.map(filterPlatformMerchantPW)
    pw['is_platform_2'] = pw.source.map(filterPlatformMerchantPW)

    pw = pw[(pw['is_test_1'] != 1) & (pw['is_test_2'] != 1) & (pw['is_test_3'] != 1) & (pw['is_platform_1'] != 1) & (
            pw['is_platform_2'] != 1)]
    return pw[['product', 'project_id', 'project_name', 'merchant_id', 'merchant_name', 'merchant_url',
               'merchant_url_type', 'update_time', 'timezone']]


def cleanedMerchantFP():
    fasterpay_engine = fasterpayConnect()
    fasterpay = pd.read_sql("""SELECT "fp" AS product,
                            id AS merchant_id,
                            company_name AS merchant_name, 
                            '' as project_name,
                            0 as project_id,
                            merchant_url,
                            "official" AS merchant_url_type,
                            CURRENT_TIMESTAMP() AS update_time,
                            @@global.time_zone AS timezone
                            FROM merchants 
                            WHERE onboarding_status = 'approved' AND merchant_url IS NOT NULL""",
                            fasterpay_engine,
                            index_col=None)
    fasterpay['is_test_1'] = fasterpay.merchant_url.map(filterTestMerchant)
    fasterpay['is_platform'] = fasterpay.merchant_url.map(filterPlatformMerchantPW)
    fasterpay = fasterpay[(fasterpay['is_test_1'] != 1) & (fasterpay['is_platform'] != 1)]

    return fasterpay[['product', 'project_id', 'project_name', 'merchant_id', 'merchant_name', 'merchant_url',
                      'merchant_url_type', 'update_time', 'timezone']]


def loadMerchantData():
    # Load Fasterpay merchants
    fasterpay = cleanedMerchantFP()
    # Load PW merchants
    pw = cleanedMerchantPW()
    # Concat dataframes
    merchant_df = pd.concat([fasterpay, pw], ignore_index=True)
    merchant_df['url_id'] = merchant_df['product'].map(str) + '_' + merchant_df['merchant_url_type'].map(str) \
                            + '_' + merchant_df['merchant_id'].map(str)
    merchant_df.set_index('url_id', inplace=True)

    # Fix urls
    for i in range(len(merchant_df)):
        url_scheme = urlparse(merchant_df.iloc[i, merchant_df.columns.get_loc('merchant_url')]).scheme
        url_path = urlparse(merchant_df.iloc[i, merchant_df.columns.get_loc('merchant_url')]).path

        if url_scheme == '':
            merchant_df.iloc[i, merchant_df.columns.get_loc('merchant_url')] = 'http://' + url_path
        else:
            pass
    merchant_df['domain'] = merchant_df['merchant_url'].map(genDomain)
    merchant_df['merchant_id'] = merchant_df['merchant_id'].map(int)
    return merchant_df


def generateSearchTerm(input_id):
    engine = create_engine(DB_CONNECTIONS)
    domain_result = pd.read_sql("""SELECT * FROM main_inputpeter 
        where input_id = '{}' """.format(input_id), engine, index_col=None)

    if domain_result['keywords'][0]:
        keyword_logic = domain_result['keyword_logic'][0]
        if keyword_logic == 'AND':
            keywords = domain_result['keywords'][0].replace(",", " AND ")
        if keyword_logic == 'OR':
            keywords = domain_result['keywords'][0].replace(",", " | ")

        search_term = 'site:' + domain_result['domain'][0] + ' ' + keywords
    else:
        keywords = ''
        keyword_logic = ''
        search_term = 'site:' + domain_result['domain'][0]

    return search_term, keyword_logic, keywords


def filterMerchant(input_id, merchant_data):
    engine = create_engine(DB_CONNECTIONS)
    result = pd.read_sql("""SELECT * FROM main_inputmary 
        where input_id = '{}' """.format(input_id), engine, index_col=None)
    pw_product = result['pw_product'][0]
    merchant_id = result['merchant_id'][0]
    merchant_name = result['merchant_name'][0]
    project_id = result['project_id'][0]
    project_name = result['project_name'][0]
    keywords = result['keywords'][0]
    is_scheduled = result['run_type'][0]

    if pw_product:
        merchant_data = merchant_data[merchant_data['product'] == pw_product]
    if merchant_id:
        merchant_data = merchant_data[merchant_data['merchant_id'] == merchant_id]
    if merchant_name:
        merchant_data = merchant_data[merchant_data['merchant_name'] == merchant_name]
    if project_id:
        merchant_data = merchant_data[merchant_data['project_id'] == project_id]
    if project_name:
        merchant_data = merchant_data[merchant_data['project_name'] == project_name]

    if keywords:
        keyword_logic = result['keyword_logic'][0]
        if keyword_logic == 'AND':
            keywords = keywords.replace(",", " AND ")
        if keyword_logic == 'OR':
            keywords = keywords.replace(",", " | ")
        merchant_data['keywords'] = keywords
    elif not keywords:
        merchant_data['keywords'] = ''
        keywords = ''
        keyword_logic = ''

    return merchant_data, is_scheduled, keyword_logic, keywords


def matchResponseCode(code):
    return responses[code]


def matchReason(text):
    # global reason
    if text is None or text == '':
        reason = 'No content'
    else:
        reason = textToReason(text)
    return reason


def textToReason(text):
    js_pattern = ['.*enable JavaScript', '.*JavaScript.*disabled', '.*without JavaScript enabled',
                  '.*turn on Javascript']

    reason = ''
    for i in js_pattern:
        if re.match(i, text, flags=re.IGNORECASE | re.DOTALL):
            reason = 'JavaScript disabled'
            break

    bb_pattern = ['.*browser.*unsupported', '.*browser.*supported']
    for i in bb_pattern:
        if re.match(i, text, flags=re.IGNORECASE | re.DOTALL):
            reason = 'Bot blocked'
            break

    if reason == '' and len(text) < 300:
        reason = 'Suspiciously short content'

    return reason

def getRunTimeCount(input_id):
    engine = create_engine(DB_CONNECTIONS)
    run_time_result = pd.read_sql("""SELECT * FROM django_celery_beat_periodictask 
        where args = '["{}"]' """.format(input_id), engine, index_col=None)
    run_count = run_time_result['total_run_count'][0]
    return run_count


def keywordMatcher(keyword_logic, keywords, page_content):
    if keywords != '':
        if keyword_logic == 'AND':
            keyword_list = keywords.split('AND')

            keyword_list = [x.strip() for x in keyword_list]
            keyword_count = len(keyword_list)
            count = 0
            for i in keyword_list:
                if i.lower() in page_content or i.upper() in page_content or i in page_content or i.capitalize() in page_content:
                    count += 1
            if count == keyword_count:
                return 1
            else:
                return 0

        if keyword_logic == 'OR':
            keyword_list = keywords.split('|')

            keyword_list = [x.strip() for x in keyword_list]
            keyword_count = len(keyword_list)
            count = 0
            for i in keyword_list:
                if i.lower() in page_content or i.upper() in page_content or i in page_content or i.capitalize() in page_content:
                    return 1
                    break
                else:
                    count += 1
                    continue

            if count == keyword_count:
                return 0
    else:
        return 1



def cleanHtml(raw_html):
    text = BeautifulSoup(raw_html)
    cleantext = text.get_text()
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', cleantext)
    cleantext = cleantext.encode("ascii", "ignore").decode()
    cleantext = cleantext.replace('\t', ' ').replace('\n', ' ')

    if '<iframe' in cleantext:
        iframe_text = re.findall("(?<=<iframe).*(?={ display:none !important; })", cleantext)[0]
        cleantext = cleantext.replace(iframe_text, ' ')
        cleantext = cleantext.replace('<iframe', '').replace('{ display:none !important; }', '')

    return cleantext