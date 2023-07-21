from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Message,Payment, contact, post_job, apply_job, report_job, Category,skilled_companies, skilled_individuals,skilled_individuals, Comments

class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={"class": "form-control" }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={ "class": "form-control"}) )
    

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"} ))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ "class": "form-control" }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.CharField(
        widget=forms.TextInput( attrs={"class": "form-control" }) )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_employee', 'is_employer')


class contactus(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets={
            'message': forms.TextInput(attrs={'class': 'form-control'})
        }


class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a category name'}),
        }



class post_job_form(forms.ModelForm):
    class Meta:
        model = post_job
        fields = ('company_name','company_address','company_email' ,'company_number', 'job_title','job_description','responsibilities','qualifications','time', 'location','deadline','category','job_for','company_image')
        widgets={
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
             'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
             'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
             'responsibilities': forms.Textarea(attrs={'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
           'time': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
           'deadline': forms.DateInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'job_for': forms.Select(attrs={'class': 'form-control'}),
            'company_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class apply_job_form(forms.ModelForm):
    class Meta:
        model = apply_job
        fields = ('name', 'email', 'number', 'information', 'cv') 



class report_job_form(forms.ModelForm):
    class Meta:
        model = report_job
        fields = ['name', 'email_address', 'contact', 'comment']
       

    def __init__(self, *args, **kwargs):
        post_id = kwargs.pop('post_id', None)
        super().__init__(*args, **kwargs)
        if post_id:
            try:
                self.instance.posts = post_job.objects.get(pk=post_id)
            except post_job.DoesNotExist:
                pass


from .models import CompanyProfile
class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'address', 'email', 'number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['number'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


from django import forms
from .models import skilled_companies

class skilled_company_form(forms.ModelForm):
    class Meta:
        model = skilled_companies
        fields = '__all__'
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'location': forms.TextInput(attrs={'class': 'form-control'}),
'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'services': forms.TextInput(attrs={'class': 'form-control'}),
'description': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
'availability': forms.Select(attrs={'class': 'form-control'}),
}


class skilled_individual_form(forms.ModelForm):
    class Meta:
        model = skilled_individuals
        fields = '__all__'
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'location': forms.TextInput(attrs={'class': 'form-control'}),
'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'services': forms.TextInput(attrs={'class': 'form-control'}),
'description': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
'availability': forms.Select(attrs={'class': 'form-control'}),
}


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('email', 'amount')
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': True, 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].initial = 20




from django import forms
from .models import skilled_companies, Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Use the Comments model instead of Comment
        fields = ('name', 'email', 'body')
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'body': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
}




class skilled_individual_form(forms.ModelForm):
    class Meta:
        model = skilled_individuals
        fields = ('name', 'location', 'phone_number', 'email', 'services', 'description', 'availability')



class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'body': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
}



from .models import MultipleImages,MultipleindImage
class MultipleImagesForm(forms.ModelForm):
    class Meta:
        model = MultipleImages
        fields = ('images',)
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class MultipleImageForms(forms.ModelForm):
    class Meta:
        model = MultipleindImage
        fields = ('images',)
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }


