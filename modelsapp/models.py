# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mob_phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TBooks(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=120, blank=True, null=True)
    book_picture = models.CharField(max_length=2000, blank=True, null=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shelf_time = models.DateTimeField(blank=True, null=True)
    book_sales = models.IntegerField(blank=True, null=True)
    book_cate = models.CharField(max_length=40, blank=True, null=True)
    customer_rating = models.IntegerField(blank=True, null=True)
    book_author = models.CharField(max_length=60, blank=True, null=True)
    press = models.CharField(max_length=120, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    printing_time = models.DateTimeField(blank=True, null=True)
    impression = models.CharField(max_length=40, blank=True, null=True)
    isbn = models.CharField(max_length=40, blank=True, null=True)
    word_num = models.CharField(max_length=60, blank=True, null=True)
    page_num = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    paper = models.CharField(max_length=40, blank=True, null=True)
    packing = models.CharField(max_length=40, blank=True, null=True)
    cate = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_books'


class TCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    cate_name = models.CharField(max_length=40, blank=True, null=True)
    book_num = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_category'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_num = models.IntegerField(blank=True, null=True)
    order_time = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TOrderitem(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(TBooks, models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    book_num = models.IntegerField(blank=True, null=True)
    sub_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_orderitem'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    add1 = models.CharField(max_length=40, blank=True, null=True)
    add2 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'
