from django.shortcuts import render

from .documents import ProductDocument
from ..cart.forms import CartAddProductForm


def home(request):
    return render(request, 'showcase/home.html')


from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    products = ProductDocument.search().filter("term", available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter("term", **{'category.slug': category_slug})
    return render(request,
                  'showcase/home.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'showcase/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})