from django.views.generic import View, CreateView, ListView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import User, Company, PU, Profile, Job, ShortListCandidates
from .forms import EmpSignUpForm, CompSignUpForm, AddProfileForm, AddJobForm, ShortlistForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .decorators import employee_required, company_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


class Home(View):

    def get(self, request):
        return render(request, 'cms/home.html')


class EmpSignUpView(CreateView):
    model = User
    form_class = EmpSignUpForm
    template_name = 'cms/employee/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('cms:emp_dashboard')


class CompSignUpView(CreateView):
    model = User
    form_class = CompSignUpForm
    template_name = 'cms/employee/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('cms:comp_dashboard')


def customer_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("ecommerce:customer_dashboard")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "cms/employee/login.html", context={"form": form})


def company_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("ecommerce:customer_dashboard")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "cms/company/login.html", context={"form": form})


@method_decorator([login_required, employee_required()], name='dispatch')
class EmpLogout(LogoutView):
    template_name = 'cms/employee/logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)


@method_decorator([login_required, company_required()], name='dispatch')
class CompLogout(LogoutView):
    template_name = 'cms/company/logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)


@method_decorator([login_required, employee_required()], name='dispatch')
class EmpDashboard(ListView):
    model = Profile
    template_name = 'cms/employee/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pu = self.request.user.pu
        context['pu'] = pu
        context['profiles'] = Profile.objects.filter(pu=pu)
        context['organization'] = pu.user.organization_name
        return context


@method_decorator([login_required, employee_required()], name='dispatch')
class AddProfile(CreateView):
    model = Profile
    template_name = 'cms/employee/add_complaint.html'
    form_class = AddProfileForm

    def post(self, request, *args, **kwargs):
        pu = request.user.pu
        name = request.POST['name']
        picture = request.FILES.get('picture', False)
        qualifications = request.POST['qualifications']
        skills = request.POST['skills']
        gpa = request.POST['gpa']
        about = request.POST['about']
        Profile.objects.create(pu=pu, name=name, picture=picture, university=pu.user.organization_name,
                               qualifications=qualifications,
                               skills=skills, gpa=gpa, about=about)
        return redirect('cms:emp_dashboard')


@method_decorator([login_required, company_required()], name='dispatch')
class CompDashboard(ListView):
    model = Profile
    template_name = 'cms/company/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.user.company
        context['profiles'] = Profile.objects.all()
        context['organization'] = self.request.user.organization_name
        context['jobs'] = self.request.user.company.job_set.all()
        return context


@method_decorator([login_required, company_required()], name='dispatch')
class CompAddJob(CreateView):
    model = Job
    template_name = 'cms/company/add_job.html'
    form_class = AddJobForm

    def post(self, request, *args, **kwargs):
        company = request.user.company
        if int(request.POST['salary']) > 0:
            Job.objects.create(company=company, position=request.POST['position'], salary=request.POST['salary'],
                               vacancy=request.POST['vacancy'])
        else:
            return redirect('cms:comp_add_job')
        return redirect('cms:comp_dashboard')


class CompJobView(CreateView):
    model = ShortListCandidates
    template_name = 'cms/company/job.html'
    form_class = ShortlistForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        job = self.kwargs['job'].replace('_', ' ')
        context['company'] = company
        context['job'] = company.job_set.get(position=job)
        context['profiles'] = Profile.objects.all()
        if self.request.user.company.shortlistcandidates_set.all().exists():
            context['shortlisted'] = self.request.user.company.shortlistcandidates_set.all()
        return context

    def post(self, request, *args, **kwargs):
        company = request.user.company
        job = self.kwargs['job'].replace('_', ' ')
        profile = Profile.objects.get(name=f'{request.POST.get("name")}')
        # name = request.POST.get('name')
        # name = request.POST
        if ShortListCandidates.objects.filter(profile=profile).exists():
            return redirect('cms:comp_job_detail', job)
        else:
            a = ShortListCandidates(profile=profile, company=company)
            a.save()
