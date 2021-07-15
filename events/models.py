from django.db import models
from django.urls import reverse
from users.models import Profile
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import gettext_lazy as _
# Create your models here.
class event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    club_name= models.ForeignKey(User, on_delete=models.CASCADE)
    event_name=models.CharField(max_length=256)
    description=models.TextField()
    event_date=models.DateField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    link=models.CharField(max_length=1000)
    def clean(self):
        if self.event_date < datetime.date.today():
            raise ValidationError(_("The date cannot be in the past!"))

    def __str__(self):
        a=str(self.pk)+self.event_name+"("+str(self.club_name)+")"
        return a
    def get_absolute_url(self):
        return reverse("events:list")
