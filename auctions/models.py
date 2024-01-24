from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="uploads", blank=True, null="True")
    category = models.CharField(max_length=64, null=True)
    price = models.IntegerField(default=0)
    date = models.DateTimeField(default=None)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.id})"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_title")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user} bid {self.bid} on {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_title")
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} commented on {self.listing}"

class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watches")

    def __str__(self):
        return f"{self.user}, {self.listing}"