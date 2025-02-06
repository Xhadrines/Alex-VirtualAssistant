from django.db import models  # Importa modulul models din Django

class ConversationHistory(models.Model):
    """
    Modelul ConversationHistory reprezinta istoricul unui dialog, cu intrebari si raspunsuri.
    Acest model va fi utilizat pentru stocarea intrebarilor si raspunsurilor intr-o baza de date,
    impreuna cu data si ora crearii acestora.
    """
    question = models.TextField()  # Campul care stocheaza intrebarea
    answer = models.TextField()    # Campul care stocheaza raspunsul
    created_at = models.DateTimeField(auto_now_add=True)  # Campul care stocheaza data si ora crearii inregistrarii

    def __str__(self):
        """
        Definirea metodei __str__ pentru a reprezenta obiectul intr-un mod lizibil atunci cand este afisat.
        Aceasta va returna intrebarea, raspunsul si data/ora crearii in formatul 'Q: <intrebare> | A: <raspuns> | <data/ora>'.
        """
        return f"Q: {self.question} | A: {self.answer} | {self.created_at}"
