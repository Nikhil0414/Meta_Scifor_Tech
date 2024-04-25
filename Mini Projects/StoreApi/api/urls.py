from django.urls import path
from .views import ItemList, ItemDetails, LocationList, LocationDetails


urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<int:pk>/', ItemDetails.as_view()),
    path('location/', LocationList.as_view()),  # Corrected endpoint for LocationList
    path('location/<int:pk>/', LocationDetails.as_view()),  # Corrected endpoint for LocationDetails
]