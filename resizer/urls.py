from django.urls import path
from . import views


app_name = 'resizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('resize/<str:image_id>', views.resize, name='resize'),    
    path('status/', views.status_page, name='status_page'),
    path('status/<str:image_id>/', views.check_status, name='check_status'),
]
