from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, User, Listing, Comment

def removeWatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isLisitingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing = listingData)
    return render(request, "auctions/listing.html" , {
        "listing": listingData,
        "isLisitingInWatchlist": isLisitingInWatchlist,
        "allComments" : allComments
    }
)

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )

    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListing,
        "categories": categories
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

def createListing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        # Get the data from form
        title = request.POST["title"]
        description = request.POST["description"]
        imgurl = request.POST["imgurl"]
        price = request.POST["price"]
        category = request.POST["category"]

        categoryData = Category.objects.get(categoryName = category)
        #Current User
        currentUser = request.user

        #Create New listing
        newListing = Listing(
             title=title,
             description=description,
             img=imgurl,
             price=float(price),
             category=categoryData,
             owner=currentUser
        )

        #Insert NewListing
        newListing.save()

        return HttpResponseRedirect(reverse(index))

def displayCategory(request):
    if request.method=="POST":
        categoryForm= request.POST["category"]
        category = Category.objects.get(categoryName = categoryForm)
        activeListing = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings":activeListing,
            "categories": categories
        })