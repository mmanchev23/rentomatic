from . import views
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.schemas import get_schema_view
from rest_framework.exceptions import NotAuthenticated
from rest_framework.documentation import include_docs_urls

def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        request = context['request']
        return Response({"You are not logged in!": {
            "home page": f"{request.scheme}://{request.get_host()}/",
            "register": f"{request.build_absolute_uri()}auth/register/",
            "login": f"{request.build_absolute_uri()}auth/login/",
        }}, status=401)

    return exception_handler(exc, context)


class APIRoot(routers.APIRootView):
    def get_view_name(self) -> str:
        return "Rentomatic"

    def get(self, request):
        if request.user.is_authenticated == True:
            return Response({
                f"Logged in as {request.user.username}": {
                    "home page": f"{request.scheme}://{request.get_host()}/",
                    f"{request.user.username}": f"{request.build_absolute_uri()}user/",
                    "likes": f"{request.build_absolute_uri()}likes/",
                    "followers": f"{request.build_absolute_uri()}followers/",
                    "cars": f"{request.build_absolute_uri()}cars/",
                    "applications": f"{request.build_absolute_uri()}applications/",
                    "documentation": f"{request.build_absolute_uri()}docs/",
                    "schema": f"{request.build_absolute_uri()}schema/",
                    "logout": f"{request.build_absolute_uri()}auth/logout/",
                }
            })


class Healthy_at_Home_Router(routers.DefaultRouter):
    APIRootView = APIRoot


API_TITLE = 'Rentomatic API'
API_DESCRIPTION = 'API for Rentomatic!'
schema_view = get_schema_view(title=API_TITLE)

router = Healthy_at_Home_Router()
router.register(r'user', views.UserView, 'user')
router.register(r'likes', views.ProfileLikeView, 'likes')
router.register(r'followers', views.ProfileFollowerView, 'followers')
router.register(r'cars', views.CarView, 'car')
router.register(r'applications', views.ApplicationView, 'application')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)), 
    path('schema/', schema_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)