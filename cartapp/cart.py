
#购物车条目对象，属性包括book对象和对应数量
class CartItem:
    def __init__(self,book,amount):
        self.book = book
        self.amount = amount
        self.status = 1

#购物车对象 ，属性为价格和存放 book对象和对应数量
class Cart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartitem = []
        self.cartitem_recover = []

# -============================================购买购物车========================================

# 计算每本书籍对象的价格
    def book_sums(self):
        self.total_price = 0
        self.save_price = 0
        for cart_object in self.cartitem:
            self.total_price += cart_object.book.discount_price * cart_object.amount
            self.save_price += (cart_object.book.market_price - cart_object.book.discount_price) * cart_object.amount

# 向购物车添加一本书籍并判断书籍是否存在，然后对书籍数量及价格进行计算
    def add_book_to_cart(self,book):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount += 1
                self.book_sums()
                return
        self.cartitem.append(CartItem(book,1))
        self.book_sums()
        # 多本
    def add_book_to_carts(self,book,amount):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount += amount
                self.book_sums()
                return
        self.cartitem.append(CartItem(book,amount))
        self.book_sums()


# 修改书籍的商品信息并重新计算价格
    def modify_cart(self,book,amount):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount = amount
        self.book_sums()
# 增加一本---修改
    def modify_cart_add(self,book):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount += 1
        self.book_sums()
# 减少一本---修改
    def modify_cart_red(self,book):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount -= 1
        self.book_sums()

# 多本————修改
    def modify_cart_books(self,book,amount):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount = amount
        self.book_sums()


# 删除购物车书籍并重新计算价格
    def delete_book(self,book):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                self.cartitem.remove(cart_object)
        self.book_sums()

# -============================================恢复购物车==============================================

 # 添加书籍到恢复区
    def add_book_to_recover(self,book):
        # 添加
        if self.cartitem_recover:
            for cart_object in self.cartitem_recover:
                if cart_object.book.id == book.id:
                    return
        self.cartitem_recover.append(CartItem(book, 1))

# 恢复书籍到购物车
    def delete_book_recover(self,book):
        for cart_object in self.cartitem_recover:
            if cart_object.book.id == book.id:
                self.cartitem_recover.remove(cart_object)

    # 恢复订单
    def recover_book_to_carts(self,book,amount):
        for cart_object in self.cartitem:
            if cart_object.book.id == book.id:
                cart_object.amount += amount
                self.book_sums()
                return
        self.cartitem.append(CartItem(book,amount))
        self.book_sums()