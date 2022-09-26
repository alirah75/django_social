from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Like
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm, CommentCreatedForm, CommentReplyForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        # posts = Post.objects.order_by('-created')
        if request.GET.get('search'):
            posts = Post.objects.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'search_form': self.form_class})


class PostDetailView(View):
    form_class = CommentCreatedForm
    form_reply_class = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        disable_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            disable_like = True
        return render(request, 'home/details.html', {'post': self.post_instance, 'comments': comments,
                                                     'form': self.form_class, 'reply_form': self.form_reply_class,
                                                     'disable_like': disable_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment submit successfully', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'deleted your post', 'success')
        else:
            messages.error(request, 'you cant deleted this post', 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'you cant updated this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()

            messages.success(request, 'you updated this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PoseCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'create new post', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id):
        form = CommentReplyForm(request.POST)
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submited successfully', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class LikePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            messages.error(request, 'you already liked this post', 'danger')
        else:
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'you like this post', 'success')
        return redirect('home:post_detail', post.id, post.slug)
