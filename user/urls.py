from django.urls import path


from . import views


app_name = 'user'


urlpatterns = [
    path('dashboard/', views.dashboard_View, name='dashboard'),
    
]





