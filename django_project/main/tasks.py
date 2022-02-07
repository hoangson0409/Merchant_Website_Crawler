from celery import shared_task
from .models import InputMary
# from django.http import JsonResponse, HttpResponseRedirect
from scrapyd_api import ScrapydAPI
import os

# scrapyd = ScrapydAPI(os.getenv('PW_SCRAPY_URL', 'http://localhost:6800'))
scrapyd = ScrapydAPI(os.environ['PW_SCRAPY_URL'])


@shared_task(name="crawl_mary")
def crawl_mary(input_id):

    scrapyd_project = os.getenv('PW_SCRAPY_PROJECT', 'spiderman')
    scrapyd_spider = os.getenv('PW_SCRAPY_SPIDER', 'mary_janes')
    task = scrapyd.schedule(scrapyd_project,
                            scrapyd_spider,
                            input_id=input_id,
                            )
    InputMary.objects.filter(input_id=input_id).update(task_id=task)


# @shared_task(name="crawl_peter")
# def crawl_peter(domain_id='', domain='', keywords=''):
#     if domain_id != '':
#         searched_entry = InputPeter.objects.get(domain_id=domain_id)
#         if not searched_entry.keywords:
#             domain = searched_entry.domain
#         else:
#             domain = searched_entry.domain + ' ' + searched_entry.keywords
#
#     elif domain != '' & keywords == '':
#         domain = domain
#
#     elif domain != '' & keywords != '':
#         domain = domain + ' ' + keywords.replace(',', '|')
#     else:
#         return "{'error': 'Required at least domain_id or domain'}"
#     scrapyd_project = os.getenv('PW_SCRAPY_PROJECT', 'spiderman')
#     scrapyd_spider = os.getenv('PW_SCRAPY_SPIDER', 'peter_parker')
#     task = scrapyd.schedule(scrapyd_project,
#                             scrapyd_spider,
#                             domain_id=domain_id,
#                             )
#     InputPeter.objects.filter(domain_id=domain_id).update(task_id=task)
#
#     # return HttpResponseRedirect('/main/crawl_result1/')
#
