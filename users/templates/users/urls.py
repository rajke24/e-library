from django.urls import path
from .views import register, login_page, profile, profile_edit, profile_books, user_books
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                            html_email_template_name='users/password_reset_email.html',
                                            subject_template_name='users/password_reset_subject.txt'), 
        name='password_reset'
        ),
    path(
        'password-reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
        ),
    path(
        'password-reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
        ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
        ),
    path('profile/', profile, name='profile'),
    path('profile/edit', profile_edit, name='profile_edit'),
    path('profile/profile_books', user_books, name='profile_books'),
]