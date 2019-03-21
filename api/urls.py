from django.urls import path, include

from api.views import CompanyEmployeesView, OurFriendsView, FavouriteFoodsView

urlpatterns = [
    path('company_employees/<int:index>', CompanyEmployeesView.as_view(), name='company_employees'),
    path('our_friends/<int:people1>/<int:people2>/', OurFriendsView.as_view(), name='our_friends'),
    path('favourite_foods/<int:index>', FavouriteFoodsView.as_view(), name='favourite_foods'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]