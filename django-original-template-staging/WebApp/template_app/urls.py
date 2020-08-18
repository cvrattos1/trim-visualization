# Django
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

# DRF
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

# Apps routes
from WebApp.template_app.web import views as web_views
from WebApp.template_app.api.v1 import views as api_views


app_name = 'template_app'

router = DefaultRouter()

# DRF api routes
router.register(r'test-data', api_views.testDataApiView, basename="test-data")
router.register(r'trim-data', api_views.trimDataApiView, basename="trim-data")
router.register(r'meta-data', api_views.metaDataApiView, basename="meta-data")

urlpatterns = [

    # web routes
    # Admin page
    path('admin/', admin.site.urls),

    # Application URLs
    url(r'^$', web_views.testDataPage.as_view(), name='index'),
    url(r'^index', web_views.testDataPage.as_view(), name='home'),
    url(r'^api/chart/data/$', api_views.ChartData.as_view()),
    url(r'^chartview', web_views.ChartView.as_view(), name='chart-view'),
    url(r'^api/state/data/$', api_views.StateData.as_view()),
    url(r'^mapview', web_views.MapView.as_view(), name='map-view'),
    url(r'^api/multiple/data/$', api_views.MultipleData.as_view()),
    url(r'^api/total/data/$', api_views.TotalData.as_view()),
    url(r'^api/meta/data/$', api_views.MetaData.as_view()),
    url(r'^newmapview', web_views.newDataPage.as_view(), name='newmap-view'),
    url(r'^api/linechart/data/$', api_views.LineChartData.as_view()),
    url(r'^api/metadata/data/$', api_views.MetaDataTest.as_view()),
    url(r'^api/stateeligible/data/$', api_views.StateEligibleData.as_view()),

    # API routes
    # include api routes from above
    path('api/v1/', include(router.urls)),

]


#urlpatterns = format_suffix_patterns(urlpatterns)
