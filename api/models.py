from django.db import models
from rest_framework.exceptions import NotAcceptable


class Car(models.Model):
    make = models.TextField()
    model = models.TextField()
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.url

    def rate_me(self, rating):
        if rating not in [1, 2, 3, 4, 5]:
            raise NotAcceptable
        else:
            self.rating_count += 1
            self.rating = (
                self.rating * (self.rating_count - 1) + rating
            ) / self.rating_count
