from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),  # Make sure 'about' view is defined
    # path('portfolio/', views.portfolio, name='portfolio'),  # Make sure 'about' view is defined
    # path('connect/', views.connect, name='connect'),  # Make sure 'about' view is defined
]
