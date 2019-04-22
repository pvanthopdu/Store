from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from .branchs import Branch
from .goods import Goods
from django.contrib.auth.models import User

class History_deal(models.Model):
    TYLES = (
        (0, 'Nhập kho'),
        (1, 'Xuất cấp'),
        (2, 'Bán'),
        (3, 'Chuyển trả')
    )
    time_deal = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Thời gian giao dịch")
    good = models.ForeignKey(Goods, null=True, on_delete=models.SET_NULL,
                             verbose_name='Chọn vật tư')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name="Số lượng")
    tyles = models.PositiveSmallIntegerField(choices=TYLES, verbose_name="Chọn loại giao dịch")
    ware_source = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE,
                                    verbose_name="chọn kho nguồn",
                                    related_name='ware_source')
    ware_des = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE,
                                 verbose_name="Chọn kho đích", related_name='ware_des')

    status = models.BooleanField(default=False, verbose_name="Kích hoạt giao dịch",
                                 help_text="Nếu chọn giao dịch sẽ thực hiện, ngược lại giao dịch không thực hiện")
    user_created = models.ForeignKey(User, on_delete=models.CASCADE,
                                 verbose_name="Thành viên", related_name='user_created')

    def __str__(self):
        return self.good.good_name



