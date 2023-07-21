from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    is_employer = models.BooleanField('Is Employer', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)

class contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=500)
    message = models.TextField(max_length=10000)

    def __str__(self):
        return self.name + '  || ' + self.email 

class sectioned(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class job_time(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class post_job(models.Model):
    job_title = models.CharField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField(max_length=100000)
    responsibilities = models.TextField(max_length=10000)
    qualifications = models.TextField(max_length=1000)
    time = models.ForeignKey(job_time, on_delete=models.CASCADE)
    location = models.CharField(max_length=500)
    deadline = models.DateTimeField()
    post_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    job_for = models.ForeignKey(sectioned, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=600)
    company_address = models.CharField(max_length=600)
    company_email = models.EmailField(max_length=600)
    company_number = models.IntegerField()
    company_image = models.ImageField(upload_to="images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved = models.BooleanField('Approved', default=False)

    def save(self, *args, **kwargs):
        self.location = self.location.capitalize()  # Capitalize the first letter
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_title} (posted by {self.user.username})"






class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    job_post = models.ForeignKey(post_job, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username}, To: {self.receiver.username}, Job Post: {self.job_post.job_title}"



class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=600)
    address = models.CharField(max_length=600)
    email = models.EmailField(max_length=600)
    number = models.IntegerField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} (profile for {self.user.username})"




class report_job(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=900)
    contact =  models.IntegerField()
    comment = models.TextField(max_length=1000)
    posts = models.ForeignKey(post_job, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + str(self.posts)


class apply_job(models.Model):
    name = models.CharField(max_length=2000)
    email = models.EmailField(max_length=200)
    number = models.IntegerField()
    cv = models.FileField()
    information = models.TextField(blank=True, max_length=3000)
    job = models.ForeignKey(post_job, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.job.job_title}"


class details(models.Model):
    name = models.ForeignKey(post_job, on_delete=models.CASCADE)



class skilled_companies(models.Model):
    AVAILABILITY_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    logo = models.ImageField()
    email = models.EmailField()
    services  = models.CharField(max_length=2000)
    description = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)

    def __str__(self):
        return self.name + ' ' + self.location
    
    



class skilled_individuals(models.Model):
    AVAILABILITY_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    email = models.EmailField()
    services  = models.CharField(max_length=2000)
    description = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)

    def __str__(self):
        return self.name + ' ' + self.location


class Comment(models.Model):
    company = models.ForeignKey(skilled_companies, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.company)




class Comments(models.Model):
    company = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)





import secrets
from .paystack import PayStack



class Payment(models.Model):
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    job_id = models.IntegerField(default=0) 

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.email} - {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.completed = True
            self.save()
            return True
        return False
    
    

class MultipleImages(models.Model):
    images = models.FileField()
    post = models.ForeignKey(skilled_companies, on_delete=models.CASCADE)


class MultipleindImage(models.Model):
    images = models.ImageField(upload_to='images/')
    post = models.ForeignKey(skilled_individuals, on_delete=models.CASCADE)


