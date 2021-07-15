"""User views."""

# Django
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.models import User
from .models import clubrating
from events.models import *
# Forms
from users.forms import SignupForm
from django.db.models import Q
# Models
from posts.models import Post
from users.models import Profile



def rate():
    n=Profile.objects.filter(Q(is_club=True))
    b=clubrating.objects.all()
    no_of_clubs=[]
    for i in n:
        no_of_clubs.append(i.user.username)
    all_rating=[]
    main=[]
    for i in b:
        all_rating.append([i.club,i.stars])
    for i in range(len(no_of_clubs)):
        sp=[]
        for j in range(len(all_rating)) :
            if all_rating[j][0]==no_of_clubs[i]:
                sp.append(all_rating[j][1])
        if len(sp)==0:
            main.append(sum(sp))
        else:
            main.append(sum(sp)/len(sp))
    main2=[]
    for i in range(len(main)):
        main2.append([no_of_clubs[i],main[i]])
    return main2




def srch(request):

    name=request.POST['search']
    try:
        oks=User.objects.get(username=name)
        n=Profile.objects.filter(Q(user=oks.id))
    except:
        return render(request,'users/d.html')
    #return render(request,'users/clubs.html',{'n':n})
    return redirect("/users/"+name)
def rating_view(request):
    n=Profile.objects.filter(Q(is_club=True))
    b=clubrating.objects.all()
    no_of_clubs=[]
    for i in n:
        no_of_clubs.append(i.user.username)
    all_rating=[]
    main=[]
    for i in b:
        all_rating.append([i.club,i.stars])
    for i in range(len(no_of_clubs)):
        sp=[]
        for j in range(len(all_rating)) :
            if all_rating[j][0]==no_of_clubs[i]:
                sp.append(all_rating[j][1])
        if len(sp)==0:
            main.append(sum(sp))
        else:
            main.append(sum(sp)/len(sp))


    print(main)
    if request.method == "POST":
        if request.POST.get('club') and request.POST.get('stars') :
            post=clubrating()
            post.user=request.user
            post.club=request.POST.get('club')
            post.stars=request.POST.get('stars')
            post.content=request.POST.get('content','')
            post.save()
            return HttpResponseRedirect('/users/rating',{'n':n,'b':b,'main':main})
    return render(request,'users/rating.html',{'n':n,'b':b,'main':main})
def clubs(request):
    n=Profile.objects.filter(Q(is_club=True))
    return render(request,'users/clubs.html',{'n':n})


class SignupView(FormView):
    """Signup View."""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """If the form is valid save the user"""
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout View."""

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update a user's profile view"""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']
    # Return success url
    def get_object(self):
        """Return user's profile"""
        return self.request.user.profile
    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username


        return reverse('users:detail', kwargs={'username_slug': username})
    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        a=self.object.user.profile.is_student
        b=self.object.user.profile.is_club
        context['a'] =a

        context['b']=b
        return context


class UserDetailView(DetailView):
    """User detail view."""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(profile__user=user).order_by('-created')
        x=User.objects.get(username=user.username)
        main2=rate()
        val=0
        ev=event.objects.filter(club_name=x)
        ev2=list(ev)
        ev2.reverse()
        context['ev']=ev2
        for i in range(len(main2)):
            if str(main2[i][0])==str(x):
                val=main2[i][1]
        context['val']=val
        context['events']=event.objects.filter(club_name_id=x.id)
        return context
