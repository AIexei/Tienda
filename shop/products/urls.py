from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index , name='index'),
    url(r'^product/id(?P<sku_id>\d+)/$', views.product, name='product'),
    url(r'^favourites/$', views.favourites, name='favourites'),
    url(r'^search/', views.search, name='search'),
    url(r'^like/', views.like_action, name='like_action'),
    url(r'^add_comment/(?P<sku_id>\d+)/$', views.add_comment, name='add_comment'),

]