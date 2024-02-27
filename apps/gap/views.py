from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.gap.forms import UserLoginForm, UserRegisterModelForm
from apps.gap.models import Room, Opinion, Comment, OpinionLike


class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'gap/rooms.html', {"rooms": rooms})


class RoomDetailView(View):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        opinions = sorted(Opinion.objects.filter(room=room), key=lambda o: o.like_count, reverse=True)
        context = {
            "room": room,
            "opinions": opinions
        }
        return render(request, "gap/opinoins.html", context=context)


class LikeOpinionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        like, created = OpinionLike.objects.get_or_create(user=request.user, opinion=opinion)
        if not created:
            like.delete()
        return redirect(reverse("gap:room", kwargs={"pk": opinion.room.pk}))


class OpinionDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        comments = opinion.comments.all().order_by("-created_at")
        comments = sorted(comments, key=lambda c: c.like_count, reverse=True)
        context = {
            "opinion": opinion,
            "comments": comments
        }
        return render(request, "gap/comments.html", context=context)


class CommentLikeView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)


class SearchOpinionView(View):
    def get(self, request):
        q = request.GET.get('q', None)
        if q:
            opinions = Opinion.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        else:
            opinions = None

        context = {
            'param': q,
            'opinions': opinions
        }
        return render(request, 'gap/search-opinion.html', context=context)


class RegisterView(View):
    def get(self, request):
        form = UserRegisterModelForm()
        return render(request, "gap/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterModelForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "User successfully registered")
            form.save()
            return redirect("gap:login-page")
        else:
            return render(request, "gap/register.html", {"form": form})


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "gap/login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.COOKIES)
                messages.success(request, "user successfully logged in")
                return redirect("landing_page")
            else:
                messages.error(request, "Username or password wrong")
                return redirect("gap:login-page")

        else:
            return render(request, "gap/login.html", {"form": form})


class UserLogoutView(View):
    def get(self, request):
        return render(request, "gap/logout.html")

    def post(self, request):
        logout(request)
        messages.info(request, "User successfully loged out")
        return redirect("gap:login-page")
