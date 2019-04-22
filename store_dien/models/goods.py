from django.db import  models

class Goods(models.Model):
    UNIT = (
        ('Cái', 'Cái'),
        ('Bộ', 'Bộ'),
        ('Thùng', 'Thùng'),
        ('Hộp', 'Hộp'),
        ('Gói', 'Gói'),
        ('kg','kg'),
        ('Mét', 'Mét')
    )
    STATUS = (
        ('Hàng mới', 'Hàng mới'),
        ('Hàng đã qua sử dụng', 'Hàng đã qua sử dụng')
    )

    good_id = models.CharField(max_length=50, verbose_name='Mã hàng hóa', primary_key=True)
    good_name = models.TextField(verbose_name='Tên vật tư')
    good_unit = models.TextField(choices=UNIT, verbose_name='Đơn vị tính')
    good_manufacturing = models.CharField(max_length=50, verbose_name="Nơi sản xuất")
    good_status = models.TextField(choices=STATUS, verbose_name='Tình trạng vật tư')
    good_price = models.PositiveIntegerField(default=0)

    def __str__(self):  # __unicode__ for Python 2
        return self.good_name