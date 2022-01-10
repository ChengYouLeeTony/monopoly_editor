# from django.shortcuts import render, redirect, get_object_or_404

# # Create your views here.
# from django.views import View
# from monopoly.models import Profile
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.models import User
# from django.core.exceptions import PermissionDenied
# from django.http import Http404, HttpResponse
# from django.template import Template, RequestContext
# from monopoly.forms.profile_form import ProfileForm
# from django.contrib.auth.tokens import default_token_generator
# from monopoly.models.session import Session

# class GameView(View):
#     template_name = 'game_view.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {
#             "username": request.user.username,
#             "hostname": kwargs.get("host_name")
#         })

#  class JoinView(View):
#     template_name = 'join_view.html'

#     def get(self, request, *args, **kwargs):
#         print(request.path)
#         user = request.user
#         host_name = kwargs.get('host_name', user.username)

#         try:
#             profile = Profile.objects.get(user=user)
#         except Exception:
#             profile = None

#         return render(request, self.template_name, {
#             "user": {
#                 "name": user.username,
#                 "avatar": profile.avatar.url if profile else ""
#             },
#             "host_name": host_name if len(host_name) else user.username
#         })

# class LoginView(View):
#     initial = {'active_page': 'register'}
#     template_name = 'login_view.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {
#             "active_page": "login",
#             "error": None
#         })

#     def post(self, request, *args, **kwargs):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect("/monopoly/join")

#             else:
#                 res = {'active_page': 'login',
#                        "error": "Inactive user."}
#                 return render(request, self.template_name, res)
#         else:
#             res = {'active_page': 'login',
#                    "error": "Invalid username or password."}
#             return render(request, self.template_name, res)

# class ProfileView(View):
#     initial = {'key': 'value'}
#     template_name = 'profile_view.html'

#     def get(self, request, *args, **kwargs):
#         try:
#             self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
#         except Exception:
#             self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
#             self.profile_user = None
#             return render(request, "404.html", {})


#         try:
#             self.profile_info = Profile.objects.get(user=self.profile_user)
#         except Exception:
#             self.profile_info = None

#         res = {
#             "user": self.profile_user,
#             "profile": self.profile_info
#         }
#         return render(request, self.template_name, res)

#     def post(self, request, *args, **kwargs):
#         # Unauthorized modification
#         try:
#             self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
#         except Exception:
#             self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
#             self.profile_user = None
#             raise render(request, "404.html", {})

#         try:
#             self.profile_info = Profile.objects.get(user=self.profile_user)
#         except Exception:
#             self.profile_info = None

#         if self.profile_user != request.user:
#             raise PermissionDenied

#         bio = request.POST.get("bio", None)
#         avatar = request.FILES.get("avatar", None)

#         if self.profile_info:
#             self.profile_info.bio = bio
#             if avatar:
#                 self.profile_info.avatar = avatar
#             self.profile_info.save()
#         else:
#             self.profile_info = Profile(user=request.user, bio=bio, avatar=avatar)
#             form = ProfileForm(request.POST, request.FILES, instance=self.profile_info)

#             if form.is_valid():
#                 print("valid")
#                 self.profile_info.save()
#             else:
#                 print(form.errors)

#         res = {
#             "user": self.profile_user,
#             "profile": self.profile_info
#         }
#         return render(request, self.template_name, res)

#  # @transaction.atomic
# class ConfirmRegistrationView(View):
#     initial = {'key': 'value'}
#     template_name = 'login_view.html'

#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(User, username=kwargs.get('username'))
#         # Send 404 error if token is invalid
#         if not default_token_generator.check_token(user, kwargs.get('token')):
#             res = {'active_page': 'register',
#                    "error": "Invalid token."}
#             return render(request, self.template_name, res)

#         # Otherwise token was valid, activate the user.
#         user.is_active = True
#         user.save()
#         login(request, user)

#         return redirect("/monopoly/join")

#  # @csrf_protect
# class RegisterView(View):
#     initial = {'active_page': 'register'}
#     template_name = 'login_view.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, self.initial)

#     def post(self, request, *args, **kwargs):
#         conf = {
#             "request": request,
#             "username": request.POST.get("username", None),
#             "firstname": request.POST.get("firstname", None),
#             "lastname": request.POST.get("lastname", None),
#             "password": request.POST.get("password", None),
#             "email": request.POST.get("email", None)
#         }
#         successful, auth_or_error = Session().register(conf)

#         if successful:
#             res = {'active_page': 'register',
#                    "error": "Confirmation sent to your email."}
#             return render(request, self.template_name, res)
#         else:
#             res = {'active_page': 'register',
#                    "error": auth_or_error}
#             return render(request, self.template_name, res)