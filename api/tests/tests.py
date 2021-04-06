from django.urls import reverse
import json
import pytest
from api.models import Car

add_cars = reverse("cars")
rate_cars = reverse("carrate")
popular_cars = reverse("popular")
pytestmark = pytest.mark.django_db


# <---------- GET for add cars


def test_add_car_should_succeed(client) -> None:
    test_car: Car = Car.objects.create(make="Volkswagen", model="Golf")
    response = client.get(add_cars)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("make") == test_car.make
    assert response_content.get("model") == test_car.model


# <---------- POST for add cars


def test_add_non_existing_car_should_fail(client) -> None:
    response = client.post(
        add_cars,
        data={"make": "Stokrotka", "model": "Polna"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert "Error" in str(response.content)
    assert "was not found" in str(response.content)


# <---------- DELETE for add cars


def test_delete_car_should_succeed_return_empty(client) -> None:
    test_car: Car = Car.objects.create(make="Volkswagen", model="Golf")
    delete_car = reverse("cardelete", kwargs={"pk": test_car.pk})
    response = client.delete(delete_car)
    assert response.status_code == 200
    assert "Success" in str(response.content)


# <---------- POST for rate


def test_post_car_rating_should_succeed(client) -> None:
    rating_to_test = 4
    test_car1: Car = Car.objects.create(make="Volkswagen", model="Golf", rating=4)
    response = client.post(
        rate_cars,
        data={"car_id": test_car1.pk, "rating": rating_to_test},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert test_car1.model in str(response.content)
    assert test_car1.make in str(response.content)
    assert test_car1.rating == rating_to_test


# <---------- GET popular cars


def test_get_popular_cars_should_succeed_and_order(client) -> None:
    test_car1: Car = Car.objects.create(
        make="Volkswagen", model="Golf", rating=3, rating_count=3
    )
    test_car2: Car = Car.objects.create(
        make="Volkswagen", model="Golf", rating=4, rating_count=4
    )
    response = client.get(popular_cars)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content[0]["rating"] > content[1]["rating"]
