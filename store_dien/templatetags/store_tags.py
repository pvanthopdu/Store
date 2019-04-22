from django import template
from ..models import Branch, Warehouse

register = template.Library()

@register.inclusion_tag('sites/menu_item.html', name = 'branch')
def branch_tag():
    branch = Branch.objects.exclude(id = 1)
    return {'branch': branch}

@register.inclusion_tag('sites/select_branch.html', name = 'select_branch')
def select_branch_tag():
    branchs = Branch.objects.all()
    return {'branchs': branchs}

@register.inclusion_tag('sites/info_branch.html',name='info_branchs')
def sum_branch_pri(branch_name):
    amount = 0
    value = 0
    branchs = Warehouse.objects.filter(branch= Branch.objects.get(branch_name= branch_name))
    for branch in branchs:
        amount += branch.amount
        value += branch.amount* branch.good.good_price
    return {
        'amount' : amount,
        'value': value
    }
