from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_user[/]?$', CreateUserView.as_view(), name='create_user'),
    url(r'^login_user[/]?$', LoginUserView.as_view(), name='login_user'),
    url(r'^detail[/]?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^add_favourites[/]?$', AddUserFavouritesView.as_view(), name='add_favourites'),
]