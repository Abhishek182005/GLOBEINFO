from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('country/', views.country_info, name='country_info'),
    path('compare/', views.country_compare, name='country_compare'),
    path('capitals/', views.country_and_capitals, name='country_and_capitals'),
    path('error/', views.error, name='error'),
    path('world-map/', views.world_map, name='world_map'),
    path('currency-exchange/', views.currency_exchange, name='currency_exchange'),
    path('api/country/<str:country_name>/', views.country_api, name='country_api'),
    path('world-records/', views.world_records, name='world_records'),
    path('', views.landing_page, name='landing_page'),
]