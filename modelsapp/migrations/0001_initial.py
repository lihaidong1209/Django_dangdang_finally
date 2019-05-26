# Generated by Django 2.0.6 on 2019-05-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TAddress',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('mob_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_address',
            },
        ),
        migrations.CreateModel(
            name='TBooks',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(blank=True, max_length=120, null=True)),
                ('book_picture', models.CharField(blank=True, max_length=2000, null=True)),
                ('market_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shelf_time', models.DateTimeField(blank=True, null=True)),
                ('book_sales', models.IntegerField(blank=True, null=True)),
                ('book_cate', models.CharField(blank=True, max_length=40, null=True)),
                ('customer_rating', models.IntegerField(blank=True, null=True)),
                ('book_author', models.CharField(blank=True, max_length=60, null=True)),
                ('press', models.CharField(blank=True, max_length=120, null=True)),
                ('pub_time', models.DateTimeField(blank=True, null=True)),
                ('edition', models.IntegerField(blank=True, null=True)),
                ('printing_time', models.DateTimeField(blank=True, null=True)),
                ('impression', models.CharField(blank=True, max_length=40, null=True)),
                ('isbn', models.CharField(blank=True, max_length=40, null=True)),
                ('word_num', models.CharField(blank=True, max_length=60, null=True)),
                ('page_num', models.IntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=20, null=True)),
                ('paper', models.CharField(blank=True, max_length=40, null=True)),
                ('packing', models.CharField(blank=True, max_length=40, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_books',
            },
        ),
        migrations.CreateModel(
            name='TCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cate_name', models.CharField(blank=True, max_length=40, null=True)),
                ('book_num', models.IntegerField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_category',
            },
        ),
        migrations.CreateModel(
            name='TOrder',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('order_num', models.IntegerField(blank=True, null=True)),
                ('order_time', models.DateTimeField(blank=True, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_order',
            },
        ),
        migrations.CreateModel(
            name='TOrderitem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_num', models.IntegerField(blank=True, null=True)),
                ('sub_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_orderitem',
            },
        ),
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('add1', models.CharField(blank=True, max_length=40, null=True)),
                ('add2', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 't_user',
            },
        ),
    ]