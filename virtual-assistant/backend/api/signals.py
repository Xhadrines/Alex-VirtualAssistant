import os
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Facultate, Specializare, Grupa, UserProfile, Adevetinta, ConversationHistory
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ----------------------------------------------------------------------------------------------------

# Creaza un logger
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    """
    Creaza un set de date prestabilite in baza de date dupa ce migrarea a fost aplicata.
    """

    if os.getenv('MIGRARI_FINITE', False):
        return
    
    os.environ['MIGRARI_FINITE'] = 'TRUE'

    logger.info("Se genereaza date default...")

    try:
        facultate_default, created = Facultate.objects.get_or_create(
            nume = "Facultatea de Inginerie Electrica si StiinTa Calculatoarelor"
        )

        logger.info(f"Facultate {'creata' if created else 'existenta'}: {facultate_default}")

        specializare_default, created = Specializare.objects.get_or_create(
            facultate = facultate_default, 
            nume = "Calculatoare"
        )

        logger.info(f"Specializare {'creata' if created else 'existenta'}: {specializare_default}")

        grupa_default, created = Grupa.objects.get_or_create(
            facultate = facultate_default,
            specializare = specializare_default,
            an_universitar = "2024/2025",
            an_studiu = 4,
            grupa = 2,
            semigrupa = "B"
        )

        logger.info(f"Grupa {'creata' if created else 'existenta'}: {grupa_default}")

        user_default, created = User.objects.get_or_create(
            username = "student",
            email = "alexandru.sandru@student.usv.ro",
            first_name = "Alexandru",
            last_name = "Sandru",
            is_superuser = False,
            is_staff = False,
            is_active = True,
        )

        if created:
            user_default.set_password("Parola#1")
            user_default.save()

        logger.info(f"User {'creata' if created else 'existenta'}: {user_default}")

        user_profile_default, created = UserProfile.objects.get_or_create(
            user = user_default,
            facultate = facultate_default,
            specializare = specializare_default,
            grupa = grupa_default
        )

        logger.info(f"UserProfile {'creata' if created else 'existenta'}: {user_profile_default}")

        next_year = datetime.now() + relativedelta(years=1)

        adeverinta_default, created = Adevetinta.objects.get_or_create(
            user = user_default,
            last_name = "Sandru",
            first_name = "Alexandru",
            an_universitar = "2024/2025",
            an_studiu = 4,
            specializare = "Calculatoare",
            motiv = "Motiv default",
            numar = 1,
            status = Adevetinta.Status.COMPLETED,
            pdf_link = None,
            is_downloaded = False,
            expires_at = timezone.make_aware(next_year)
        )

        logger.info(f"Adeverinta {'creata' if created else 'existenta'}: {adeverinta_default}")

        conversation_history_default, created = ConversationHistory.objects.get_or_create(
            user = user_default,
            question = "Ce faci?",
            answer = "Bine",
        )

        logger.info(f"Conversatie {'creata' if created else 'existenta'}: {conversation_history_default}")

        admin_default, created = User.objects.get_or_create(
            username = "admin",
            email = "admin",
            first_name = "admin",
            last_name = "admin",
            is_superuser = True,
            is_staff = True,
            is_active = True,
        )

        if created:
            admin_default.set_password("Admin#1")
            admin_default.save()

        logger.info(f"Admin {'creata' if created else 'existenta'}: {admin_default}")

        logger.info("S-a finalizat generarea datelor default.")

    except Exception as e:
        logger.error(f"Eroare la generarea datelor default: {e}")

    finally:
        os.environ['MIGRARI_FINITE'] = "TRUE"

# ----------------------------------------------------------------------------------------------------
