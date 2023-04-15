from django.db import models
from django.contrib.auth.models import User

###########################################################################
# Template


class Template(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=True)
    subscribers = models.ManyToManyField(
        User, related_name="templates", blank=True)

    option_1 = models.CharField(max_length=30)
    option_2 = models.CharField(max_length=30)
    option_3 = models.CharField(max_length=30)
    option_4 = models.CharField(max_length=30)

    creator = models.ForeignKey(
        User, related_name="created_templates", on_delete=models.CASCADE, blank=True, null=True)
    # TODO isPublic = models.models.BooleanField(_("True"))


###########################################################################
# Subscription


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template')
