from django.db import models
from ..models.goods import Goods
from .branchs import Branch
class Warehouse(models.Model):

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,
                              verbose_name='Kho lưu trữ')
    good = models.ForeignKey(Goods,
                                   verbose_name='Vật tư', null=True, on_delete=models.SET_NULL)
    amount = models.PositiveSmallIntegerField(default=1,verbose_name='Số lượng')

    def __str__(self):
        return self.branch.branch_name
