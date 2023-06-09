from django.urls import path
from .views import PetView, PetDetailsViwes


urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDetailsViwes.as_view()),
]
