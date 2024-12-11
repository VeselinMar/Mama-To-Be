from django.urls import path

from mama_to_be.profiles.views import RegisterView, CustomLoginView, CustomLogoutView, ProfileEditView, \
    ProfileDisplayView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('<int:user_id>/', ProfileDisplayView.as_view(), name='profile-display'),
]
