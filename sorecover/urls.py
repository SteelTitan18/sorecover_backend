"""sorecover URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from recovering.views import *

router = routers.SimpleRouter()

router.register('admin', AdminViewSet, basename='admin')
router.register('member', MemberViewSet, basename='member')
router.register('version', VersionViewSet, basename='version')
router.register('community', ValidatedCommunityViewSet, basename='community')
router.register('all_communities', CommunityViewSet, basename='all_community')
router.register('comity', ComityViewSet, basename='comity')
router.register('saloon', SaloonViewSet, basename='saloon')
router.register('community_validation', CommunityValidationViewSet, basename='community_validation')
router.register('favorites', FavoritesViewSet, basename='favorites')
router.register('final_version', FinalVersionViewSet, basename='final_version')
router.register('message', MessageViewSet, basename='message')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/community/<int:community_id>/members', MemberViewSet.as_view({'get': 'list'}), name='community_members'),
    path('api/community/<int:community_id>/saloons', SaloonViewSet.as_view({'get': 'list'}), name='community_saloons'),
    path('api/member/<int:member_id>/communities', ValidatedCommunityViewSet.as_view({'get': 'list'}),
         name='member_communities'),
path('api/member/<int:member_id>/saloons', SaloonViewSet.as_view({'get': 'list'}),
         name='member_projects'),
    # path('api/saloon/<int:saloon_id>/messages', MessageViewSet.as_view({'get': 'list'}), name='saloon_messages'),
    path('api/community_integration/', community_integration,
         name='community_integration'),
    path('api/community_pull_out/', community_pull_out,
         name='community_pull_out'),
    path('api/like_version/', version_liking, name='like-version'),
    path('api/dislike_version/', version_disliking, name='dislike-version'),
    path('api/tag_on_message/', message_taging, name='tag-on-message'),
    path('api/tag_on_version/', version_taging, name='tag-on-version'),
    path('test/', MessageViewSet.as_view({'get': 'list'}), name='test'),
]
