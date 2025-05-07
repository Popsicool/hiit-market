from django.urls import path
from product.views import *

urlpatterns = [
    path('add', add_product, name='add_product'),
    path('edit/<int:id>', edit_product, name="edit_product"),
    path('delete/<int:id>', delete_product, name="delete_product")
]