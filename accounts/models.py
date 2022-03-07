from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone

from django.conf import settings

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid

class CustomUserAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザーID')
    main = models.BooleanField(verbose_name="メイン住所", default=False)
    name = models.CharField(verbose_name='名前', max_length=30, blank=False, null=True)
    prefcode = models.CharField(verbose_name='郵便番号', max_length=8, blank=False, null=True)
    address1 = models.CharField(verbose_name='都道府県', max_length=40, blank=False, null=True)
    address2 = models.CharField(verbose_name='市区町村名', max_length=40, blank=False, null=True)
    address3 = models.CharField(verbose_name='町域名', max_length=40, blank=False, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(
                    _('username'),
                    max_length=150,
                    unique=True,
                    help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                    validators=[username_validator],
                    error_messages={
                        'unique': _("A user with that username already exists."),
                    },
                )
    phone_number = models.CharField(verbose_name='電話番号', max_length=40, blank=True, null=True)
    email = models.EmailField(verbose_name='メールアドレス', unique=True,
                              error_messages={
                                  'unique': ("同一のメールアドレスが既に登録されています"),
                              }, )
    name = models.CharField(verbose_name='名前', blank=False, max_length=30)
    name_kana = models.CharField(verbose_name='名前(ふりがな)', blank=False, max_length=60)
    is_staff = models.BooleanField(
                    _('staff status'),
                    default=False,
                    help_text=_('Designates whether the user can log into this admin site.'),
                )
    is_active = models.BooleanField(
                    _('active'),
                    default=True,
                    help_text=_(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                    ),
                )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ["name", "name_kana", "email"]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def addresses(self):
        return CustomUserAddress.objects.filter(user_id=self.id)

    def __str__(self):
        return self.username