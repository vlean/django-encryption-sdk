from django.db import models


# Create your models here.
from django_encryption.field import EncryptCharField, DataKeeperCharField


class User(models.Model):
    """
    用户基础信息
    """
    name = models.CharField(verbose_name="用户名", max_length=56)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    phone = EncryptCharField(verbose_name="手机号", blank=True, max_length=256)
    identity_number = DataKeeperCharField(verbose_name="身份证号", blank=True, max_length=256)

