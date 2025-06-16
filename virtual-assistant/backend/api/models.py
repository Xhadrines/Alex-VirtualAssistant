import logging
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# ----------------------------------------------------------------------------------------------------

# Creaza un logger
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------

class Facultate(models.Model):
    """
    Definirea modelului Facultate.
    """

    nume = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.nume}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza Facultatea: {self.nume}")
            
            super().save(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea Facultatea: {str(e)}")

# ----------------------------------------------------------------------------------------------------

class Specializare(models.Model):
    """
    Definirea modelului Specializare.
    """

    facultate = models.ForeignKey(Facultate, on_delete=models.CASCADE, related_name='specializari')

    nume = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nume} {self.facultate}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza Specializare: {self.nume} {self.facultate}")
            
            super().save(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea Specializare: {str(e)}")

# ----------------------------------------------------------------------------------------------------

class Grupa(models.Model):
    """
    Definirea modelului Grupa.
    """

    facultate = models.ForeignKey(Facultate, on_delete=models.CASCADE, related_name='grupe')
    specializare = models.ForeignKey(Specializare, on_delete=models.CASCADE, related_name='grupe')

    an_universitar = models.CharField(max_length=9)
    an_studiu = models.IntegerField()
    grupa = models.IntegerField()
    semigrupa = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.facultate} {self.specializare} {self.an_universitar} {self.an_studiu} {self.grupa} {self.semigrupa}"
    
    def nume(self):
        return f"{self.facultate}{self.specializare}{self.an_studiu}{self.grupa}{self.semigrupa}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza Grupa: {self.facultate} {self.specializare} {self.an_universitar} {self.an_studiu} {self.grupa} {self.semigrupa}")
            
            super().save(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea Grupa: {str(e)}")

# ----------------------------------------------------------------------------------------------------

class UserProfile(models.Model):
    """
    Definirea modelului UserProfile.
    """

    class TipTaxa(models.TextChoices):
        FARA_TAXA = 'fara taxa'
        CU_TAXA = 'cu taxa'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_student = models.IntegerField()
    facultate = models.ForeignKey(Facultate, on_delete=models.CASCADE)
    specializare = models.ForeignKey(Specializare, on_delete=models.CASCADE)
    grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE)
    tip_taxa = models.CharField(max_length=9, choices=TipTaxa)
    an_universitar = models.CharField(max_length=9)
    an_studiu = models.IntegerField()

    is_2fa_enable = models.BooleanField(default=False)
    totp_secret_key = models.CharField(max_length=32, blank=True, null=True)
    totp_enable_at = models.DateTimeField(blank=True, null=True)
    is_2fa_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.facultate} {self.specializare} {self.grupa} {self.is_2fa_enable} {self.totp_secret_key} {self.totp_enable_at} {self.is_2fa_verified}"
    
    def nume(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza UserProfile: {self.user} {self.facultate} {self.specializare} {self.grupa} {self.is_2fa_enable} {self.totp_secret_key} {self.totp_enable_at} {self.is_2fa_verified}")
            
            super().save(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea UserProfile: {str(e)}")

# ----------------------------------------------------------------------------------------------------

class Adevetinta(models.Model):
    """
    Definirea modelului Adevetinta.
    """

    class Status(models.TextChoices):
        IN_PROCESS = 'in_progress'
        COMPLETED = 'completed'
        REJECTED = 'rejected'

    class TipTaxa(models.TextChoices):
        FARA_TAXA = 'fara taxa'
        CU_TAXA = 'cu taxa'

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    an_universitar = models.CharField(max_length=9)
    an_studiu = models.IntegerField()
    specializare = models.CharField(max_length=150)
    tip_taxa = models.CharField(max_length=9, choices=TipTaxa)
    motiv = models.TextField()
    data_emitere = models.DateField(auto_now_add=True)
    numar = models.IntegerField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.IN_PROCESS)
    pdf_link = models.CharField(max_length=500, blank=True, null=True)
    is_downloaded = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user} {self.last_name} {self.first_name} {self.an_universitar} {self.an_studiu} {self.specializare} {self.motiv} {self.data_emitere} {self.numar} {self.status} {self.pdf_link} {self.is_downloaded} {self.expires_at}"
    
    def nume(self):
        return f"{self.last_name} {self.first_name}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza Adevetinta: {self.user} {self.last_name} {self.first_name} {self.an_universitar} {self.an_studiu} {self.specializare} {self.motiv[:50]} {self.data_emitere} {self.numar} {self.status} {self.pdf_link} {self.is_downloaded} {self.expires_at}")
            
            super().save(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea Adevetinta: {str(e)}")

# ----------------------------------------------------------------------------------------------------

class ConversationHistory(models.Model):
    """
    Definirea modelului ConversationHistory.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.question} {self.answer} {self.date_create}"
    
    def nume(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        try:
            logger.info(f"[{datetime.now()}] Se salveaza ConversationHistory: {self.user} {self.question[:50]} {self.answer[:50]} {self.date_create}")
            
            super().save(*args, **kwargs)

        except Exception as e:
            logger.error(f"[{datetime.now()}] Eroare la salvarea ConversationHistory: {str(e)}")

# ----------------------------------------------------------------------------------------------------
