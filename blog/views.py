import telegram
from telegram import ParseMode
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from taggit.models import Tag
from django.conf import settings
from django.template.loader import render_to_string

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post, Author


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        if object_list.count() < 3:
            object_list = Post.published.all()

    first_slot = object_list[0]
    second_slot = object_list[1]
    last_slot = object_list[2]

    object_list = object_list[3:]

    paginator = Paginator(object_list, 7)  # 7 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'page': page, 'posts': posts, 'tag': tag, 'first_slot': first_slot, 'second_slot': second_slot,
               'last_slot': last_slot}
    return render(request, 'blog/post_list.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.author = request.user
            comment_form.publish = timezone.now()
            comment_form.post = post
            comment_form.save()
            return HttpResponseRedirect(
                f'/blog/{post.publish.year}/{post.publish.month}/{post.publish.day}/{post.slug}/')
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]

    context = {'post': post, 'comments': comments, 'comment_form': comment_form,
               'similar_posts': similar_posts}

    return render(request, 'blog/post_detail.html', context=context)


def author(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'blog/author.html', context=context)


@receiver(post_save, sender=Post)
def post_event_on_telegram(sender, instance, created, **kwargs):
    if created:
        message_html = render_to_string('blog/telegram_message.html', {'post': instance})
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        bot.send_photo(chat_id="@%s" % telegram_settings['channel_name'], photo=instance.image,
                       caption=message_html, parse_mode=ParseMode.HTML)
