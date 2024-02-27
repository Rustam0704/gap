from django.urls import path

from apps.gap.views import RoomListView, RoomDetailView, LikeOpinionView, SearchOpinionView, OpinionDetailView, \
    UserLoginView, RegisterView, UserLogoutView

app_name = 'gap'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('register/', RegisterView.as_view(), name='register-page'),
    path('login/', UserLoginView.as_view(), name='login-page'),
    path('logout/', UserLogoutView.as_view(), name='logout-page'),
    path('room/<pk>', RoomDetailView.as_view(), name='room'),
    path('opinion/<pk>', OpinionDetailView.as_view(), name='opinion'),
    path('like/<pk>', LikeOpinionView.as_view(), name='opinion-like'),
    path('search', SearchOpinionView.as_view(), name='search-opinion'),

]
