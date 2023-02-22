from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True)
    user = models.ForeignKey(
        User, related_name='templates', on_delete=models.CASCADE)
    option_1 = models.CharField(max_length=30)
    option_2 = models.CharField(max_length=30)
    option_3 = models.CharField(max_length=30)
    option_4 = models.CharField(max_length=30)
    # TODO isPublic = models.models.BooleanField(_("True"))


    