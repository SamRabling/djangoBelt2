from django.conf.urls import url
from . import views           
urlpatterns = [
  ## LOGIN / REGISTRATION / LOGOUT ROUTES
  url(r'^process$', views.process),
  url(r'^create$', views.create),
  url(r'^logout$', views.logout),
  
  ## ADDING/DELETING DATA
  url(r'^add_quote$', views.add_quote),
  url(r'^add_to_my_faves/(?P<id>\d+)$', views.add_to_my_faves),
  url(r'^remove_from_faves/(?P<id>\d+)$', views.remove_from_faves),
  
  ## PAGE ROUTES
  url(r'^$', views.index), 
  url(r'^home$', views.home), 
  url(r'^user_quotes/(?P<id>\d+)$', views.user_quotes),
  
]

# 