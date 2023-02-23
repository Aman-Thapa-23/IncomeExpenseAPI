"""
IncomeExpense URL Configuration

"""
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="IncomeExpense API",
      default_version='v1',
      description="This system helps to maintain the daily incomes and expenses record.",
      terms_of_service="There is not any specific terms and condition in order to use this service.",
      contact=openapi.Contact(email="soldieranjan29@gmail.com"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('auth/api/v1/', include('authentication.urls', namespace='authentication')),
   path('expense/api/v1/', include('expense.urls', namespace='expense')),
   path('income/api/v1/', include('income.urls', namespace='income')),
   path('user-stats/api/v1/', include('userstats.urls', namespace='userstats')),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
