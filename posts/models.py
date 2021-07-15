"""Posts models."""

# Django
from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
import uuid

class Post(models.Model):
    """Post Model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='author')

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    liked=models.ManyToManyField(User,default=None,blank=True,related_name='Liked')

    def __str__(self):
        """Return title and username"""
        return "{} by @{}".format(self.title, self.profile.user.username)
    @property
    def num_likes(self):
        return self.liked.all().count()
LIKE_CHOICES=(
    ('Like','Like'),
    ('UnLike','UnLike')
    )
class Like(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)
    def __str__(self):
        return str(self.post)
