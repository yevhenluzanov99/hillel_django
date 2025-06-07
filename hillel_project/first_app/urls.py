from django.urls import path
from django.views.decorators.cache import cache_page

from first_app.views import func_views, generic_views

urlpatterns = [
    # path('employees/', func_views.employee_list, name='employee_list'),
    path(
        "employees/",
        generic_views.EmployeeListView.as_view(),
        name="employee_list",
    ),
    path(
        "employees/<int:pk>/",
        cache_page(180)(generic_views.EmployeeDetailsView.as_view()),
        name="employee_details",
    ),
    path(
        "employees/update/<int:pk>/",
        generic_views.EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employees/delete/<int:pk>/", func_views.employee_delete, name="employee_delete"
    ),
    path("querysets/", func_views.queryset_route, name="querysets"),
    path(
        "salary-calculator/",
        cache_page(120)(generic_views.SalaryCalculatorView.as_view()),
        name="salary_calc",
    ),
]
