from django import forms
from django.core.exceptions import ValidationError

from .models import Bid, Auction

class PlaceBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ("bid",)

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop("auction", None) 
        super().__init__(*args, **kwargs)

    def clean_bid(self):
        bid = self.cleaned_data.get("bid")
        if self.auction: 
            current_highest_bid = self.auction.start_bid 
            min_bid_increment = self.auction.min_bid_increment
            
            if bid <= current_highest_bid + min_bid_increment:
                raise forms.ValidationError(
                    f"The bid must be greater than the current highest bid ({current_highest_bid}) plus the minimum increment ({min_bid_increment})."
                )
        return bid