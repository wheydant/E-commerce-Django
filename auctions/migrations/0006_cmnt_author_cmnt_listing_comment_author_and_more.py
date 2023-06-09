# Generated by Django 4.2 on 2023-04-09 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_cmnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmnt',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userCmnt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cmnt',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lisitngCmnt', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lisitngComment', to='auctions.listing'),
        ),
    ]
