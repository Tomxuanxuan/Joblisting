from django.conf.urls import url,include
from resume import views

urlpatterns = [
    #当访问路径是空的时候
    url(r'^$', views.index),
    url(r'^workexp', views.workexperience, name='workexp'),
    url(r'^login$', views.login_views, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^contact$', views.contactme, name='contact'),
]
