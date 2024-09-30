from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Auction, Category
from .forms import PlaceBidForm


class AuctionList(ListView):
    context_object_name = "auctions"
    paginate_by = 1

    def get_queryset(self):
        queryset = Auction.objects.filter(active=True)
        category_slug = self.request.GET.get("category_slug")
        if category_slug is not None:
            queryset = queryset.filter(category_slug=category_slug)
        
        search_query = self.request.GET.get("search")
        if search_query is not None:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(AuctionList, self).get_context_data(**kwargs)
        context['current_page'] = context.pop('page_obj', None)
        return context


class AuctionDetailView(DetailView):
    model = Auction
    context_object_name = "auction"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PlaceBidForm(auction=self.object) 
        auction = self.get_object()
        bids_history = auction.bids.all()
        context["bids_history"] = bids_history

        if not auction.active:
            if auction.seller == self.request.user:
                context["seller_message"] = "Your auction has been closed"

            last_bid = auction.bids.last()
            if last_bid:
                bidder = last_bid.bidder
                if bidder == self.request.user:
                    context["bidder_won_message"] = "You are the winner of this bid"
            else:
                context["bidder_won_message"] = "No bids were placed."
        return context
    

class AuctionCreateView(LoginRequiredMixin, CreateView):
    model = Auction
    fields = ["title", "description", "start_bid", "min_bid_increment", "image"]
    
    def form_valid(self, form):
        if form.instance.finished and form.instance.finished < timezone.now():
            form.add_error("finished", "End time must be in the future")
            return self.form_invalid(form)
        form.instance.seller = self.request.user
        return super().form_valid(form)


class AuctionUpdateView(UpdateView):
    model = Auction
    template_name_suffix = "_edit_form"
    fields = ["title", "description", "start_bid", "min_bid_increment", "image"]
    

class AuctionDeleteView(DeleteView):
    model = Auction
    success_url = reverse_lazy("auction_list")


class PlaceBidView(FormView):
    form_class = PlaceBidForm
    template_name = "auction/auction_place_bid.html"

    def dispatch(self, request, *args, **kwargs):
        self.auction = self.get_auction()
        return super().dispatch(request, *args, **kwargs)
    
    def get_auction(self):
        return get_object_or_404(Auction, id=self.kwargs["auction_pk"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["auction"] = self.auction 
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["auction"] = self.auction
        return kwargs
    
    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.auction = self.auction
        self.auction.make_unactive()
        bid.bidder = self.request.user
        bid.save()

        self.auction.start_bid = bid.bid
        self.auction.save()

        messages.success(self.request, "Your bid has been placed successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your bid.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("auction_detail", kwargs={"pk": self.kwargs["auction_pk"]})
    
