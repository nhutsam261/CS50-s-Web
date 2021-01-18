from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Product, Reviews, Start, Purchased
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.
class IndexListView(ListView):
    model = Product
    template = 'KAT/index.html'
    context_object_name = 'products'
    ordering = ['-count_sold']

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Product.objects.all()[:10]

def products(request, category):
    try:
        all_products = Product.objects.filter(category=category)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Products not found."}, status=404)
    
    if request.method == 'GET':
        products = Product.objects.all().order_by('-count_sold')
        results = [product.serialize() for product in products]
        return JsonResponse(results, safe=False)

def profile(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user_profile = Profile.objects.filter(slug=slug).first()
    user = user_profile.user
    orders = user.order.all()
    incomplete_orders = [order for order in orders if order.status == 0]
    completed_orders = [order for order in orders if order.status == 1]
    error_orders = [order for order in orders if order.status == 2]
    context = {'user': user,'incomplete_orders': incomplete_orders,'completed_orders': completed_orders,'error_orders': error_orders}
    return render(request, 'KAT/profile.html', context)


@login_required
def checkout(request, products):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method is required'}, status = 400)
    products = json.loads(request.body)
    
    return render(request, 'network/profile.html', products)
 

@login_required
def submit_order(request, products):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method is required'}, status = 400)
    jsonProducts = json.loads(request.body)
    products = jsonProducts.get('products', '')
    if products == '':
        return JsonResponse({'error': 'products must not empty !!'}, status=400)
    
    user = request.user
    userOrder = Order.objects.create(user=user)

    for product in products:
        instance_product = Product.objects.filter(name_product=product['name_product'])
        OrderProduct.objects.create(order = userOrder, product=instance_product, quality = product['quality'])
    













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
            return render(request, "KAT/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "KAT/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "KAT/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phone_number)
            user.save()
        except IntegrityError:
            return render(request, "KAT/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
