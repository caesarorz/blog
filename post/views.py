from django.http import HttpResponse, Http404
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import CreateView, View

from .models import Post, Author, Document, DocumentDownload
from subscription.models import Signup
from .forms import CommentForm, PostForm


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }

    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    documents = Document.objects.all().filter(title__icontains="myresume")
    # print("resume ", documents.generate_download_url())
    for doc in documents:
        print(doc.generate_download_url())

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'docs': documents,
    }
    return render(request, "index.html", context)


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count,
    }

    return render(request, "blog.html", context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    form = CommentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse(
                            'post-detail',
                            kwargs={'id': post.id
                                    }))

    context = {
        'form': form,
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent
    }
    return render(request, "post.html", context)


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={"id": form.instance.id}))

    context = {
        'title': title,
        'form': form
    }

    return render(request, "post_create.html", context)


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={"id": form.instance.id}))

    context = {
        'title': title,
        'form': form
    }

    return render(request, "post_create.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))

import os
from wsgiref.util import FileWrapper
from django.conf import settings
from mimetypes import guess_type

class DownloadDocs(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("id")
        qs = Document.objects.filter(title__icontains="myresume")
        # print(qs)
        if qs.count() != 1:
            raise Http404("Document not found")
        document_obj = qs.first()
        file_root = settings.PROTECTED_ROOT
        filepath = document_obj.file.path         
        final_path = os.path.join(file_root, filepath)

        with open(final_path, 'rb') as f:
            wrapper = FileWrapper(f)
            content = "This is an example"
            mimetype = "application/force-download"
            guess_mimetype = guess_type(filepath)[0]
            if guess_mimetype:
                mimetype = guess_mimetype
            # response = HttpResponse(download_obj.get_download_url())
            response = HttpResponse(wrapper, content_type=mimetype)
            response["Content-Disposition"] = "attachment;filename={}".format(document_obj.name)
            response["X-SendFile"] = str(document_obj.name)
            return response