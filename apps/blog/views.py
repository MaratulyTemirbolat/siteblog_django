from typing import (
    Any,
    Dict,
)

from django.views.generic import (
    ListView,
    DetailView,
)
from django.db.models import (
    QuerySet,
    F,
)

from blog.models import (
    Post,
    Category,
)


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False
    # Чтобы при запросе несуществующей категории была ошибка 404 если пусто

    def get_queryset(self) -> QuerySet:
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: dict = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: dict = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # get_context_data нужен для увеличения количества просмотров к посту
        # Можно использовать не только для того, чтобы передать контекст
        # но и выполнить какие-то действия с данными
        context: dict = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        # После обновления views мы перезапрашиваем данные
        return context


class PostsByTag(ListView):
    pass
