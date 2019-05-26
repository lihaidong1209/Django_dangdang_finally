from django.contrib import admin
from django.urls import path
from orderapp import views

app_name = 'orderapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('car/', views.car,name='car'),
    path('indent/', views.indent,name='indent'),
    path('indent_ok/', views.indent_ok,name='indent_ok'),

    path('add_book/', views.add_book,name='add_book'),                          #增加一本书
    path('add_books/', views.add_books,name='add_books'),                         #增加多本书

    # 修改
    path('update_cart_add/', views.update_cart_add,name='update_cart_add'),       #增加一本书
    path('update_cart_red/', views.update_cart_red,name='update_cart_red'),       #减少一本书
    path('delete_cart_book/', views.delete_cart_book,name='delete_cart_book'),    #删除书
    path('update_cart_books/', views.update_cart_books,name='update_cart_books'),  #修改多本书

    # 恢复
    path('add_book_recover/', views.add_book_recover,name='add_book_recover'),     #移入到恢复区
    path('recover_book_cart/', views.recover_book_cart,name='recover_book_cart'),  #恢复到购物车

    # 判断购物车
    path('cart_settlement/', views.cart_settlement,name='cart_settlement'),  #判断购物车是否存在

# 选择用户地址
    path('select_address/', views.select_address,name='select_address'),  #选择用户地址
    path('add_user_address/', views.add_user_address,name='add_user_address'),  #新增用户地址

    #订单页面
    path('index_detail/', views.index_detail,name='index_detail'),  #订单页面

    #购物完成清除函数
    path('delete_information/', views.delete_information,name='delete_information'),  #清除历史

    path('order_detail/', views.order_detail,name='order_detail'),  #清除历史


]