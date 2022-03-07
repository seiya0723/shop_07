from django import forms

from .models import ProductCategoryParent, ProductCategoryChild, Product, ProductImage, Cart, Contacts

class ProductCategoryParentForm(forms.ModelForm):
    class Meta:
        model = ProductCategoryParent
        fields = ['name']

class ProductCategoryChildForm(forms.ModelForm):
    class Meta:
        model = ProductCategoryChild
        fields = ['category', 'name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'stock', 'image', 'description', 'price', 'situation']

class ProductsImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'product']

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'stock', 'image', 'description', 'price', 'situation']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'amount']

class CartEditForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['amount']

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['user_id', 'name', 'email', 'title', 'contents']