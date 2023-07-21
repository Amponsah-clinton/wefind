from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm,MessageForm, LoginForm, contactus,CommentForm, post_job_form,PaymentForm, apply_job_form, report_job_form, CompanyProfileForm, categoryform, skilled_company_form, skilled_individual_form
from django.contrib.auth import authenticate, login,  logout
from . models import contact,post_job,Comment,Message,sectioned, Category,CompanyProfile, skilled_companies, skilled_individuals, Payment
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import folium
import geocoder
from bs4 import BeautifulSoup
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse



def add_category(request):
    form = categoryform()
    if request.method == 'POST':
        form = contactus(request.POST)
        if form.is_valid():
            form.save()
            form = categoryform()
            return redirect('contact')
    return render(request,'addcategory.html',{'form':form})


def sign_up(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'user created'
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'signup.html', {'form': form, 'msg': msg})



def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_employer:
                login(request, user)
                return redirect('employer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
        else:
            messages.success(request, 'invalid login')
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('index')


def employer(request):
    return render(request,'employer.html')


def employee(request):
    return render(request,'employee.html')




from django.db.models import Count, Case, When, Value, IntegerField

def index(request):
    categories = Category.objects.annotate(
        total_jobs=Count(
            Case(
                When(post_job__approved=True, post_job__deadline__gte=timezone.now(), then=1),
                output_field=IntegerField()
            )
        )
    ).all()
    job_posts = post_job.objects.filter(deadline__gte=timezone.now())[:4]
    skilled_individuals_list = skilled_individuals.objects.all()[:4]
    return render(request, 'index.html', {'categories': categories, 'job_posts': job_posts, 'skilled_individuals_list': skilled_individuals_list})





def about(request):
    return render(request,'about.html')


from django.utils import timezone

def job_list(request):
    current_time = timezone.now()
    jobs = post_job.objects.filter(deadline__gt=current_time)
    sections = sectioned.objects.all()
    job = post_job.objects.filter(job_for__name="company", deadline__gt=current_time)
    homes = post_job.objects.filter(job_for__name="Home", deadline__gt=current_time)
    return render(request, 'job-list.html', {'jobs': jobs, 'sections': sections, 'job': job, 'homes': homes})




def job_detail(request, pk):
    job = post_job.objects.get(pk=pk)

    if request.method == 'POST':
        form = apply_job_form(request.POST, request.FILES)
        message_form = MessageForm(request.POST)

        if form.is_valid():
            apply_job = form.save(commit=False)
            apply_job.job = job
            apply_job.save()

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = job.user
            message.job_post = job
            message.save()
            return redirect('job_detail', pk=pk)
    else:
        form = apply_job_form(initial={'job': job})
        message_form = MessageForm()
    report_form = report_job_form()

    return render(request, 'job-detail.html', {'job': job, 'form': form, 'message_form': message_form, 'report_form': report_form})


    

def category(request):
    obj = Category.objects.all()
    return render(request,'category.html', {'obj':obj})


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    current_time = timezone.now()
    posts = post_job.objects.filter(category=category, deadline__gt=current_time)
    context = {'category': category, 'posts': posts}
    return render(request, 'each_category.html', context)




def testimonial(request):
    return render(request,'testimonial.html')


@login_required
def profile(request):
    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        company_profile = None
    num_jobs_posted = post_job.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CompanyProfileForm(instance=company_profile)
    context = {'form': form, 'company_profile': company_profile, 'num_jobs_posted': num_jobs_posted}
    return render(request, 'profile.html', context)



def employer_details(request):
    return render(request, 'employee_details.html')


def delete_job_post(request, pk):
    if request.user.is_authenticated:
        delete_it = post_job.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('job_list')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('index')
    






def contact(request):
    form = contactus()
    if request.method == 'POST':
        form = contactus(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                f'New message from {name} ({email}) ',
                message,
                 settings.EMAIL_HOST_USER,
                ['amponsahc306@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Message sent successfully')
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})




def privacy(request):
    return render(request,'privacy.html')
    

def terms(request):
    return render(request,'terms.html')
    



def post_a_job(request):
    cat = Category.objects.all()
    obj = sectioned.objects.all()
    if request.method == 'POST':
        form = post_job_form(request.POST, request.FILES)
        if form.is_valid():
            post_job = form.save(commit=False)
            post_job.user = request.user
            post_job.save()
            post_job = post_job_form()
            messages.success(request, 'Job posted successfully' )
            return redirect('job_list')
    else:
        form = post_job_form()
    return render(request, 'post_a_job.html', {'form': form, 'obj': obj,'cat':cat})




from django.urls import reverse
@never_cache
def map(request):
    searches = post_job.objects.all()
    m = folium.Map(location=[7.9465, -1.0232], zoom_start=7.4)
    fg = folium.FeatureGroup(name='Job locations')
    for search in searches:
        location = geocoder.osm(search.location)
        if location.lat is not None and location.lng is not None:
            lat = location.lat
            lng = location.lng
            country = location.country
            popup_content = f"<strong>{search.job_title}</strong><br><a href='/job/{search.pk}/'>Click here to view job details</a>"
            popup_text = BeautifulSoup(popup_content, 'html.parser').get_text()
            popup = folium.Popup(popup_content, max_width=2650)
            folium.Marker([lat, lng], tooltip='click for details', popup=popup).add_to(fg)
    fg.add_to(m)
    m = m._repr_html_()
    return render(request, 'map.html', {'m': m})






def admin_approval(request):
    obj = post_job.objects.all().order_by('-post_date')
    if request.user.is_superuser:
       if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            obj.update(approved=False)
            for x in id_list:
                post_job.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, 'Update successful') 
            return redirect('job_list')
            
       else:
            return render(request,'admin_approval.html',{'obj': obj})
    else:
        messages.success(request, 'You are not authorized')
        return redirect('index')
    return render(request,'admin_approval.html')


from django.contrib.auth.decorators import user_passes_test
def all_jobs(request):
    obj = post_job.objects.all()
    return render(request,'all_posted_jobs.html',{'obj':obj})
    

def search_results(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        jobbs = post_job.objects.filter(job_title__contains=searched)
        if jobbs.count() == 0:
            messages.warning(request, f"No jobs found for {searched}")
        return render(request,'search_results.html',{'searched':searched, 'jobbs':jobbs})

    else:
        return render(request,'search_results.html')


def employer_job_post(request, post_id=None):
    if request.method == 'POST':
        if 'delete' in request.POST:
            job_post = get_object_or_404(post_job, id=post_id)
            job_post.delete()
        elif 'update' in request.POST:
            pass
        return redirect('employer_job_post')
    else:
        job_posts = post_job.objects.filter(user=request.user).order_by('-post_date')
        return render(request, 'employer_job_post.html', {'job_posts': job_posts})





def skilled_individual(request):
    form = skilled_individual_form()
    if request.method == 'POST':
        form = skilled_individual_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('skilled_individual')
    else:
        form = skilled_individual_form()
    obj = skilled_individuals.objects.all()
    search_name = request.GET.get('search_name', '')
    search_location = request.GET.get('search_location', '')
    search_availability = request.GET.get('search_availability', '')
    if search_name:
        obj = obj.filter(name__icontains=search_name)
    if search_location:
        obj = obj.filter(location__icontains=search_location)
    if search_availability:
        obj = obj.filter(availability=search_availability)
    return render(request, 'skilled_individual.html', {'form': form, 'obj': obj, 'search_name': search_name, 'search_location': search_location, 'search_availability': search_availability})




def all_applicants(request):
    m_emails = Payment.objects.values_list('email', flat=True)
    user_posts = post_job.objects.filter(user=request.user)
    applicants = []
    for post in user_posts:
        post_applicants = post.apply_job_set.all()
        for applicant in post_applicants:
            applicants.append(applicant)
    is_superuser = request.user.is_superuser
    return render(request, 'all_applicants.html', {'applicants': applicants, 'm_emails': m_emails, 'is_superuser': is_superuser})



from django.shortcuts import render, get_object_or_404, redirect
from .models import skilled_individuals, Comments, MultipleindImage
from .forms import skilled_individual_form, CommentForm,CommentsForm, MultipleImageForms
from django.contrib.auth.decorators import login_required




def skilled_individual_details(request, id):
    company = get_object_or_404(skilled_individuals, id=id)
    new_comments = None

    if request.method == 'POST':
        form = skilled_individual_form(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('skilled_individual_details', id=id)
        else:
            comment_form = CommentsForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.company = company
                new_comment.save()
                return redirect('skilled_individual_details', id=id)
            else:
                image_form = MultipleImageForms(request.POST, request.FILES)
                if image_form.is_valid():
                    images = request.FILES.getlist('images')
                    for image in images:
                        MultipleindImage.objects.create(images=image, post=company)
                    return redirect('skilled_individual_details', id=id)
    else:
        form = skilled_individual_form(instance=company)
        comment_form = CommentForm()
        image_form = MultipleImageForms()

    comments = company.comments.filter(active=True)
    if new_comments is None:
        new_comments = Comments.objects.none()

    return render(request, 'skilled_individual_details.html', {'company': company, 'form': form, 'comments': comments, 'comment_form': comment_form, 'image_form': image_form, 'new_comments': new_comments})


# def skilled_individual_details(request, id):
#     company = get_object_or_404(skilled_individuals, id=id)
#     new_comments = None
#     if request.method == 'POST':
#         form = skilled_individual_form(request.POST, request.FILES, instance=company)
#         if form.is_valid():
#             form.save()
#             return redirect('skilled_individual_details', id=id)
#         else:
#             comment_form = CommentsForm(request.POST)
#             if comment_form.is_valid():
#                 new_comment = comment_form.save(commit=False)
#                 new_comment.company = company
#                 new_comment.save()
#                 return redirect('skilled_individual_details', id=id)
#     else:
#         form = skilled_individual_form(instance=company)
#         comment_form = CommentForm()
#     comments = company.comments.filter(active=True)
#     if new_comments is None:
#         new_comments = Comment.objects.none()
#     return render(request, 'skilled_individual_details.html', {'company': company, 'form': form, 'comments': comments, 'comment_form': comment_form, 'new_comments': new_comments})




def find_a_talent(request):
    return render(request, 'find_a_talent.html')



def skilled_company(request):
    obj = skilled_companies.objects.all()
    form = skilled_company_form()
    if request.method == 'POST':
        form = skilled_company_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('skilled_company')
    else:
        form = skilled_company_form()
    search_name = request.GET.get('search_name', '')
    search_location = request.GET.get('search_location', '')
    search_availability = request.GET.get('search_availability', '')
    if search_name:
        obj = obj.filter(name__icontains=search_name)
    if search_location:
        obj = obj.filter(location__icontains=search_location)
    if search_availability:
        obj = obj.filter(availability=search_availability)
    return render(request, 'skilled_company.html', {'form': form, 'obj':obj, 'search_name': search_name, 'search_location': search_location, 'search_availability': search_availability})




from .forms import MultipleImagesForm
from .models import skilled_companies, MultipleImages, Comment

def skilled_company_details(request, id):
    company = get_object_or_404(skilled_companies, id=id)
    new_comments = None
    if request.method == 'POST':
        form = skilled_company_form(request.POST, request.FILES, instance=company)
        images_form = MultipleImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        if images_form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                MultipleImages.objects.create(images=image, post=company)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.company = company  
            new_comment.save()
        return redirect('skilled_company_details', id=id)
    else:
        form = skilled_company_form(instance=company)
        images_form = MultipleImagesForm()
        comment_form = CommentForm()
    comments = company.comments.filter(active=True)
    if new_comments is None:
        new_comments = Comment.objects.none()
    images = company.multipleimages_set.all()  
    return render(request, 'skilled_company_details.html', {'form': form, 'images_form': images_form, 'company': company, 'comments': comments, 'comment_form': comment_form, 'new_comments': new_comments, 'images': images})









def Delete(request, id):
    obj = skilled_companies.objects.get(id=id)
    obj.delete()
    return redirect('skilled_company')


from django.http.request import HttpRequest
from django.http.response import HttpResponse


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment: Payment = payment_form.save(commit=False)
            if request.user.is_authenticated:
                payment.email = request.user.email
            payment.amount = 50
            payment.save()
            return render(request, 'make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
        initial['amount'] = 50
        payment_form = PaymentForm(initial=initial)
    return render(request, "initiate_payment.html", {"payment_form": payment_form,})




def verify_payment(request, ref: str):
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    if payment.verify_payment():
        messages.success(
            request, f"Payment Completed Successfully, GH₵ {payment.amount}."
        )
        messages.success(
            request, f"Your new credit balance is GH₵ {payment.user.credit}."
        )
        return redirect('index')

    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return redirect("initiate-payment")










































