from django import forms
from ..models import History_deal
from ..models import Branch,Warehouse
from django.http import HttpResponse

class HistoryformAdmin(forms.ModelForm):
    class Meta:
        model = History_deal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ware_source'].initial = Branch.objects.get(id=1)

    def save(self, commit=True):
        if self.cleaned_data['status'] == True:

            record_source = Warehouse.objects.filter(good=self.cleaned_data['good'],
                                                     store=self.cleaned_data['ware_source']).first()
            if record_source:
                amount_source = record_source.amount
                if self.cleaned_data['tyles'] == 0:
                    record_source.amount = amount_source + self.amount
                    record_source.save()
                elif (self.cleaned_data['tyles'] == 1 or self.cleaned_data['tyles'] == 2):
                    if amount_source > self.cleaned_data['amount']:
                        record_des = Warehouse.objects.filter(good=self.cleaned_data['good'],
                                                              store=self.cleaned_data['ware_des']).first()
                        if record_des:
                            record_des.amount += self.cleaned_data['amount']
                        else:
                            record_des.amount = self.cleaned_data['amount']
                        record_source.amount -= self.cleaned_data['amount']
                        record_des.save()
                        record_source.save()
                    else:
                        self.cleaned_data['status'] = False
                        raise ValueError("Số lượng vượt quá kho hiện có")
                else:
                    record_source.amount = amount_source + self.cleaned_data['amount']
                    record_source.save()
        else:
            record = Warehouse(store=self.cleaned_data['ware_des'], good=self.cleaned_data['good'],
                               amount=self.cleaned_data['amount'])
            record.save()

        super().save()
