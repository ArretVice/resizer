from django.urls import path
from . import views


app_name = 'resizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.UploadAndResizeView.as_view(), name='upload'),
    path('status/', views.CheckStatusView.as_view(), name='check_status'),
    path('status/<str:task_id>/', views.TaskStatusView.as_view(), name='task'),
]
