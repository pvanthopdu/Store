from django import forms
from ..models import History_deal
from ..models import Branch

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History_deal
        fields = '__all__'
        exclude = ['user_created']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ware_source'].initial = Branch.objects.get(id=1)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['status'].widget.attrs.update({'class': ''})
