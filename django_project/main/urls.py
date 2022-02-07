from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'app1_input', views.InputPeterViewSet)
router.register(r'app1_output', views.OutputPeterViewSet)
router.register(r'app2_input', views.InputMaryViewSet)
router.register(r'app2_output', views.OutputMaryViewSet)

urlpatterns = [
    # RESTAPI
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # MAIN PAGE
    path('', views.spiderman, name='spiderman'),
    # APP 1
    path('search_one/', views.peter_parker, name='peter_parker'),
    path('crawl/', views.peter_parker_crawl, name='crawl'),
    path('crawl_result1/', views.peter_output.as_view(), name='crawl_result1'),
    path('crawl_result1/<output_id>', views.peter_output_detail, name='crawl_result_detail1'),
    # APP 2
    path('search_all/', views.mary_janes, name='mary_janes'),
    path('crawl_all/', views.mary_janes_crawl, name='crawl2'),
    path('crawl_result2/', views.mary_output.as_view(), name='crawl_result2'),
    path('crawl_result2/<output_id>', views.mary_output_detail, name='crawl_result_detail2'),
    # OTHERS

]
