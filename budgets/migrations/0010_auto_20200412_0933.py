# Generated by Django 2.2.8 on 2020-04-12 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0009_monthlybalancecategory_is_diff_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlybalancecategory',
            old_name='is_diff_currency',
            new_name='is_foreign_currency',
        ),
    ]
