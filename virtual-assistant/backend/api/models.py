from django.db import models

class ConversationHistory(models.Model):
    # Camp pentru stocarea intrebarii
    question = models.TextField()
    
    # Camp pentru stocarea raspunsului
    answer = models.TextField()
    
    # Camp pentru stocarea datei si orei la care a fost adaugat inregistrarea
    created_at = models.DateTimeField(auto_now_add=True)

    # Reprezentare string pentru obiectul ConversationHistory
    def __str__(self):
        return f"Q: {self.question} | A: {self.answer} | {self.created_at}"
