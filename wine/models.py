from django.db import models

# Create your models here.
class WineData(models.Model):
    id = models.IntegerField(primary_key=True)
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
    wine_type = models.CharField(blank=True, null=True, max_length=100)
    country = models.CharField(blank=True, null=True, max_length=100)
    rating = models.TextField(blank=True, null=True)
    pickup_location = models.TextField(blank=True, null=True)
    vivino_link = models.TextField(blank=True, null=True)
    flavor_description = models.TextField(blank=True, null=True)
    pairing = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "wine_data"


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    length = models.IntegerField(default=0)
    stage_history = models.CharField(max_length=200, default="")


class Utterance(models.Model):
    # UTTERANCE_CATEGORY = ((0, "Start of conversation"), (1, "Ask wine"), (2, "Common"))
    id = models.AutoField(primary_key=True)
    user_side = models.TextField(blank=True, null=True, default="")
    ai_side = models.TextField(blank=True, null=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    time_to_response = models.IntegerField(default=0)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    # text = models.TextField(max_length=500)  ## 발화내용
    stage = models.IntegerField(blank=True, null=True)
    # category = models.IntegerField(choices=UTTERANCE_CATEGORY)  ## 발화 카테고리


class WineRecommendation(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    utterance = models.ForeignKey(Utterance, on_delete=models.CASCADE)


class ChatExamples(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    utterance = models.ForeignKey(Utterance, on_delete=models.CASCADE)
    example = models.TextField(max_length=500, blank=True, null=True)


class WineBar(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    price_range = models.CharField(max_length=200, null=True, blank=True)
    parking = models.CharField(max_length=200, null=True, blank=True)
    opening_hours = models.CharField(max_length=200, null=True, blank=True)
    holidays = models.CharField(max_length=200, null=True, blank=True)
    menu = models.TextField(null=True, blank=True)
    img_url = models.TextField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
