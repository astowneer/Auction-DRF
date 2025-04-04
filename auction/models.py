from django.db import models
from users.models import CustomUser
from django.urls import reverse_lazy
from django.utils import timezone

from .utils import send_notification

class Category(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to="auctions", blank=True, null=True)
    start_bid = models.PositiveIntegerField()
    min_bid_increment = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True, null=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def close_auction(self):
        if timezone.now() > self.finished and self.active:
            self.active = False
            self.save()

    def notify_users(self):
        highest_bid = self.bids.last()
        if highest_bid:
            bidder = highest_bid.bidder
            send_notification(bidder, f"You won auction {self.title}")
        send_notification(self.seller, f"Your auction {self.title} has been closed")

    def get_absolute_url(self):
        return reverse_lazy("auction_detail", args=[self.id,])
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="bids")
    bid = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __bid__(self):
        return f"{self.bidder} {self.bid}"