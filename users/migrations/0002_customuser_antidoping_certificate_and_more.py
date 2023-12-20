# Generated by Django 4.2.8 on 2023-12-20 09:08

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='antidoping_certificate',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='certificates/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='has_valid_membership',
            field=models.BooleanField(default=False, verbose_name='valid membership'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='social_security_number',
            field=models.CharField(default=None, max_length=13, validators=[users.models.validate_ss], verbose_name='EMŠO'),
        ),
    ]
