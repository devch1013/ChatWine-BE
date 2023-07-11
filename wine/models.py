from django.db import models

# Create your models here.
class WineDetails(models.Model):
    url = models.TextField(blank=True, null=True)
    site = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    kr_name = models.TextField(blank=True, null=True)
    en_name = models.TextField(blank=True, null=True)
    img_url = models.TextField(blank=True, null=True)
    body = models.IntegerField(blank=True, null=True)
    acidity = models.IntegerField(blank=True, null=True)
    tannin = models.IntegerField(blank=True, null=True)
    sweetness = models.IntegerField(blank=True, null=True)
    alcohol = models.IntegerField(blank=True, null=True)
    wine_type = models.IntegerField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    pickup_location = models.TextField(blank=True, null=True)
    vivino_link = models.TextField(blank=True, null=True)
    flavor_description = models.TextField(blank=True, null=True)
    pairing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine_details'
        app_label = 'mysql_db'