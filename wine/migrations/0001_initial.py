# Generated by Django 4.2.3 on 2023-07-16 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WineData',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.TextField(blank=True, null=True)),
                ('site', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('kr_name', models.TextField(blank=True, null=True)),
                ('en_name', models.TextField(blank=True, null=True)),
                ('img_url', models.TextField(blank=True, null=True)),
                ('body', models.IntegerField(blank=True, null=True)),
                ('acidity', models.IntegerField(blank=True, null=True)),
                ('tannin', models.IntegerField(blank=True, null=True)),
                ('sweetness', models.IntegerField(blank=True, null=True)),
                ('alcohol', models.IntegerField(blank=True, null=True)),
                ('wine_type', models.IntegerField(blank=True, null=True)),
                ('country', models.IntegerField(blank=True, null=True)),
                ('rating', models.TextField(blank=True, null=True)),
                ('pickup_location', models.TextField(blank=True, null=True)),
                ('vivino_link', models.TextField(blank=True, null=True)),
                ('flavor_description', models.TextField(blank=True, null=True)),
                ('pairing', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'wine_data',
                'managed': True,
            },
        ),
    ]
