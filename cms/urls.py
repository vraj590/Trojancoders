from django.urls import path, include
from .views import Home, EmpSignUpView, customer_login, EmpDashboard, EmpLogout, CompSignUpView, company_login, CompLogout, \
    CompDashboard, AddProfile, CompAddJob, CompJobView

app_name = 'cms'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('pu/', include([
        path('signup', EmpSignUpView.as_view(), name='emp_signup'),
        path('login', customer_login, name='emp_login'),
        path('dashboard', EmpDashboard.as_view(), name='emp_dashboard'),
        path('logout', EmpLogout.as_view(), name='emp_logout'),
        path('profile/add', AddProfile.as_view(), name='pu_add_profile'),
    ])),
    path('company/', include([
        path('signup', CompSignUpView.as_view(), name='comp_signup'),
        path('login', company_login, name='comp_login'),
        path('dashboard', CompDashboard.as_view(), name='comp_dashboard'),
        path('logout', CompLogout.as_view(), name='comp_logout'),
        path('jobs/add', CompAddJob.as_view(), name='comp_add_job'),
        path('jobs/<str:job>/detail', CompJobView.as_view(), name='comp_job_detail')
    ])),
]
