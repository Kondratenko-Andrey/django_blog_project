from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    # Использую менеджер published, который создал в модели
    posts_list = Post.published.all()

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(posts_list, 3)

    # Извлекаем HTTP GET-параметр page и сохраняем его в переменной page_number
    # Этот параметр содержит запрошенный номер страницы.
    # Если параметра page нет в GET-параметрах запроса, то мы используем стандартное значение 1,
    # чтобы загрузить первую страницу результатов.
    page_number = request.GET.get('page', 1)

    try:
        # Получаем объекты для желаемой страницы, вызывая метод page() класса Paginator.
        # Этот метод возвращает объект Page, который хранится в переменной posts.
        # Он состоит из: object_list содержащие объекты записей(Post) данной страницы,
        # номер текущей страницы - number, и paginator, хранящий объект пагинатора.
        # Класс paginator содержит все записи(Post), количество страниц и количество записей.
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
