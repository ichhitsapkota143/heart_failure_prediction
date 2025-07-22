from django.db import models

class MAX30100Data(models.Model):
    spo2 = models.FloatField()
    bpm = models.FloatField()
    glucose = models.FloatField()
    cholesterol = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ECGData(models.Model):
    ecg_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
