from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from modelsapp.models import TCategory,TBooks
# 主页
def index(request):
    '''
    主页渲染函数，其中包括类别，书籍推荐排序等
    :param request:
    :return:
    '''
    # 拿到类别，按照类别ID分类
    one_cate = TCategory.objects.filter(parent_id=0)
    two_cate = TCategory.objects.filter(parent_id__gt=0)
    # 上架时间
    book_shlefs = TBooks.objects.all().order_by("-shelf_time")[0:8]
    # 上架时间和新书销量
    book_new_sales = TBooks.objects.all().order_by("-shelf_time", "-book_sales")[0:5]
    # 书籍销量
    book_sales = TBooks.objects.all().order_by("-book_sales")[0:8]
    # 作者推荐
    author_intro = TBooks.objects.all().order_by("-stock")[0:8]
    return render(request,'indexapp/index.html',{"one_cate": one_cate,"two_cate": two_cate,"book_shlefs": book_shlefs,
                            "book_new_sales": book_new_sales,"book_sales": book_sales, "author_intro": author_intro})

# 书籍详情
def book_details(request):
    '''
    书籍详情页面，根据书籍的ID渲染不同的书
    :param request:
    :return:
    '''
    # 书籍ID
    book_id = request.GET.get("id")
    if not book_id:
        book_id = 1
    # 书籍对象
    book_query= TBooks.objects.filter(id= book_id)
    book_one = book_query[0]
    # 二级类别ID
    cate_two2 = book_query[0].cate_id
    # 二级类别model对象
    cate_two = TCategory.objects.filter(id=cate_two2)[0]
    # 拿到二级类别对象
    cate_two_deltail = TCategory.objects.filter(id=cate_two2)
    # 拿到一级类别ID
    cate_one1 = cate_two_deltail[0].parent_id
    # 拿到一级类别model对象
    cate_one = TCategory.objects.filter(id=cate_one1)[0]
    book_detail = TBooks.objects.filter(id=book_id)[0]
    return render(request, 'indexapp/book_details.html',{"book_detail": book_detail,"cate_one": cate_one, "cate_two": cate_two,"book_one":book_one})

# 书籍列表
def book_list(request):
    '''
    书籍分类列表，包括不同类别书籍数量，分页，首页，末页，输入跳转等
    :param request:
    :return:
    '''
    # 分页，类别ID
    number = request.GET.get("number")
    one_id = request.GET.get("one_id")
    two_id = request.GET.get("two_id")
    # 拿到一级ID和二级ID
    one_cate = TCategory.objects.filter(parent_id=0)
    two_cate = TCategory.objects.filter(parent_id__gt=0)
    # 如果没有NUM。则默认第一页
    if not number or not number.isdigit():
        number = 1
        # 如果没有ID，默认进入ID=1
    if not one_id and not two_id:
        one_id=1
        # 如果没有二级ID，则点击的类别为一级，通过一级ID找到二级ID，然后通过二级ID查找书籍
    if not two_id:
        list_id = []
        categroy_query = TCategory.objects.filter(parent_id=one_id)
        cate_one = TCategory.objects.filter(id=one_id)[0]
        cate_two = None
        for model in categroy_query:
            list_id.append(model.id)
        books_list = TBooks.objects.filter(cate__id__in=list_id)
        # 直接通过二级ID查找书籍
    else:
        books_list = TBooks.objects.filter(cate_id=two_id)
        # 取到类别的MODLE对象，用于做详情点击
        cate_one = TCategory.objects.filter(id=one_id)[0]
        cate_two = TCategory.objects.filter(id=two_id)[0]
        # 拿到model对象进行分页
    pagtor = Paginator(books_list, per_page=3)
    # number页的页面对象
    pages = pagtor.page(number)
    # 查询到所有书籍信息，用来统计各类别的书籍数量
    books = TBooks.objects.all()
    # 存放cate_id的列表
    books_cate_id_lists = []
    for book_model in books:
        books_cate_id_lists.append(book_model.cate_id)
    # 对列表去重,变为集合
    books_cate_id_list = set(books_cate_id_lists)
    # 定义列表，存放不同书籍cate_id对应的数量及cate_id号，用于前端页面遍历
    lists = []
    for ids in books_cate_id_list:
        # 不同cate_id所对应的数量
        num = TBooks.objects.filter(cate_id=ids).count()
        lists.append([ids,num])
    return render(request, 'indexapp/book_list.html',{"pages": pages, "one_cate": one_cate,"two_cate": two_cate, "cate_one": cate_one, "cate_two": cate_two,"lists": lists})



