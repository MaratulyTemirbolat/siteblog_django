"""Controller to connect data with templates."""
from typing import (
    Any,
    Dict,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
)
from django.views.generic import (
    ListView,
    DetailView,
)
from django.db.models import (
    QuerySet,
    F,
)
from django.contrib.auth import (
    login,
    logout,
)

from auths.models import CustomUser
from blog.models import (
    Post,
    Category,
    Tag,
)
from blog.forms import (
    CustomUserRegisterForm,
    CustomerUserLoginForm,
)


def user_register(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.method == 'POST':
        form: CustomUserRegisterForm = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            custom_user: CustomUser = form.save()
            login(request, custom_user)
            return render(request,
                          "blog/successful_action.html",
                          {"message": "You are successfully registerred"})
    else:
        form: CustomUserRegisterForm = CustomUserRegisterForm()
    return render(request, "blog/register_form.html", {"form": form})


def user_login(request: WSGIRequest) -> HttpResponse:  # noqa
    if request.method == 'POST':
        form: CustomerUserLoginForm = CustomerUserLoginForm(data=request.POST)
        if form.is_valid():
            user: CustomUser = form.get_user()
            login(request, user)
            return render(request,
                          "blog/successful_action.html",
                          {"message": f"Welcome {user.surname} {user.name}"})
    else:
        form: CustomerUserLoginForm = CustomerUserLoginForm()
    return render(request, "blog/login.html", {"form": form})


def user_logout(request: WSGIRequest) -> HttpResponse:  # noqa
    logout(request)
    return redirect('home')


class PostsByCategory(ListView):  # noqa
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False
    # Чтобы при запросе несуществующей категории была ошибка 404 если пусто

    def get_queryset(self) -> QuerySet:  # noqa
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # noqa
        context: dict = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Home(ListView):  # noqa
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # noqa
        context: dict = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context


class GetPost(LoginRequiredMixin, DetailView):  # noqa
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'
    raise_exception = True

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # noqa
        # get_context_data нужен для увеличения количества просмотров к посту
        # Можно использовать не только для того, чтобы передать контекст
        # но и выполнить какие-то действия с данными
        context: dict = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        # После обновления views мы перезапрашиваем данные
        return context


class PostsByTag(ListView):  # noqa
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1
    allow_empty = False

    def get_queryset(self) -> QuerySet:  # noqa
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # noqa
        context: dict = super().get_context_data(**kwargs)
        context['title'] = ('Записи по тегу: ' +
                            str(Tag.objects.get(slug=self.kwargs['slug'])))
        return context


class Search(ListView):  # noqa
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self) -> QuerySet:  # noqa
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:  # noqa
        context: dict = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context
