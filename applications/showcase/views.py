import json

from django.db.models import Count
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import Q

from .documents import ProductDocument
from .forms import SearchProductsForm
from ..auth_app.models import User
from ..cart.forms import CartAddProductForm
from ..orders.models import OrderItem


def home(request):
    return render(request, 'showcase/home.html')


from django.shortcuts import render, get_object_or_404
from .models import Category, Product


@csrf_exempt
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    form = SearchProductsForm()

    filters = [Q('term', available=True)]
    if category_slug:
        filters.append(Q("term", **{'category.slug': category_slug}))

    if request.method == 'POST':
        form = SearchProductsForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data.get("search_input")
            filters.append(Q('bool', should=[Q('match', name=search_value),
                                             Q('match', description=search_value)]))
    else:
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
    products = ProductDocument.search().query(Q('bool', must=[*filters]))
    return render(request,
                  'showcase/home.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'form': form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'showcase/detail.html', {'product': product,
                                                    'cart_product_form': cart_product_form})
