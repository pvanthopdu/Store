from .models import History_deal, Branch
from django.http import HttpResponseRedirect
from django.contrib import messages

def user_permit(function):
    def wrap(request, *args, **kwargs):
        deal = History_deal.objects.get(pk=kwargs['deal_id'])
        if deal.user_created == request.user or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            messages.error(request,"Bạn không có quyền với chức năng này")
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_active(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            messages.error(request,"Bạn không có quyền với chức năng này")
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

