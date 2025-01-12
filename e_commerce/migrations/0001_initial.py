# Generated by Django 5.1 on 2024-08-18 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_num', models.CharField(max_length=15)),
                ('bill_address', models.CharField(max_length=100)),
                ('image', models.ImageField(default='default_user.jpg', upload_to='customers')),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Customers',
            },
        ),
    ]
