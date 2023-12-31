# Generated by Django 4.2 on 2023-05-09 15:05

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_employer', models.BooleanField(default=False, verbose_name='Is Employer')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is Employee')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='job_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='post_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('job_title', models.CharField(max_length=800)),
                ('job_description', models.TextField(max_length=100000)),
                ('responsibilities', models.TextField(max_length=10000)),
                ('qualifications', models.TextField(max_length=1000)),
                ('location', models.CharField(max_length=500)),
                ('deadline', models.DateTimeField()),
                ('company_name', models.CharField(max_length=600)),
                ('company_address', models.CharField(max_length=600)),
                ('company_email', models.EmailField(max_length=600)),
                ('company_number', models.IntegerField()),
                ('company_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.category')),
            ],
        ),
        migrations.CreateModel(
            name='sectioned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='skilled_companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField()),
                ('logo', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('services', models.CharField(max_length=2000)),
                ('description', models.TextField()),
                ('availability', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='skilled_individuals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('services', models.CharField(max_length=2000)),
                ('description', models.TextField()),
                ('availability', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='report_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email_address', models.EmailField(max_length=900)),
                ('contact', models.IntegerField()),
                ('comment', models.TextField(max_length=1000)),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.post_job')),
            ],
        ),
        migrations.AddField(
            model_name='post_job',
            name='job_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.sectioned'),
        ),
        migrations.AddField(
            model_name='post_job',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.job_time'),
        ),
        migrations.AddField(
            model_name='post_job',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('ref', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('job_id', models.IntegerField(default=0)),
                ('jobs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.post_job')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.post_job')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=600)),
                ('address', models.CharField(max_length=600)),
                ('email', models.EmailField(max_length=600)),
                ('number', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='portal.skilled_individuals')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='portal.skilled_companies')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='apply_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('email', models.EmailField(max_length=200)),
                ('number', models.IntegerField()),
                ('cv', models.FileField(upload_to='')),
                ('information', models.TextField(blank=True, max_length=3000)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.post_job')),
            ],
        ),
    ]
