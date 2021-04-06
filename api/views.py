from api.serializers import CarSerializer, CarSerializerRatingCount
from rest_framework.exceptions import NotAcceptable
from api.models import Car
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests


@api_view(http_method_names=["GET", "POST"])
def cars(request, format=None):
    if request.method == "GET":
        cars = Car.objects.all()
        if not cars:
            return Response({"Message": "Empty database"})
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        url = Car.url
        post_fields = {"format": "json"}
        serializer = CarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"Error": "Fields not valid. Check the request body."})
        else:
            try:
                # <---------- Connect to external API --------------->
                make = request.data.get("make")
                r_make = requests.get(url + make, params=post_fields)
                r_make.raise_for_status()
            # Can handle HTTPError, timeout, network connection separately if needed
            except Exception as e:
                return Response({"Error": e.args[0]}, status=r_make.status_code)
            # <---------- Search through the results for a match --------------->
            for item in r_make.json()["Results"]:
                if request.data.get("model") in item.values():
                    # <---------- Save to database --------------->
                    serializer.save()
                    # print("saving")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            # <---------- In case search was not matched --------------->
            return Response(
                {"Error": "Car was not found, can not add to database"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(http_method_names=["DELETE"])
def carspk(request, pk, format=None):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response({"Error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)
    car.delete()
    return Response({"Success": "Car deleted"}, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
def rate(request, format=None):
    try:
        car: Car = Car.objects.get(pk=request.data["car_id"])
        ratecar = request.data["rating"]
        print(ratecar)
        car.rate_me(ratecar)
        car.save()
        return Response(
            {f"Car {car.pk}, {car.make} {car.model} rated at ": f"{car.rating}"},
            status=status.HTTP_200_OK,
        )
    except Car.DoesNotExist:
        return Response({"Error": "Car not found."}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(
            {"Error": "The request should contain car_id and rating keys."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except NotAcceptable:
        return Response(
            {"Error": "Rating should be between 1 and 5"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"Error": f"{e}"})


@api_view(http_method_names=["GET"])
def carspopular(request, format=None):
    cars = Car.objects.order_by("-rating_count").all()
    if not cars:
        return Response({"Message": "Empty database"})
    serializer = CarSerializerRatingCount(cars, many=True)
    print(serializer.data)
    return Response(serializer.data)