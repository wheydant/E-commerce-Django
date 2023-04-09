from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    img = models.CharField(max_length=2000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing =  models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="lisitngComment")
    message =  models.CharField(max_length=400)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"

class Cmnt(models.Model):
    author =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userCmnt")
    listing =  models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="lisitngCmnt")
    message =  models.CharField(max_length=400)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"