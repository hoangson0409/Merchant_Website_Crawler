
# Django
### Running in outer Django project folder (cd django_project)
* Make Migrations
`python manage.py makemigrations`
* Migrate to Database
`python manage.py migrate`
* Run Server
`python manage.py runserver`
  
# Scrapy & Scrapyd
### Run in scrapy application (cd django_project/scrapy_app/scrapy_app)
* Run Scrapyd Server
`scrapyd`  
* Deploy spiders 
`scrapyd-deploy scrapy_app -p spiderman`
* List spiders
`scrapyd-client spiders -p spiderman`
* Cancel Job
`curl http://localhost:6800/cancel.json -d project=spiderman -d job=<job_id>`
  
# CELERY 
### Running in outer Django project folder (cd django_project)
* Start Worker 
`celery -A django_project worker -P solo`
* Start Beat (Scheduler)
`celery -A django_project beat` 