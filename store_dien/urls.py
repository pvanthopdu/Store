from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'store_dien'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_deal/', views.add_deal, name='add_deal'),
    path('active/<int:deal_id>', views.active_deal, name='active_deal'),
    path('edit/<int:deal_id>', views.edit_deal, name='edit_deal'),
    path('homeajax', views.homeajax, name='homeajax'),
    path('loadhomeajax', views.loadhomeajax, name='loadhomeajax'),
    path('activeajax/<int:deal_id>', views.ajaxactive, name='activeajax'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    #view the stores
    path('stores/<int:branch_id>', views.statistical_branch, name='stores'),
    path('statistical', views.statistical, name = 'statistical')
]
