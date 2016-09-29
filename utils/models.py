from django.db import models


class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Misc(models.Model):
    item = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return self.item

    class Meta:
        app_label = 'act'
        verbose_name_plural = 'Miscellaneous'

