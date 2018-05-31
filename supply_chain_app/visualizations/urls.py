from django.conf.urls import url,include
from django.contrib import admin
from .views import treemap, chord_diagram, force_directed, matrix, upload_csv, index

app_name = 'visualizations'

urlpatterns = [
	url(r'^$' , index , name = 'index'),
    url(r'^treemap/$' , treemap , name = 'treemap'),
    url(r'^chord/$' , chord_diagram , name = 'chord_diagram'),
    url(r'^force_directed/$' , force_directed , name = 'force_directed'),
    url(r'^matrix/$' , matrix , name = 'matrix'),
	url(r'^upload/csv/$', upload_csv, name='upload_csv'),
]	