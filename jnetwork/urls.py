# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Views
from users import views as users_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('events/',include('events.urls',namespace='events')),
    # Users
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # Posts
    path('', include(('posts.urls', 'posts'), namespace='posts')),

    path('users/', include("django.contrib.auth.urls")),
    #forgot password
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_complete"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
