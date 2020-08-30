# Generated by Django 2.2.13 on 2020-08-29 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0016_auto_20200814_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='text',
            field=models.CharField(default=None, max_length=40),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('text', 'created_by'), name='cat-per-user'),
        ),
    ]
