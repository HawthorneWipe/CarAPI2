from django.urls import path
from api.views import cars, carspk, rate, carspopular

urlpatterns = [
    path("cars/", cars, name="cars"),
    path("cars/<pk>", carspk, name="cardelete"),
    path("rate/", rate, name="carrate"),
    path("popular/", carspopular, name="popular"),
]