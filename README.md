
## 使用阿里kms数据加密保护你的隐私数据

```python

class User(models.Model):
    """
    用户基础信息
    """
    name = models.CharField(verbose_name="用户名", max_length=56)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    phone = EncryptCharField(verbose_name="手机号", blank=True, max_length=256)
    identity_number = DataKeeperCharField(verbose_name="身份证号", blank=True, max_length=256)
```

```python
# 查询使用
user = User.objects.first()
user.phone # 明文使用，密文落库
user.identity_number # 默认掩码格式，需显式获取明文，密文落库
user.identity_number.plain() # 明文
user.identity_number.mask() # 掩码，默认
user.identity_number.cipher() # 密文
```