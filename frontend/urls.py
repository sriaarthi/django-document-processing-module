from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('uploadPage/', views.uploadPage, name='uploadPage'),
    # path('upload/', views.upload, name='upload'),
    path('uploadPage/', views.uploadPage, name='uploadPage')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

