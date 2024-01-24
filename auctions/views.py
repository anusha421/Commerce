from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime
from django.template.defaultfilters import date

from .models import *


class CreateForm(forms.Form):
    CategoryCHOICES = [
        ('Apparels', 'Apparels'),
        ('Footwear', 'Footwear'),
        ('Health', 'Health'),
        ('Electronics', 'Electronics'),
        ('Jewellery', 'Jewellery'),
        ('Accessories', 'Accessories'),
        ('Books', 'Books'),
        ('Appliances', 'Appliances'),
        ('Toys and Games', 'Toys and Games'),
        ('Other', 'Other')
    ]
    title = forms.CharField(widget=forms.TextInput(attrs={
                            'style': 'width: 70%;' 'outline-color: blue;'}), label="Add Title*", max_length=64, required=True)

    description = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'width: 63%;' 'outline-color: blue;'}), label="Add a description*", max_length=1000, required=True)

    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'min': '0', 'style': 'width: 30%;' 'outline-color: blue;'}), label="Enter starting bid*", required=True)

    image = forms.ImageField(widget=forms.FileInput(),
                             label="Upload an image", required=False)

    category = forms.ChoiceField(
        label="Choose Category", choices=CategoryCHOICES)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)

        if form.is_valid():
            obj = Listing()
            obj.user = request.user
            obj.title = form.cleaned_data['title']
            obj.description = form.cleaned_data['description']
            image = Listing(request.FILES.get('image'))
            obj.image = form.cleaned_data['image']
            obj.category = form.cleaned_data['category']
            obj.price = form.cleaned_data['price']
            obj.date = datetime.datetime.now()

            obj.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": CreateForm()
    })


def listing(request, listing_id, title):
    listing = Listing.objects.get(pk=listing_id)
    listing_bids = Bid.objects.filter(listing=listing)

    if Watch.objects.filter(listing=listing) != None:
        watch = Watch.objects.filter(user=request.user, listing=listing)
    
    if Comment.objects.filter(listing=listing) != None:
        comments = Comment.objects.filter(listing=listing)

    if request.method == "POST":
        if 'watch' in request.POST:
            if watch:
                watch.delete()
            else:
                obj = Watch(user=request.user, listing=listing)
                obj.save()
            return HttpResponseRedirect(reverse("watch"))
        
        if 'comment' in request.POST:
            new_comment = request.POST.get('comment_text')
            comment = Comment(user=request.user, listing=listing, text=new_comment)
            comment.save()
            return HttpResponseRedirect(f"/listing/{ listing_id }/{ title }")

        if 'bid' in request.POST:
            new_bid = request.POST.get('bid_number')
            bid = Bid(user=request.user, listing=listing, bid=new_bid)
            bid.save()
            listing1 = Listing.objects.filter(pk=listing_id)
            listing1.update(price=new_bid)
            return HttpResponseRedirect(f"/listing/{ listing_id }/{ title }")

        if 'close_bid' in request.POST:
            listing1 = Listing.objects.filter(pk=listing_id)
            listing1.update(status=False)
            return HttpResponseRedirect(f"/listing/{ listing_id }/{ title }")

    return render(request, "auctions/listings.html", {
        "count": Bid.objects.filter(listing=listing).count(),
        "comments": comments,
        "listing_id": listing_id,
        'title': title,
        "listing": listing,
        "listing_bids": listing_bids,
        "watch": watch
    })


def watch(request):
    watch_items = Watch.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watches": watch_items
    })


def categories(request):
    options = ['Apparels', 'Footwear', 'Health', 'Electronics', 'Jewellery', 'Accessories', 'Books', 'Appliances', 'Toys and Games', 'Other']
    return render(request, "auctions/categories.html", {
        "options": options
    })


def category(request, title):
    listings = Listing.objects.filter(category=title)
    return render(request, "auctions/category.html", {
        "title": title,
        "listings": listings
    })