from django.urls import path
from .views import (
    ListAllStockData,
    ListAllCompany,
    RetrieveStockDataByCompanyName,
    CalculateCumulativeReturns
)

urlpatterns = [
    path('', ListAllStockData.as_view(), name='all-stocks'),
    path('company/', ListAllCompany.as_view(), name='list-company'),
    path('<int:company_id>/', RetrieveStockDataByCompanyName.as_view(), name='get-stocks'),
    path('cumulative/', CalculateCumulativeReturns.as_view(), name='cumulative-returns'),
]