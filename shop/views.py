from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator

from accounts.models import CustomUser
# from accounts.forms import SignupForm, AccountEditForm

from .models import ProductCategoryParent, ProductCategoryChild, Product, ProductImage, Cart, Contacts
from .forms import ProductCategoryParentForm, ProductCategoryChildForm, ProductForm, ProductsImageForm, ProductEditForm, CartForm, ContactsForm

class HomeView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        context["products"] = Product.objects.all()[:4]
        context['categories'] = ProductCategoryParent.objects.all()
        context['category'] = ProductCategoryChild.objects.all()
        context['users'] = CustomUser.objects.all()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'shop/home.html', context)

Home = HomeView.as_view()

class ProductsListView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        context["products"] = Product.objects.all()
        context['category'] = ProductCategoryParent.objects.all()
        context['categories'] = ProductCategoryChild.objects.all()
        context['users'] = CustomUser.objects.all()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        sort_list = [
            {"key": "price", "value": "値段が安い順"},
            {"key": "-price", "value": "値段が高い順"},
            {'key': 'dt', 'value': '最新順'},
        ]

        keys = [s["key"] for s in sort_list]

        context["sort_list"] = sort_list


        if "order_by" in request.GET:

            #その並び替えが指定のリストの中にある。

            if request.GET["order_by"] in keys:

                context["products"] = Product.objects.order_by(request.GET["order_by"])
            else:
                context["products"] = Product.objects.all()
        else:
            context["products"] = Product.objects.all()

        return render(request, 'shop/product_list.html', context)

ProductsList = ProductsListView.as_view()

class ProductsSearchView(View):
    def get(self, request, *args, **kwargs):

        if "search" in request.GET:

            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("shop:search")

            search = request.GET["search"].replace("　", " ")
            search_list = search.split(" ")

            query = Q()
            for word in search_list:
                query &= Q(name__contains=word)

            # .order_byメソッドで並び替えしないと、paginatorでWARNINGが出る。
            data = Product.objects.filter(query).order_by("id")
        else:
            data = Product.objects.all().order_by("id")

        # ===========ここからページネーション処理================
        paginator = Paginator(data, 4)

        if "page" in request.GET:
            data = paginator.get_page(request.GET["page"])
        else:
            data = paginator.get_page(1)

        context = {"data": data}
        context['category'] = ProductCategoryParent.objects.all()
        context['users'] = CustomUser.objects.all()
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, "shop/search.html", context)

    def post(self, request, *args, **kwargs):

        return redirect("shop:search")

ProductsSearch = ProductsSearchView.as_view()

class ProductsView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        context['products'] = Product.objects.all()
        context['category'] = ProductCategoryParent.objects.all()
        context['categories'] = ProductCategoryChild.objects.all()

        return render(request, 'shop/products_create.html', context)

    def post(self, request, *args, **kwargs):

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            print('バリデーションOK')
            messages.info(request, "バリデーションOK")
            form.save()
        else:
            print('バリデーションNG')
            print(form.errors)
            messages.add_message(request, messages.INFO, form.errors)

        return redirect('shop:products')

Products = ProductsView.as_view()

class ProductCategoryParentView(View):
    def post(self, request, *args, **kwargs):

        form = ProductCategoryParentForm(request.POST)

        if form.is_valid():
            print('バリデーションOK')
            messages.info(request, "バリデーションOK")
            form.save()
        else:
            print('バリデーションNG')
            print(form.errors)
            messages.add_message(request, messages.INFO, form.errors)

        return redirect('shop:products')

CategoryParent = ProductCategoryParentView.as_view()

class ProductCategoryChildView(View):
    def post(self, request, *args, **kwargs):

        form = ProductCategoryChildForm(request.POST)

        if form.is_valid():
            print('バリデーションOK')
            messages.info(request, "バリデーションOK")
            form.save()
        else:
            print('バリデーションNG')
            print(form.errors)
            messages.add_message(request, messages.INFO, form.errors)

        return redirect('shop:products')

CategoryChild = ProductCategoryChildView.as_view()

class ProductImagesView(View):
    def post(self, request, *args, **kwargs):

        print(request.POST)
        print(request.FILES)

        form = ProductsImageForm(request.POST, request.FILES)

        if form.is_valid():

            print('バリデーションOK')
            messages.info(request, "バリデーションOK")

            form.save()

        else:

            print('バリデーションNG')
            print(form.errors)
            messages.add_message(request, messages.INFO, form.errors)

        data = {"error": True}

        from django.http import JsonResponse

        return JsonResponse(data)

ProductsImages = ProductImagesView.as_view()

class CategoryView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        # context['category'] = ProductCategory.objects.filter(id=pk).first()
        # context['category'] = ProductCategory.objects.all()
        context['category'] = ProductCategoryChild.objects.filter(id=pk).first()
        context['category'] = ProductCategoryChild.objects.all()
        context['categories'] = ProductCategoryParent.objects.filter(id=pk).first()
        context['categories'] = ProductCategoryParent.objects.all()
        context['products'] = Product.objects.filter(category_id=pk)
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        sort_list = [
            {"key": "price", "value": "値段が安い順"},
            {"key": "-price", "value": "値段が高い順"},
            {'key': 'dt', 'value': '最新順'},
        ]

        keys = [s["key"] for s in sort_list]


        context["sort_list"] = sort_list

        #並び替えが指定されている。

        if "order_by" in request.GET:

            #その並び替えが指定のリストの中にある。

            if request.GET["order_by"] in keys:

                context["products"] = Product.objects.filter(category_id=pk).order_by(request.GET["order_by"])
            else:
                context['products'] = Product.objects.filter(category_id=pk)
        else:
            context['products'] = Product.objects.filter(category_id=pk)

        return render(request, 'shop/home.html', context)

Category = CategoryView.as_view()

class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['products'] = Product.objects.filter(id=pk).first()
        # context['images'] = ProductImage.objects.filter(product_id=pk)
        context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, 'shop/product_detail.html', context)

    def post(self, request, pk, *args, **kwargs):

        # ここでユーザーのカートへ追加
        if request.user.is_authenticated:
            # TIPS:ここで既に同じ商品がカートに入っている場合、レコード新規作成ではなく、既存レコードにamount分だけ追加する。
            copied = request.POST.copy()

            copied["user"] = request.user.id
            copied["product"] = pk

            form = CartForm(copied)

            if not form.is_valid():
                print("バリデーションNG")
                return redirect("shop:product_detail", pk)

            # print("バリデーションOK")

            # TIPS:ここで既に同じ商品がカートに入っている場合、レコード新規作成ではなく、既存レコードにamount分だけ追加する。
            cart = Cart.objects.filter(user=request.user.id, product=pk).first()

            if cart:
                cleaned = form.clean()

                # TODO:ここでカートに数量を追加する時、追加される数量が在庫数を上回っていないかチェックする。上回る場合は拒否する。
                stock = Product.objects.filter(id=pk).first().stock

                if stock >= cart.amount + cleaned["amount"]:
                    # カート内商品は在庫数以下につき、保存OK
                    cart.amount += cleaned["amount"]
                    cart.save()

                else:
                    print("在庫数を超過しているため、カートに追加できません。")

            else:
                # 存在しない場合は新規作成
                form.save()

        else:
            print("未認証です")
            return redirect('account_login')
            # TODO:未認証ユーザーにはCookieにカートのデータを格納するのも良い

        return redirect("shop:product_detail", pk)

ProductsDetail = ProductDetailView.as_view()

class ProductEditView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['products'] = Product.objects.filter(id=pk).first()
        context['category'] = ProductCategoryChild.objects.all()


        return render(request, 'shop/edit.html', context)

    def post(self, request, pk, *args, **kwargs):

        product = Product.objects.filter(id=pk).first()

        form = ProductEditForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            print('バリデーションOK')
            form.save()
        else:
            print('バリデーションNG')
            print(form.errors)

        return redirect('shop:edit', pk)

Edit = ProductEditView.as_view()

class CartView(View):

    def get(self, request, *args, **kwargs):
        #ここでカートの中身を表示

        context = {}

        if request.user.is_authenticated:

            carts = Cart.objects.filter(user=request.user.id)
            context["num"] = Cart.objects.filter(user=request.user.id).count()
            context['category'] = ProductCategoryChild.objects.all()

            context["total"] = 0
            for cart in carts:
                context["total"] += cart.get_total_price()

            context["carts"] = carts

        else:
            #TODO:未認証ユーザーにはCookie格納されたカートのデータを表示するのも良い
            context = {}

            context["num"] = Cart.objects.filter(user=request.user.id).count()

        return render(request, "shop/cart.html", context)

cart = CartView.as_view()

class CartEditView(View):
    def get(self, request, pk, *args, **kwargs):

        context = {}

        context['products'] = Cart.objects.filter(product=pk).first()

        return render(request, "shop/cart.html", context)

    def post(self, request, pk, *args, **kwargs):

        product = Cart.objects.filter(user=request.user.id, product=pk).first()

        copied = request.POST.copy()
        copied["user"] = request.user.id

        form = CartForm(copied, instance=product)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)

            return redirect("shop:cart")

        cart = Cart.objects.filter(user=request.user.id, product=pk).first()

        if cart:

            cleaned = form.clean()

            # TODO:数量0であれば削除する
            if cleaned["amount"] == 0:
                cart.delete()

                return redirect("shop:cart")

            if cart.amount_change(cleaned["amount"]):

                # もし数量が規定値であれば編集して保存する。
                form.save()

            else:
                print("数量が在庫数を超過。")
        else:

            # TODO:未認証ユーザーにはCookie格納された内容を処理
            pass

        return redirect('shop:cart')

CartEdit = CartEditView.as_view()

class DeleteView(View):
    def post(self, request, pk, *args, **kwargs):

        product = Cart.objects.filter(product=pk).first()

        if product:
            print("削除")
            product.delete()
        else:
            print("対象のデータは見つかりませんでした。")

        return redirect("shop:cart")

Delete = DeleteView.as_view()

class ContactView(View):
    def get(self, request, *args, **kwargs):

        user = CustomUser.objects.all()
        content = Contacts.objects.all()

        context = {'contents': content,
                   'users': user}

        return render(request, 'shop/contact.html', context)

    def post(self, request, *args, **kwargs):

        copied = request.POST.copy()
        copied['user_id'] = request.user.id

        form = ContactsForm(copied)

        if form.is_valid():
            print('バリデーションOK')
            form.save()
        else:
            print('バリデーションNG')
            print(form.errors)

        return redirect('shop:contact')

Contact = ContactView.as_view()