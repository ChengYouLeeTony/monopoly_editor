from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate

class LoginView(View):
    initial = {'active_page': 'register'}
    template_name = 'login_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "active_page": "login",
            "error": None
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/monopoly/creator")

            else:
                res = {'active_page': 'login',
                       "error": "閒置的使用者"}
                return render(request, self.template_name, res)
        else:
            res = {'active_page': 'login',
                   "error": "錯誤的帳號或密碼"}
            return render(request, self.template_name, res)

