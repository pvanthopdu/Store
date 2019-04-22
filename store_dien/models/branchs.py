from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    branch_name = models.CharField(max_length=50, verbose_name='Tên kho chi nhánh')
    branch_address = models.TextField(verbose_name='Địa chỉ kho chi nhánh')
    branch_admin = models.ForeignKey(User, verbose_name='Nhân viên quản trị chi nhánh',
                                     related_name='user_admin',
                                     on_delete=models.SET_NULL, null=True )

    def __str__(self):
        return self.branch_name

