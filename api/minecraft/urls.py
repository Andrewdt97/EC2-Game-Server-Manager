from django.urls import path

from . import views

urlpatterns = [
    path('server-status', views.getServerStatus, name='getServerStatus'),
    path('stop-server', views.stopServer, name='stopServer'),
    path('start-server', views.startServer, name='startServer'),
    path('get-servers', views.getServerList, name='getServerList'),
    path('qa-start-server', views.qa_startServer, name='qaStartServer'),
]