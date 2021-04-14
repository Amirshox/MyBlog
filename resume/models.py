from django.db import models


class Portfolio(models.Model):
    title = models.CharField(max_length=20)
    url = models.URLField()
    image = models.ImageField(upload_to='portfolio/')

    def __str__(self):
        return self.title
