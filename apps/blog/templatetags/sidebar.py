from typing import (
    Dict,
    Any,
)

from django import template
from django.db.models import QuerySet

from blog.models import (
    Post,
    Tag,
)

register: template.Library = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular_posts(post_number: int = 3) -> Dict[str, Any]:  # noqa
    posts: QuerySet[Post] = Post.objects.order_by('-views')[:post_number]
    return {"posts": posts, "post_number": post_number}


@register.inclusion_tag('blog/tags_tpl.html')
def get_popular_tags(tag_number: int = 20) -> Dict[str, Any]:  # noqa
    tags: QuerySet[Tag] = Tag.objects.all()[:tag_number]
    return {"tags": tags, "tag_number": tag_number}
