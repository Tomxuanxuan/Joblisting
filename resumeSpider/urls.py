from django.conf.urls import url
from resumeSpider import views

urlpatterns = [
    url(r'^$', views.JobIndex, name='jobindex'),
    url(r'^single$', views.JobSingle, name='jobsingle'),
    url(r'^search$', views.Search, name='search'),
    url(r'^updatejobs$', views.UpdateJobs, name='updatejob'),
    url(r'^analyze', views.Analyze, name='analyze'),
    url(r'^message$', views.Message, name='message'),
    url(r'contantme$', views.Contactme, name='jobcontact')
]
