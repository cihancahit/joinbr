from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse


from reviews_and_rating.models import ReviewModel
from users.models import UserProfileModel, User
from expert.models import Expert
from companies.models import Company
from events.models import Event
from users.token import account_activation_token
from .forms import SignUpForm, LoginForm, CustomPasswordResetForm
from fec_app.views import BaseContext


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     raw_password = form.cleaned_data.get('password1')
        #     user = authenticate(request, email=user.email, password=raw_password)
        #     if user is not None:
        #         login(request, user)
        #     else:
        #         print("user is not authenticated")
        #     return redirect('index_url')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Revealin account.'
            message = render_to_string('pages/user_pages/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()
            send_mail(
                mail_subject,
                'Revealin',
                'no-reply@revealin.com',
                [to_email],
                html_message=message,
            )
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'pages/user_pages/user_registration1.html', {'form': form})


class UserLogin(LoginView):
    form_class = LoginForm
    template_name = 'pages/user_pages/user_login1.html'


class UserPublicProfile(BaseContext, DetailView):
    model = UserProfileModel
    template_name = 'pages/user_pages/public_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserPublicProfile, self).get_context_data(**kwargs)
        user1 = UserProfileModel.objects.filter(slug=self.kwargs["slug"]).all()
        context["user_active"] = "menu-active"
        context["followed_experts"] = Expert.objects.filter(follower_list__in=user1).all()
        context["followed_companies"] = Company.objects.filter(follower_list__in=user1).all()
        context["followed_events"] = Event.objects.filter(follower_list__in=user1).all()
        context["reviews"] = ReviewModel.objects.filter(user__in=user1, anon=False).all()
        context["events"] = Event.objects.filter()

        return context


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('index_url')
    else:
        return HttpResponse('Activation link is invalid!')


def active(request):
    return render(request, "pages/user_pages/acc_active_email.html")


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'pages/user_pages/password_reset_email.html'
    form_class = CustomPasswordResetForm
