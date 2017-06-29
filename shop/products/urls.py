from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', IndexView.as_view() , name='index'),
    url(r'^product/id(?P<sku_id>\d+)/$', ProductView.as_view(), name='product'),
    url(r'^favourites/$', FavouritesView.as_view(), name='favourites'),
    url(r'^search/', SearchView.as_view(), name='search'),
    url(r'^like/', LikeUpdate.as_view(), name='like_action'),
    url(r'^add_comment/(?P<sku_id>\d+)/$', CommentCreate.as_view(), name='add_comment'),
    url(r'^buy/id(?P<sku_id>\d+)/c(?P<cost>\d+)/$', Payment.as_view(), name='buy'),
]