from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NotesHandler.as_view(), name='all notes')
]
