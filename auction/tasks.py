# auction/tasks.py
from celery import shared_task
from auction.models import Auction
from django.utils import timezone

@shared_task
def close_expired_auctions():
    expired_auctions = Auction.objects.filter(active=True, finished__lt=timezone.now())
    for auction in expired_auctions:
        auction.close_auction()
    return f"Successfully closed {expired_auctions.count()} expired auctions"
