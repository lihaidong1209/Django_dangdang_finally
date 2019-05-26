from django.shortcuts import render,redirect,HttpResponse
from cartapp.cart import Cart
from django.db import transaction
from modelsapp.models import TBooks,TUser,TAddress,TOrder,TOrderitem
from django.http import JsonResponse
import random ,string
from datetime import datetime
# 购物车
def car(request):
    cart = request.session.get("cart")
    cart1 = request.session.get("cart1")
    book_ones,total_prices,save_prices ,book_twos,order_query= "","","","",""
    username = request.session.get("stats")
    if username:
        user_id = TUser.objects.filter(username=username)[0].id
        order_query = TOrder.objects.filter(user_id=user_id)
        order_ids=[]
        if order_query:
            if not cart:
                cart = Cart()
                #通过用户找到的多个query对象进行遍历出model
                for order_model in order_query:
                    #获得此用户对应的多个订单的id
                    order_ids.append(order_model.id)
                    # 将订单的id进行遍历，
                for order_id in order_ids:
                    # 找到对应的多个orderitem的query,并将其存入列表
                    item_query = TOrderitem.objects.filter(order_id=order_id)
                    #将orderitem的query进行遍历
                    for item_model in item_query:
                        # 得到书的id和对应数量
                        book_id = item_model.book_id
                        amount = item_model.book_num
                        #获得书的model
                        book_model = TBooks.objects.filter(id=book_id)[0]
                        cart.recover_book_to_carts(book_model, amount)
                book_ones = cart.cartitem
                total_prices = cart.total_price
                save_prices = cart.save_price
    if cart:
        book_ones = cart.cartitem
        total_prices = cart.total_price
        save_prices = cart.save_price
    if cart1:
        book_twos = cart1.cartitem_recover
    if cart and cart1:
        return render(request,'orderapp/car.html',{"book_ones":book_ones,"total_prices":total_prices,"save_prices":save_prices,"book_twos":book_twos})
    elif username and order_query and cart1:
        return render(request,'orderapp/car.html',{"book_ones":book_ones,"total_prices":total_prices,"save_prices":save_prices,"book_twos":book_twos})
    elif cart and not cart1 :
        return render(request,'orderapp/car.html',{"book_ones":book_ones,"total_prices":total_prices,"save_prices":save_prices})
    elif username and order_query and not cart:
        return render(request,'orderapp/car.html',{"book_ones":book_ones,"total_prices":total_prices,"save_prices":save_prices})
    elif not cart and cart1:
        return render(request, 'orderapp/car.html',{"book_twos": book_twos, "total_prices": total_prices, "save_prices": save_prices})
    return render(request, 'orderapp/car.html')

# 收货地址
def indent(request):
    username = request.session.get("stats")
    cart = request.session.get("cart")
    if username:
        if cart:
            user_id = TUser.objects.filter(username=username)[0].id
            user_addresss = TAddress.objects.filter(user_id=user_id)
            if user_addresss:
                return render(request, 'orderapp/indent.html',{"user_addresss":user_addresss})
        return render(request,"orderapp/indent.html")
    return redirect("/userapp/login/?flag=5")

def index_detail(request):
    '''
    订单详情页面渲染函数,此函数需要保存订单表和订单项表，一定要添加事务控制
    :param request:
    :return:
    '''
    try:
        with transaction.atomic():
            cart = request.session.get("cart")
            if cart:
                total_prices = cart.total_price
                save_prices = cart.save_price
                order_time = datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                request.session["order_time"] = order_time
                username = request.session.get("stats")
                #用户ID
                user_id = TUser.objects.filter(username=username)[0].id
                name = request.session.get("name")
                address_id = TAddress.objects.filter(name=name)[0].id
                # 存地址
                order_number = random.sample(string.digits, 9)
                order_number =int("".join(order_number))
                request.session["order_number"] = order_number
                # 生成订单表
                TOrder.objects.create(order_num=order_number,order_time=order_time,total_price=total_prices,address_id=address_id,user_id=user_id)
                order_id = TOrder.objects.filter(order_num=order_number)[0].id
                # 保存session中物品到购物车
                cart_settlements = cart.cartitem
                # 可以判断共有几种商品
                number = 0
                for books in cart_settlements:
                    number += 1
                    TOrderitem.objects.create(book_id=books.book.id,book_num=books.amount,order_id=order_id)
                request.session["number"] = number
                return render(request,"orderapp/indent_detail.html",{"total_prices":total_prices,"cart_settlements":cart_settlements,"number":number,"save_prices":save_prices,"order_number":order_number})
            return redirect("orderapp:car")
    except:
        return redirect("orderapp:indent")

# 购买成功
def indent_ok(request):
    try:
        with transaction.atomic():
            order_number = request.session.get("order_number")
            number = request.session.get("number")
            mob_phone = request.session.get("mob_phone")
            name = request.session.get("name")
            code = request.session.get("code")
            user_address = request.session.get("user_address")
            order_time = request.session.get("order_time")
            cart = request.session.get("cart")
            total_prices = cart.total_price
            return render(request,'orderapp/indent ok.html',{"order_number":order_number,"number":number,"name":name,"total_prices":total_prices,
                         "order_time":order_time,"user_address":user_address,"code":code,"mob_phone":mob_phone})
    except:
        return render(request,"")

# ==================================操作购物车书籍===============================================

# 增加一本书籍
def add_book(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    # print(cart)   #<cartapp.cart.Cart object at 0x0000024C8F71CE48>
    if cart:
        cart.add_book_to_cart(book_model)
    else:
        cart = Cart()
        cart.add_book_to_cart(book_model)
    request.session["cart"] = cart
    return JsonResponse({"result": 1})
# 增加多本书籍
def add_books(request):
    book_id = request.GET.get("id")
    amount = int(request.GET.get("amount"))
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    if cart:
        cart.add_book_to_carts(book_model,amount)
    else:
        cart = Cart()
        cart.add_book_to_carts(book_model,amount)
    request.session["cart"] = cart
    return JsonResponse({"result": 1})


# 增加一本书籍
def update_cart_add(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    cart.modify_cart_add(book_model)
    request.session["cart"] = cart
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices})


# 减少一本书籍
def update_cart_red(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    cart.modify_cart_red(book_model)
    request.session["cart"] = cart
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices})
# 更新多本书籍
def update_cart_books(request):
    book_id = request.GET.get("id")
    amount = int(request.GET.get("amount"))
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    cart.modify_cart_books(book_model,amount)
    request.session["cart"] = cart
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices})

# 删除书籍
def delete_cart_book(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")
    cart.delete_book(book_model)
    request.session["cart"] = cart
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices})

# 添加到恢复区
def add_book_recover(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")   #购物车
    cart1 = request.session.get("cart1")   #恢复区
    if cart1:
        cart1.add_book_to_recover(book_model)
    else:
        cart1 = Cart()
        cart1.add_book_to_recover(book_model)
    cart.delete_book(book_model)
    request.session["cart"] = cart
    request.session["cart1"] = cart1
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price

    book_id = book_model.id
    book_name = book_model.book_name
    book_picture = book_model.book_picture
    book_author = book_model.book_author
    discount_price = book_model.discount_price
    pub_time = book_model.pub_time.strftime("%Y-%m-%d")
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices,
                         "book_id": book_id,"book_name": book_name,"book_picture": book_picture,
                         "book_author": book_author, "discount_price": discount_price,"pub_time":pub_time})

# 添加到购物车
def recover_book_cart(request):
    book_id = request.GET.get("id")
    book_model = TBooks.objects.filter(id=book_id)[0]
    cart = request.session.get("cart")   #购物车
    cart1 = request.session.get("cart1")   #恢复区
    if cart:
        cart.add_book_to_cart(book_model)
    else:
        cart = Cart()
        cart.add_book_to_cart(book_model)
    cart1.delete_book_recover(book_model)
    request.session["cart"] = cart
    request.session["cart1"] = cart1
    cart = request.session.get("cart")
    total_prices = cart.total_price
    save_prices = cart.save_price

    book_id = book_model.id
    book_name = book_model.book_name
    book_picture = book_model.book_picture
    book_author = book_model.book_author
    discount_price = book_model.discount_price
    pub_time = book_model.pub_time.strftime("%Y-%m-%d")
    return JsonResponse({"result": 1, "total_prices": total_prices, "save_prices": save_prices,
                         "book_id": book_id, "book_name": book_name, "book_picture": book_picture,
                         "book_author": book_author, "discount_price": discount_price, "pub_time": pub_time})

#判断购物车是否存在
def cart_settlement(request):
    cart = request.session.get("cart")
    if cart:
        return JsonResponse({"result": 1})
    return JsonResponse({"result": 2})


# 获取用户地址

def select(address1):
    if isinstance(address1,TAddress):
        return {"name": address1.name, "address": address1.address, "code": address1.code,
         "phone": address1.phone, "mob_phone": address1.mob_phone }

def select_address(request):
    address_id = request.POST.get("id")
    address_detail = TAddress.objects.filter(id=address_id)
    return JsonResponse({"user_address":list(address_detail)},safe=True,json_dumps_params={"default": select})

# 填写或者选择地址
def add_user_address(request):
    name = request.GET.get("username")
    user_address = request.GET.get("user_address")
    code = request.GET.get("code")
    mob_phone = request.GET.get("mob_phone")
    phone = request.GET.get("phone")
    username = request.session.get("stats")
    user_id = TUser.objects.filter(username=username)[0].id
    result = TAddress.objects.filter(name=name, address=user_address, code=code, mob_phone=mob_phone, phone=phone,user_id=user_id)
    if name and user_address and code and mob_phone and phone:
        request.session["mob_phone"] = mob_phone
        request.session["name"] = name
        request.session["user_address"] = user_address
        request.session["code"] = code
        if result:
            return JsonResponse({"result": 1})
        TAddress.objects.create(name=name,address=user_address,code=code,mob_phone=mob_phone,phone=phone,user_id=user_id)
        return JsonResponse({"result": 2})
    return JsonResponse({"result": 3})


# 结算后清除函数
def delete_information(request):
    order_number = request.session.get("order_number")
    order_id = TOrder.objects.filter(order_num=order_number)[0].id
    TOrderitem.objects.filter(order_id=order_id).delete()
    del request.session["cart"]
    del request.session["order_number"]
    del request.session["number"]
    del request.session["mob_phone"]
    del request.session["name"]
    del request.session["code"]
    del request.session["user_address"]
    del request.session["order_time"]
    return redirect("orderapp:car")


def order_detail(request):
    username = request.session.get("stats")
    if username:
        username = request.session.get("stats")
        user_id = TUser.objects.filter(username=username)[0].id
        order_list  = TOrder.objects.filter(user_id=user_id)
        return render(request,"orderapp/indent_order_list.html",{"order_list":order_list})
    return redirect("/userapp/login/?flag=6")




