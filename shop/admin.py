from django.contrib import admin
from .models import ProductCategoryParent, ProductCategoryChild, Product, ProductImage, Cart, Contacts

admin.site.register(ProductCategoryParent)
admin.site.register(ProductCategoryChild)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Contacts)