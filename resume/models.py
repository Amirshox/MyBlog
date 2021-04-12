from django.db import models


class Portfolio(models.Model):
    title = models.CharField(max_length=20)
    url = models.URLField()
    image_one = models.ImageField(upload_to='portfolio/')
    image_two = models.ImageField(upload_to='portfolio/')
    image_three = models.ImageField(upload_to='portfolio/')

    def __str__(self):
        return self.title
