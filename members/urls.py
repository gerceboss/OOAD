from django.urls import path

from members.views import adminLoggedIn, auctionPortalItems
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clientLogin/',views.clientLogin, name='clientLogin'),
    path('clientRegister/',views.clientRegister, name='clientRegister'),
    path('adminLogin/',views.adminLogin, name='adminLogin'),
    path('adminRegister/',views.adminRegister, name='adminRegister'),
    path('adminLoggedIn/',views.adminLoggedIn, name='adminLoggedIn'),
    path('clientLoggedIn/',views.clientLoggedIn, name='clientLoggedIn'),
    path('clientRegistered/',views.clientRegistered, name='clientRegistered'),
    path('adminRegistered/',views.adminRegistered, name='adminRegistered'),
    path('auctionPortalItems/',views.auctionPortalItems,name='auctionPortalItems'),
    path('bidUpdate/',views.bidUpdate,name='bidUpdate'),
    path('itemAdded/',views.itemAdded,name='itemAdded'),
    path('bidRequest/',views.bidRequest, name='bidRequest'),
    path('bidAccept/',views.bidAccept, name='bidAccept'),
    path('bidReject/',views.bidReject, name='bidReject'),
    path('about/',views.first, name="first"),
    path('addItem/',views.addItem, name="addItem"),
    path('myProfile/',views.myProfile, name='myProfile'),
    path('balanceUpdate/',views.balanceUpdate, name='balanceUpdate'),
    path('connect-wallet/', views.wallet_view, name='connect-wallet'),
    path('transfer-ethers/', views.form_view,name='transfer-ethers'),
    ]
