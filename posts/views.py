"""Posts Views"""

# Django
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from posts.models import Post
from .models import *
from users.models import *
from django.shortcuts import render,redirect

from posts.forms import PostForm
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from events.models import event

class PostUpdateView(UpdateView):
    fields = ("title","photo")
    model = Post
    template_name = 'posts/new.html'
    context_object_name = 'form'
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        """Add User and profile to context."""

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

class PostDeleteView(DeleteView):
    template_name = 'posts/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy("posts:feed")
# LoginRequired into Views
class CreatePostView(LoginRequiredMixin, CreateView):
    """Create New Post View"""
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        """Add User and profile to context."""

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class PostFeedView(ListView):
    """Return all published posts."""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 4
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        """Add User and profile to context."""
        ev_list=[]
        ev_list=event.objects.all()
        e=list(ev_list)
        e.reverse()
        context = super().get_context_data(**kwargs)
        print(e)
        context['e'] = e
        return context


def like_post(request):
    user=request.user
    if request.method=="POST":
        post_id=request.POST['post_id']

        post_obj=Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like,created=Like.objects.get_or_create(user=user,post_id=post_id)
        print("see: ",created,like,like.value)
        if not created:
            if like.value=='Like':
                like.value='UnLike'
            else:
                like.value='Like'


        else:
            like.value='Like'
            post_obj.save()
            like.save()
        data={
        'value':like.value,
        'likes':post_obj.liked.all().count()
        }
        print(data)
        return JsonResponse(data,safe=False)

    return redirect('posts:feed')
#        $(document).ready(function(){
#   $("#heart").click(function(){
#     if($("#heart").hasClass("liked")){
#       $("#heart").html('<i class="fa fa-heart-o" aria-hidden="true"></i>');
#       $("#heart").removeClass("liked");
#     }else{
#       $("#heart").html('<i class="fa fa-heart" aria-hidden="true"></i>');
#       $("#heart").addClass("liked");
#     }
#   });
# });
