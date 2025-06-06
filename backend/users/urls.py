from django.urls import path
<<<<<<< HEAD
from . views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
=======
from . views import LoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
>>>>>>> 84b0af2340e4302f70c3d35fd5d4dba17ecaa9ea
]
