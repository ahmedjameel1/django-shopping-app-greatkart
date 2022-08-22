from .models import *
from carts.models import *
from carts.views import _cart_id


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


