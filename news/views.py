from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *
from .filters import PostFilter
from .forms import PostForm, AuthorForm


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/authors.html'


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/allnews.html'
    context_object_name = 'Posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'news/post_search.html'
    context_object_name = 'Posts'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/news/'


class PostOne(DetailView):
    model = Post
    context_object_name = 'Post'
    queryset = Post.objects.filter()


class UserUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'news/author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return self.request.path


# class NewsCreateView(PermissionRequiredMixin, CreateView):
#     template_name = 'add.html'
#     form_class = PostForm
#     permission_required = ('news.add_post', )
#
#
# class NewsUpdateView(PermissionRequiredMixin, UpdateView):
#     template_name = 'add.html'
#     form_class = PostForm
#     permission_required = ('news.update_post',)
#
#     def get_object(self, **kwargs):
#         id = self.kwargs.get('pk')
#         return Post.objects.get(pk=id)
