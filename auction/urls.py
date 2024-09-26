from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.AuctionList.as_view(), name="auction_list"),
    path("list/category/<str:category_slug>/", views.AuctionList.as_view(), name="auction_category_list"),
    path("<int:pk>/detail/", views.AuctionDetailView.as_view(), name="auction_detail"),
    path("create/", views.AuctionCreateView.as_view(), name="auction_create"),
    path("<int:pk>/update/", views.AuctionUpdateView.as_view(), name="auction_update"),
    path("<int:pk>/delete/", views.AuctionDeleteView.as_view(), name="auction_delete"),
    path("<int:auction_pk>/place_bid/", views.PlaceBidView.as_view(), name="place_bid"),
]