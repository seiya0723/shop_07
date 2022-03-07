from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator

from django.conf import settings

import uuid

class ProductCategoryParent(models.Model):
    # 本格的な運用を試みるのであれば、自動採番で予測されやすい数値型の主キーではなく、不規則な文字列が生成されるUUID型の主キーを使用するとセキュリティが向上する。
    # https://ja.wikipedia.org/wiki/UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt = models.DateTimeField(verbose_name="登録日時", default=timezone.now)
    name = models.CharField(verbose_name="カテゴリ名", max_length=20, unique=True,
                            error_messages={
                                    'unique': ("同一のカテゴリーが既に登録されています"),
                                },)
    def __str__(self):
        return self.name

class ProductCategoryChild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt = models.DateTimeField(verbose_name="登録日時", default=timezone.now)
    category = models.ForeignKey(ProductCategoryParent, on_delete=models.CASCADE, verbose_name='カテゴリー')
    name = models.CharField(verbose_name="カテゴリー名", max_length=100, unique=True, error_messages={
                                    'unique': ("同一の商品が既に登録されています"),
                                },)
    def __str__(self):
        return self.name

class Product(models.Model):
    # 同じカテゴリと同じ商品名の組み合わせの登録は禁止にする。unique_togetherを使用する。
    # 例:名前の重複を禁止する場合、便箋用の『マスキングテープ』と工具用の『マスキングテープ』が同時に登録できないため、カテゴリと名前の組み合わせでの重複を禁止にする。
    # https://noauto-nolife.com/post/django-same-user-operate-prevent/

    class Meta:
        unique_together = ("category", "name")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt = models.DateTimeField(verbose_name="登録日時", default=timezone.now)
    category = models.ForeignKey(ProductCategoryChild, verbose_name="カテゴリ", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="商品名", max_length=100, unique=True, error_messages={
                                    'unique': ("同一の商品が既に登録されています"),
                                },)
    description = models.CharField(verbose_name="商品説明", max_length=3000)
    price = models.PositiveIntegerField(verbose_name="価格")
    situation = models.BooleanField(verbose_name='販売状態')
    stock = models.PositiveIntegerField(verbose_name='在庫数')
    image = models.ImageField(verbose_name='サムネイル', upload_to="shop/product_image/images/")

    # 1対多で関連づいた画像を全て取り出し、モデルオブジェクトのリストを返却。テンプレートではこれをループして1枚ずつ画像を出す。
    def images(self):
        return ProductImage.objects.filter(product=self.id).order_by("dt")

    def single_img(self):
        return ProductImage.objects.filter(product=self.id).order_by("dt").first()

    def __str__(self):
        return self.name


# キャメルケースは↓のクラス名のように単語ごとに頭文字を大文字で連結する
class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt = models.DateTimeField(verbose_name="登録日時", default=timezone.now)

    # スネークケースでアプリ名/モデルクラス名/フィールド名に保存する。
    # スネークケースは単語ごとに_を入れて全て小文字で連結する。
    image = models.ImageField(verbose_name="商品画像", upload_to="shop/product_image/images/")

    # 画像を指定する。1対多を使う。
    # 理由:商品に指定する画像の個数は、後からフレキシブルに変更できるようにする必要がある。そのため、ProductにImageFieldを複数追加する方法は望ましくない。
    product = models.ForeignKey(Product, verbose_name="対象商品", on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt = models.DateTimeField(verbose_name="カート追加日時", default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="カート所有者", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="商品", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="商品の個数", default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.product.name

    def get_total_price(self):
        return self.product.price * self.amount


    def amount_change(self, after_value):
        if self.product.stock >= after_value:
            return True
        else:
            return False

class Contacts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザーID')
    dt = models.DateTimeField(verbose_name="お問い合わせ日時", default=timezone.now)
    name = models.CharField(verbose_name='名前', max_length=30)
    email = models.EmailField(verbose_name='メールアドレス', max_length=200)
    title = models.CharField(verbose_name='タイトル', max_length=100)
    contents = models.CharField(verbose_name='お問い合わせ内容', max_length=3000)

    def __str__(self):
        return self.title

class Like(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザーID')
    liked = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class FavoriteList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザーID')
    name = models.CharField(verbose_name='リスト名', max_length=100)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')

    def __str__(self):
        return self.name

