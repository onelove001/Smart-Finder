# Generated by Django 3.1.4 on 2021-03-02 01:45

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
            name='customUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('account_type', models.CharField(choices=[(1, 'Admin'), (2, 'Buyer'), (3, 'Seller')], default=1, max_length=9)),
                ('contacts', models.ManyToManyField(blank=True, related_name='_customuser_contacts_+', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_title', models.CharField(max_length=50)),
                ('image', models.FileField(upload_to='')),
                ('category_words', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contact_Us',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery_days',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Label_choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ordered', 'ordered'), ('paid', 'paid'), ('delivered', 'delivered'), ('rejected', 'rejected')], max_length=20)),
                ('date_ordered', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default=1, max_length=10)),
                ('image', models.FileField(upload_to='')),
                ('description', models.TextField()),
                ('verified', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sell', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='star_rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating_star', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Xperienece_level',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_acc', models.FloatField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_category_title', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('charge', models.FloatField()),
                ('description', models.TextField()),
                ('function', models.TextField()),
                ('image1', models.FileField(upload_to='')),
                ('image2', models.FileField(upload_to='')),
                ('image3', models.FileField(upload_to='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('days', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.delivery_days')),
                ('orders', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.plan')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='seller',
            name='experience_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.xperienece_level'),
        ),
        migrations.AddField(
            model_name='seller',
            name='label',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.label_choice'),
        ),
        migrations.AddField(
            model_name='seller',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.language'),
        ),
        migrations.AddField(
            model_name='seller',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subcategory'),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review_content', models.TextField()),
                ('date_reviewed', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.star_rating')),
                ('seller_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.seller')),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.service')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review_notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.reviews')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('budget', models.IntegerField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request_replies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reply_text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.requests')),
            ],
        ),
        migrations.CreateModel(
            name='Reply_notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_replies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.request_replies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order_notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='seller_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.seller'),
        ),
        migrations.AddField(
            model_name='order',
            name='service_ordered',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sellerss', to='core.seller'),
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=20)),
                ('image', models.FileField(upload_to='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Added_skills',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=50)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller')),
            ],
        ),
    ]
