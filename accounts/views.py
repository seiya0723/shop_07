from django.shortcuts import render, redirect
from django.views.generic import View

from .models import CustomUser, CustomUserAddress
from .forms import SignupForm, NameEditForm, AddressForm, AddressEditForm

from shop.models import ProductCategoryParent, ProductCategoryChild, Product, Cart, Contacts

class AccountsMyPageView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['user'] = CustomUser.objects.filter(id=pk).first()
        context['categories'] = ProductCategoryParent.objects.all()
        context['category'] = ProductCategoryChild.objects.all()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'accounts/accounts_page.html', context)

MyPage = AccountsMyPageView.as_view()

class NameEditView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['user'] = CustomUser.objects.filter(id=pk).first()
        context['categories'] = ProductCategoryParent.objects.all()
        context['category'] = ProductCategoryChild.objects.all()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, "accounts/name_edit.html", context)

    def post(self, request, pk, *args, **kwargs):

        account = CustomUser.objects.filter(id=pk).first()

        form = NameEditForm(request.POST, instance=account)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("accounts:name_edit", pk)

NameEdit = NameEditView.as_view()

class AccountsAddressListView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['user'] = CustomUser.objects.filter(id=pk).first()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'accounts/address_list.html', context)

AddressList = AccountsAddressListView.as_view()

class AddressCreateView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['user'] = CustomUser.objects.filter(id=pk).first()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'accounts/address_create.html', context)

    def post(self, request, pk, *args, **kwargs):

        copied = request.POST.copy()
        copied["user_id"] = request.user.id

        form = AddressForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect('accounts:address_create', pk)

AddressCreate = AddressCreateView.as_view()


class AccountsAddressEditView(View):

    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['user'] = CustomUser.objects.filter(id=pk).first()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'accounts/address_edit.html', context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:共通箇所
        #指定されたpkが存在するかチェック
        address = CustomUserAddress.objects.filter(id=pk, user_id=request.user.id).first()

        #存在しない場合
        #ここはアーリーリターンを使いましょう
        if not address:
            return redirect('accounts:address_edit', pk)



        #TODO:ここでmainの値のみ書き換える場合、バリデーション用のフォームクラスは不要。
        #TODO:以下、mainを変える場合のみの処理(実践ではPATCHメソッドに下記の処理を割り当て)
        """
        #全てのデータをFalseに
        addresses = CustomUserAddress.objects.filter(user_id=request.user.id, main=True)

        for a in addresses:
            a.main = False
            a.save()

        #指定された値をTrueに変換して保存。
        address.main = True
        address.save()
        """


        #TODO:もし全てのデータを同時に書き換える場合、バリデーション用のフォームクラスは必要

        copied              = request.POST.copy()
        copied["user_id"]   = request.user.id

        form = AddressEditForm(copied, instance=address)

        if not form.is_valid():
            print('バリデーションNG')
            print(form.errors)
            return redirect('accounts:address_edit', pk)


        #TODO:この時、mainの値がTrueであれば、既に記録されているデータのTrueをFalseにする。
        cleaned = form.clean()

        if cleaned["main"]:
            addresses = CustomUserAddress.objects.filter(user_id=request.user.id, main=True)

            for a in addresses:
                a.main = False
                a.save()

        #そして保存する。
        print('バリデーションOK')
        form.save()

        return redirect('accounts:address_edit', pk)

AddressEdit = AccountsAddressEditView.as_view()
