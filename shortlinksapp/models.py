from django.db import models


class Links(models.Model):
    orig_link = models.URLField()
    short_link = models.URLField()
    datetime = models.DateTimeField()
    clicks = models.IntegerField()
