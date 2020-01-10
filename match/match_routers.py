from match import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'team', views.TeamViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'category', views.CategoryViewSet)
