# User models

# Django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    """
    Profile model

    Proxy Model that extends the base data with other information.
    """
    # Relation con la tabla user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Campos extendidos
    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_student = models.BooleanField(default=True)
    is_club = models.BooleanField(default=False)
    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    # time
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username"""
        return self.user.username
class clubrating(models.Model):
    user = models.ForeignKey(User,related_name='rating', on_delete=models.CASCADE)
    club=models.CharField(max_length=200)
    content=models.TextField(blank=True,null=True)
    stars=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)+" "+self.club+" "+str(self.stars)
