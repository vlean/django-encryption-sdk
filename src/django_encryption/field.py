from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from django_encryption.aes import crypto

"""
enum 内建脱敏类型，address、phone、money、card number
"""


class DataKeeper(object):
    def __init__(self, plain_text=None, cipher_text=None) -> None:
        self.plain_text = plain_text
        self.cipher_text = cipher_text

    def plain(self):
        """
        获取原始明文，增加额外记录
        """
        if self.plain_text is not None:
            return self.plain_text
        if self.cipher_text is not None:
            return crypto.decrypt(self.cipher_text)
        return None

    def cipher(self):
        """
        获取密文
        """
        if self.cipher_text is not None:
            return self.cipher_text
        if self.plain_text is not None:
            self.cipher_text = crypto.encrypt(self.plain_text)
            return self.cipher_text
        return None

    def mask(self):
        """
        获取掩码信息
        """
        plain_info = self.plain()
        # 遮盖中间部分数据 or 根据类型遮挡
        # todo check字符数or字节数
        if len(plain_info) > 10:
            return plain_info[:3] + "****" + plain_info[-4:]
        else:
            return "****"

    def __str__(self) -> str:
        return self.mask()

    def __repr__(self) -> str:
        return self.mask()


class EncryptCharField(CharField):
    description = _("Encrypt String (base CharField)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    # 回显python
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            return crypto.decrypt(value)
        return str(value)

    # 录入db
    def get_prep_value(self, value):
        # encode
        return crypto.encrypt(value)


class DataKeeperCharField(CharField):
    description = _("Plain Data Keeper String (base CharField)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    # 回显python
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, DataKeeper):
            return value

        return DataKeeper(cipher_text=value)

    # 录入db
    def get_prep_value(self, value):
        # encode
        if value is None:
            return ""
        if isinstance(value, DataKeeper):
            return value.cipher()

        dk = DataKeeper(plain_text=value)
        return dk.cipher()


