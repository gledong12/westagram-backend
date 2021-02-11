from django.urls import path
from user.views  import UserView, SigninView

urlpatterns = [
	path('',       UserView.as_view()),
        path('signin', SigninView.as_view()),
]
