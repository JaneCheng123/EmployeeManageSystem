# Generated by Django 2.1.5 on 2021-07-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeid', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('department', models.CharField(max_length=50)),
                ('hiredate', models.CharField(default='2000-01-01', max_length=50)),
                ('salary', models.IntegerField()),
                ('level', models.IntegerField(default=3)),
                ('subsidy', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
