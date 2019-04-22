from datetime import datetime
from django.contrib.auth import authenticate, login as user_login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from .forms import HistoryForm
from .models import Warehouse
from django.contrib import messages
from .models import History_deal, Branch

from django.contrib.auth.decorators import login_required
from .decorators import *
from django.db.models import Q

# function ajax
def homeajax(request):
    return render(request, 'sites/homeajax.html')


def loadhomeajax(request):
    search = request.GET.get('search')
    search = search.strip()
    style = request.GET.get('style')
    status = request.GET.get('status')

    deals = list()

    if search == "":
        dealquery = History_deal.objects.all().order_by('-time_deal')
    else:
        dealquery = History_deal.objects.filter(good__good_name__icontains=search).order_by('-time_deal')
    if style != "":
        if int(style) <= 2:
            dealquery = dealquery.filter(tyles=int(style))
    if status != 'null' and status != '':
        if int(status) < 2:
            dealquery = dealquery.filter(status=int(status))

    # phan trang
    # get page from user
    page = request.GET.get('page', 1)
    # show number item per page
    paginator = Paginator(dealquery, 10)
    # get content of page
    try:
        deals_page = paginator.get_page(page)
    except PageNotAnInteger:
        deals_page = paginator.get_page(1)
    except EmptyPage:
        deals_page = paginator.get_page(paginator.num_pages)

    for item in deals_page:
        if item.tyles == 0:
            style_i = "Nhập kho"
        elif item.tyles == 1:
            style_i = "Xuất cấp"
        else:
            style_i = "Bán"
        deal = [item.id, item.time_deal.strftime("%d-%m-%Y %H:%M"),
                item.good.good_id, item.good.good_name, item.amount, style_i, item.status]
        deals.append(deal)

    data = {
        'deals': deals,
        'pages': deals_page.paginator.num_pages,
        'page': page
    }
    return JsonResponse(data)


def ajaxactive(request, deal_id):
    is_active = False
    deal = History_deal.objects.get(pk=deal_id)
    record_source = Warehouse.objects.filter(good=deal.good,
                                             branch=deal.ware_source).first()
    if record_source:
        amount_source = record_source.amount
        if deal.tyles == 0:
            record_source.amount += deal.amount
            if deal.ware_source.pk != 1 or deal.ware_des != deal.ware_source:
                messages = "Giao dịch nhập kho chỉ cho nhập vào kho tổng. Giao dịch không được kích hoạt"
            else:
                record_source.save()
                deal.status = True
                deal.save()
                messages = "Giao dịch đã kích hoạt thành công"
                is_active = True
        else:
            record_des = Warehouse.objects.filter(good=deal.good,
                                                  branch=deal.ware_des).first()
            amount_des = deal.amount
            if amount_source >= amount_des:
                if record_des:
                    record_des.amount += amount_des
                    record_source.amount -= amount_des
                    record_source.save()
                    record_des.save()
                    messages = "Giao dịch đã kích hoạt thành công"
                    # return HttpResponseRedirect("/")
                else:
                    record = Warehouse(store=deal.ware_des, good=deal.good,
                                       amount=deal.amount)
                    record.save()
                    messages = "Giao dịch đã kích hoạt thành công"
                    # return HttpResponseRedirect("/")
                deal.status = True
                deal.save()
                is_active = True

            else:
                messages = "Số lượng vượt quá kho đang có. Giao dịch không được kích hoạt"

    else:
        if deal.ware_source.pk != 1 or deal.ware_des != deal.ware_source:
            messages = "Vật tư giao dịch chưa có trong kho nguồn. Giao dịch không được kích hoạt"
        else:
            record = Warehouse(branch=deal.ware_des, good=deal.good,
                               amount=deal.amount)
            record.save()
            deal.status = True
            deal.save()
            messages = "Giao dịch đã kích hoạt thành công"
            is_active = True

    data = {
        'active': is_active,
        'messages': messages
    }
    return JsonResponse(data)


# function view home
def home(request):
    if request.method == "POST":
        search_name = request.POST.get('search_name')
        style = request.POST.get('style')
        status = request.POST.get('status')
        if search_name != "":
            deals = History_deal.objects.filter(good__good_name__icontains=search_name).order_by('-time_deal')
        else:
            deals = History_deal.objects.all().order_by('-time_deal')
        if style != None:
            if int(style) <= 3:
                deals = deals.filter(tyles=int(style))
        if status != None:
            if int(status) < 2:
                deals = deals.filter(status=int(status))

    else:
        deals = History_deal.objects.all().order_by('-time_deal')

    page = request.GET.get('page', 1)
    paginator = Paginator(deals, 5)

    try:
        deals_page = paginator.get_page(page)
    except PageNotAnInteger:
        deals_page = paginator.get_page(1)
    except EmptyPage:
        deals_page = paginator.get_page(paginator.num_pages)

    return render(request, 'sites/home.html', {'deals': deals_page})


@login_required(login_url='/')
def add_deal(request):
    header = "Thêm giao dịch"
    deal = HistoryForm()
    content = {
        'deal': deal,
        'header': header
    }
    if request.method == 'POST':
        deal = HistoryForm(request.POST)
        if deal.is_valid():

            record_source = Warehouse.objects.filter(good=deal.cleaned_data['good'],
                                                     branch=deal.cleaned_data['ware_source']).first()
            if record_source:
                amount_source = record_source.amount
                if deal.cleaned_data['tyles'] == 0:
                    if deal.cleaned_data['ware_source'].pk != 1 or \
                                    deal.cleaned_data['ware_des'] != deal.cleaned_data['ware_source']:
                        messages.error(request, "Giao dịch nhập kho chỉ cho nhập vào kho tổng. "
                                                "Vui lòng chọn kho nguồn và kho đích là kho tổng")
                        deal.add_error('ware_des', "Kho nguồn chưa trùng với kho đích")
                    else:
                        if deal.cleaned_data['status'] == True:
                            record_source.amount += deal.cleaned_data['amount']
                            record_source.save()

                        deal = deal.save(commit=False)
                        deal.user_created = request.user
                        deal.save()
                        messages.success(request, "Một giao dịch đã thực hiện thành công")
                        return HttpResponseRedirect("/")
                else:
                    if deal.cleaned_data['ware_source'] == deal.cleaned_data['ware_des']:
                        messages.error(request, "Chọn kho nguồn và kho đích phải khác nhau.")
                        deal.add_error('ware_des', "Kho nguồn và kho đích phải khác nhau.")
                        deal.add_error('ware_source', "Kho nguồn và kho đích phải khác nhau.")

                    else:
                        if deal.cleaned_data['tyles'] == 3:
                            if deal.cleaned_data['ware_des'].pk != 1:
                                messages.error(request, "Chọn kho đích là kho tổng trong giao dịch chuyển trả.")
                                deal.add_error('ware_des', "Chọn kho đích là kho tổng")
                                return render(request, 'sites/add_deal01.html', content)

                        record_des = Warehouse.objects.filter(good=deal.cleaned_data['good'],
                                                              branch=deal.cleaned_data['ware_des']).first()
                        amount_des = deal.cleaned_data['amount']
                        if amount_source >= amount_des:
                            if deal.cleaned_data['status'] == True:
                                if record_des:
                                    record_des.amount += amount_des
                                    record_source.amount -= amount_des
                                    record_source.save()
                                    record_des.save()
                                else:
                                    record = Warehouse(branch=deal.cleaned_data['ware_des'],
                                                       good=deal.cleaned_data['good'],
                                                       amount=deal.cleaned_data['amount'])
                                    record.save()
                            deal = deal.save(commit=False)
                            deal.user_created = request.user
                            deal.save()
                            messages.success(request, "Một giao dịch đã thực hiện thành công")
                            return HttpResponseRedirect("/")

                        else:
                            messages.error(request, "Số lượng vượt quá kho đang có")
                            deal.add_error('amount', "Số lượng vượt quá kho đang có")

            else:
                if deal.cleaned_data['ware_source'].pk != 1 or \
                                deal.cleaned_data['ware_des'] != deal.cleaned_data['ware_source']:
                    messages.error(request,
                                   "Kho nguồn chưa có vật tư này. Chọn nhập vật tư này vào kho tổng trước.")

                    deal.add_error('ware_des', "Kho nguồn chưa trùng với kho đích")
                else:
                    if deal.cleaned_data['status'] == True:
                        record = Warehouse(branch=deal.cleaned_data['ware_des'], good=deal.cleaned_data['good'],
                                           amount=deal.cleaned_data['amount'])
                        record.save()

                    deal = deal.save(commit=False)
                    deal.user_created = request.user
                    deal.save()
                    messages.success(request, "Một giao dịch đã thực hiện thành công")
                    return HttpResponseRedirect("/")
                    # else:
                    #     deal.save()
                    #     messages.success(request, "Một giao dịch đã thực hiện thành công, nhưng chưa kích hoạt")
                    #     return HttpResponseRedirect("/")

    return render(request, 'sites/add_deal01.html', content)


@login_required(login_url='/')
@user_active
def active_deal(request, deal_id):
    deal = History_deal.objects.get(pk=deal_id)
    record_source = Warehouse.objects.filter(good=deal.good,
                                             branch=deal.ware_source).first()
    if record_source:
        amount_source = record_source.amount
        if deal.tyles == 0:
            record_source.amount += deal.amount
            if deal.ware_source.pk != 1 or deal.ware_des != deal.ware_source:
                messages.error(request, "Giao dịch nhập kho chỉ cho nhập vào kho tổng. "
                                        "Giao dịch không được kích hoạt")
            else:
                record_source.save()
                deal.status = True
                deal.save()
                messages.success(request, "Giao dịch đã kích hoạt thành công")
                # return HttpResponseRedirect("/")
        else:
            if deal.ware_source == deal.ware_des:
                messages.error(request, "Chọn kho nguồn và kho đích phải khác nhau.")

            else:
                if deal.cleaned_data['tyles'] == 3:
                    if deal.ware_des.pk != 1:
                        messages.error(request, "Chọn kho đích là kho tổng trong giao dịch chuyển trả.")
                        return HttpResponseRedirect("/")

                record_des = Warehouse.objects.filter(good=deal.good,
                                                      branch=deal.ware_des).first()
                amount_des = deal.amount
                if amount_source >= amount_des:
                    if record_des:
                        record_des.amount += amount_des
                        record_source.amount -= amount_des
                        record_source.save()
                        record_des.save()
                        messages.success(request, "Giao dịch đã kích hoạt thành công")
                        # return HttpResponseRedirect("/")
                    else:
                        record = Warehouse(branch=deal.ware_des, good=deal.good,
                                           amount=deal.amount)
                        record.save()
                        messages.success(request, "Giao dịch đã kích hoạt thành công")
                        # return HttpResponseRedirect("/")
                    deal.status = True
                    deal.save()

                else:
                    messages.error(request, "Số lượng vượt quá kho đang có. Giao dịch không được kích hoạt")

    else:
        if deal.ware_source != 1 or deal.ware_des != deal.ware_source:
            messages.error(request, "Giao dịch nhập kho chỉ cho nhập vào kho tổng. "
                                    "Giao dịch không được kích hoạt")
        else:
            record = Warehouse(branch=deal.ware_des, good=deal.good,
                               amount=deal.amount)
            record.save()
            deal.status = True
            deal.save()
            messages.success(request, "Giao dịch đã kích hoạt thành công")
    return HttpResponseRedirect("/")


@login_required(login_url='/')
@user_permit
def edit_deal(request, deal_id):
    header = "Edit giao dịch"
    dealinit = History_deal.objects.get(pk=deal_id)
    formDeal = HistoryForm(instance=dealinit)
    content = {
        'deal': formDeal,
        'header': header
    }
    if formDeal.has_changed():
        if request.method == 'POST':
            deal = HistoryForm(request.POST)
            if deal.is_valid():
                if deal.cleaned_data['status'] == True:
                    record_source = Warehouse.objects.filter(good=deal.cleaned_data['good'],
                                                             branch=deal.cleaned_data['ware_source']).first()
                    if record_source:
                        amount_source = record_source.amount
                        if deal.cleaned_data['tyles'] == 0:
                            record_source.amount += deal.cleaned_data['amount']
                            if deal.cleaned_data['ware_source'].pk != 1 or \
                                            deal.cleaned_data['ware_des'] != deal.cleaned_data['ware_source']:
                                messages.error(request, "Giao dịch nhập kho chỉ cho nhập vào kho tổng. "
                                                        "Vui lòng chọn kho nguồn và kho đích là kho tổng")
                                deal.add_error('ware_des', "Kho nguồn chưa trùng với kho đích")
                            else:
                                record_source.save()
                                # dealinit.time_deal = deal.cleaned_data['time_deal']
                                dealinit.good = deal.cleaned_data['good']
                                dealinit.tyles = deal.cleaned_data['tyles']
                                dealinit.ware_source = deal.cleaned_data['ware_source']
                                dealinit.ware_des = deal.cleaned_data['ware_des']
                                dealinit.amount = deal.cleaned_data['amount']
                                dealinit.status = deal.cleaned_data['status']
                                dealinit.save()
                                messages.success(request, "Cập nhật giao dịch đã thực hiện thành công")
                                return HttpResponseRedirect("/")
                        else:
                            if deal.cleaned_data['tyles'] == 3:
                                if deal.cleaned_data['ware_des'].pk != 1:
                                    messages.error(request,
                                                   "Chọn kho đích là kho tổng trong giao dịch chuyển trả.")
                                    return render(request, 'sites/add_deal01.html', content)

                            record_des = Warehouse.objects.filter(good=deal.cleaned_data['good'],
                                                                  branch=deal.cleaned_data['ware_des']).first()
                            amount_des = deal.cleaned_data['amount']
                            if amount_source >= amount_des:
                                if record_des:
                                    record_des.amount += amount_des
                                    record_source.amount -= amount_des
                                    record_source.save()
                                    record_des.save()

                                else:
                                    record = Warehouse(branch=deal.cleaned_data['ware_des'],
                                                       good=deal.cleaned_data['good'],
                                                       amount=deal.cleaned_data['amount'])
                                    record.save()

                                # dealinit.time_deal = deal.cleaned_data['time_deal']
                                dealinit.good = deal.cleaned_data['good']
                                dealinit.tyles = deal.cleaned_data['tyles']
                                dealinit.ware_source = deal.cleaned_data['ware_source']
                                dealinit.ware_des = deal.cleaned_data['ware_des']
                                dealinit.amount = deal.cleaned_data['amount']
                                dealinit.status = deal.cleaned_data['status']
                                dealinit.save()
                                messages.success(request, "Cập nhật giao dịch đã thực hiện thành công")
                                return HttpResponseRedirect("/")
                            else:
                                messages.error(request, "Số lượng vượt quá kho đang có")
                                deal.add_error('amount', "Số lượng vượt quá kho đang có")

                    else:
                        if deal.cleaned_data['ware_source'].pk != 1 or \
                                        deal.cleaned_data['ware_des'] != deal.cleaned_data['ware_source']:
                            messages.error(request, "Giao dịch nhập kho chỉ cho nhập vào kho tổng. "
                                                    "Vui lòng chọn kho nguồn và kho đích là kho tổng")
                            deal.add_error('ware_des', "Kho nguồn chưa trùng với kho đích")
                        else:
                            record = Warehouse(branch=deal.cleaned_data['ware_des'], good=deal.cleaned_data['good'],
                                               amount=deal.cleaned_data['amount'])
                            record.save()
                            # dealinit.time_deal = deal.cleaned_data['time_deal']
                            dealinit.good = deal.cleaned_data['good']
                            dealinit.tyles = deal.cleaned_data['tyles']
                            dealinit.ware_source = deal.cleaned_data['ware_source']
                            dealinit.ware_des = deal.cleaned_data['ware_des']
                            dealinit.amount = deal.cleaned_data['amount']
                            dealinit.status = deal.cleaned_data['status']
                            dealinit.save()
                            messages.success(request, "Cập nhật giao dịch đã thực hiện thành công")
                            return HttpResponseRedirect("/")
                else:
                    dealinit.good = deal.cleaned_data['good']
                    dealinit.tyles = deal.cleaned_data['tyles']
                    dealinit.ware_source = deal.cleaned_data['ware_source']
                    dealinit.ware_des = deal.cleaned_data['ware_des']
                    dealinit.amount = deal.cleaned_data['amount']
                    dealinit.status = deal.cleaned_data['status']
                    dealinit.save()
                    messages.success(request,
                                     "Cập nhật giao dịch đã thực hiện thành công, nhưng chưa kích hoạt")
                    return HttpResponseRedirect("/")

        return render(request, 'sites/add_deal01.html', content)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username.strip(), password=password)
        if user is not None:
            user_login(request, user)
            messages.info(request, "You are already login successfully.")
        else:
            messages.error(request, "Please enter a correct username and password.")
    return HttpResponseRedirect("/")


# statistical the branchs
def statistical_branch(request, branch_id):
    if request.method == "POST":
        search_name = request.POST.get('search_name')
        if search_name.strip() != "":
            store = Warehouse.objects.filter(branch=Branch.objects.get(pk=branch_id),
                                             good__good_name__icontains=search_name)
        else:
            store = Warehouse.objects.filter(branch=Branch.objects.get(pk=branch_id))
    else:
        store = Warehouse.objects.filter(branch=Branch.objects.get(pk=branch_id))

    sumamount = 0
    for item in store:
        sumamount += item.amount

    page = request.GET.get('page', 1)
    paginator = Paginator(store, 10)

    try:
        store_page = paginator.get_page(page)
    except PageNotAnInteger:
        store_page = paginator.get_page(1)
    except EmptyPage:
        store_page = paginator.get_page(paginator.num_pages)

    content = {
        'store': store_page,
        'branch_id': branch_id,
        'sum': sumamount
    }
    return render(request, 'sites/branchs.html', content)

def statistical(request):
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = request.POST.get('date_to')
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        branch_id = int(request.POST.get('branch'))
        branch_search = Branch.objects.get(pk=branch_id)
        if branch_search.branch_admin == request.user or request.user.is_superuser:
            deals = History_deal.objects.filter(status=True,
                                                time_deal__gte=date_from,
                                                time_deal__lte=date_to).order_by('-time_deal')
            deals = deals.filter(Q(ware_source=branch_search) |
                                 Q(ware_des=branch_search))

            value_in_pri = 0
            value_out = 0
            value_sale = 0
            value_return = 0
            exist_start = 0
            exist_end = 0

            for deal in deals:
                if deal.tyles == 0:
                    value_in_pri += deal.amount
                elif deal.tyles == 1:
                    value_out += deal.amount
                elif deal.tyles == 2:
                    value_sale += deal.amount
                else:
                    value_return += deal.amount

            branch_required = Warehouse.objects.filter(branch=Branch.objects.get(pk=branch_id))
            for item in branch_required:
                exist_end += item.amount

            if branch_id == 1:
                exist_start = exist_end - value_in_pri - value_return + value_out + value_sale
            else:
                exist_start = exist_end + value_return - value_out - value_sale

            content = {
                'deals': deals,
                'branch': branch_id,
                'value_in_pri': value_in_pri,
                'value_out': value_out,
                'value_sale': value_sale,
                'value_return': value_return,
                'exist_start': exist_start,
                'exist_end': exist_end
            }
            print(deals)
            return render(request, 'sites/statistical.html', content)
        else:
            messages.error(request, "Bạn không có quyền với chức năng này")

    return render(request, 'sites/statistical.html')
