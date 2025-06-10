import os
import logging
import requests
from bs4 import BeautifulSoup
# import ollama
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import Facultate, Specializare, Grupa, UserProfile, Adevetinta, ConversationHistory
from .serializers import FacultateSerializer, SpecializareSerializer, GrupaSerializer, UserSerializer, UserProfileSerializer, AdevetintaSerializer, ConversationHistorySerializer
from .rag import RAG

# TODO: Pentru a folosi filtrul pentru specializare si grupa la final trebuie introdus .../?[numele variabilei respectiva]=[id-ul respectiv] 
# TODO: Pentru a descarca pdf-urile de pe site trebuie sa trimiti o cerere json goala "{}"

# ----------------------------------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------

class FacultateListView(generics.ListAPIView):
    queryset = Facultate.objects.all()
    serializer_class = FacultateSerializer


class FacultateCreateView(generics.CreateAPIView):
    queryset = Facultate.objects.all()
    serializer_class = FacultateSerializer


class FacultateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Facultate.objects.all()
    serializer_class = FacultateSerializer


class FacultateDeleteView(generics.DestroyAPIView):
    queryset = Facultate.objects.all()
    serializer_class = FacultateSerializer

class FacultateFilteredView(APIView):
    def get(self, request, *args, **kwargs):
        nume_facultate = request.query_params.get('nume')
        if nume_facultate:
            facultati = Facultate.objects.filter(nume__icontains=nume_facultate)
            serializer = FacultateSerializer(facultati, many=True)
            return Response(serializer.data)
        return Response({"error": "Selectarea facultatii este necesar"}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------------------------------------

class SpecializareListView(generics.ListAPIView):
    queryset = Specializare.objects.all()
    serializer_class = SpecializareSerializer


class SpecializareCreateView(generics.CreateAPIView):
    queryset = Specializare.objects.all()
    serializer_class = SpecializareSerializer


class SpecializareUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Specializare.objects.all()
    serializer_class = SpecializareSerializer


class SpecializareDeleteView(generics.DestroyAPIView):
    queryset = Specializare.objects.all()
    serializer_class = SpecializareSerializer


class SpecializareFilteredView(APIView):
    def get(self, request, *args, **kwargs):
        facultate = request.query_params.get('facultate')
        if facultate is not None:
            specializari = Specializare.objects.filter(facultate=facultate)
            serializer = SpecializareSerializer(specializari, many=True)
            return Response(serializer.data)
        return Response({"error": "Selectarea facultatii este necesar"}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------------

class GrupaListView(generics.ListAPIView):
    queryset = Grupa.objects.all()
    serializer_class = GrupaSerializer


class GrupaCreateView(generics.CreateAPIView):
    queryset = Grupa.objects.all()
    serializer_class = GrupaSerializer


class GrupaUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Grupa.objects.all()
    serializer_class = GrupaSerializer


class GrupaDeleteView(generics.DestroyAPIView):
    queryset = Grupa.objects.all()
    serializer_class = GrupaSerializer


class GrupaFilteredView(APIView):
    def get(self, request, *args, **kwargs):
        specializare = request.query_params.get('specializare')
        if specializare is not None:
            grupe = Grupa.objects.filter(specializare=specializare)
            serializer = GrupaSerializer(grupe, many=True)
            return Response(serializer.data)
        return Response({"error": "Selectarea specializare este necesar"}, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------------

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ----------------------------------------------------------------------------------------------------

class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({"error": "Toate campurile trebuie sa fie completate"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=identifier).first()

        if not user:
            user = User.objects.filter(username=identifier).first()

        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                refresh = RefreshToken.for_user(auth_user)
                access_token = str(refresh.access_token)
            
                return Response({
                    "message": "Autentificare reusita", 
                    "token": access_token, 
                    "user_id": auth_user.id,
                    "first_name": auth_user.first_name,
                    "last_name": auth_user.last_name,
                })
            else:
                return Response({"error": "Parola gresita"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Utilizatorul nu exista"}, status=status.HTTP_404_NOT_FOUND)
        
# ----------------------------------------------------------------------------------------------------

class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDeleteView(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# ----------------------------------------------------------------------------------------------------

class AdevetintaListView(generics.ListAPIView):
    queryset = Adevetinta.objects.all()
    serializer_class = AdevetintaSerializer


class AdevetintaCreateView(generics.CreateAPIView):
    queryset = Adevetinta.objects.all()
    serializer_class = AdevetintaSerializer


class AdevetintaUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Adevetinta.objects.all()
    serializer_class = AdevetintaSerializer


class AdevetintaDeleteView(generics.DestroyAPIView):
    queryset = Adevetinta.objects.all()
    serializer_class = AdevetintaSerializer

# ----------------------------------------------------------------------------------------------------

class ConversationChat(APIView):
    permission_classes = [AllowAny]
    rag = RAG()

    def post (self, request):
        try:
            question = request.data.get('message')

            if not question:
                return Response({"error": "Mesajul nu poate fi gol."}, status=status.HTTP_400_BAD_REQUEST)
            
            # message = [
            #     {"role": "system", "content": "Te rog sa raspunzi in limba romana, pe tine te cheama 'Alex' si esti asistentul virtual pentru 'Facultatea de Inginerie Electrica si Stiinta Calculatoarelor'."},
            #     {"role": "user", "content": question}
            # ]

            # response = ollama.chat(model="llama3.1", messages=message)
            # answer = response['message']['content']

            answer = self.rag.get_response(question)

            if request.user and request.user.is_authenticated:
                logger.info(f"User {request.user.username} is authenticated.")
                ConversationHistory.objects.create(
                    user=request.user,
                    question=question,
                    answer=answer
                )

            return Response({"answer" : answer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------------------------------------------------------------------------------

class ConversationHistoryListView(generics.ListAPIView):
    queryset = ConversationHistory.objects.all()
    serializer_class = ConversationHistorySerializer


class ConversationHistoryCreateView(generics.CreateAPIView):
    queryset = ConversationHistory.objects.all()
    serializer_class = ConversationHistorySerializer


class ConversationHistoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ConversationHistory.objects.all()
    serializer_class = ConversationHistorySerializer


class ConversationHistoryDeleteView(generics.DestroyAPIView):
    queryset = ConversationHistory.objects.all()
    serializer_class = ConversationHistorySerializer


class ConversationHistoryFilteredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.id != pk:
            return Response({"detail": "Nu ai permisiunea sa accesezi mesajele acestui utilizator."}, status=status.HTTP_403_FORBIDDEN)

        try:
            conversations = ConversationHistory.objects.filter(user__id=pk)

            serializer = ConversationHistorySerializer(conversations, many=True)

            return Response(serializer.data)

        except ConversationHistory.DoesNotExist:
            return Response({"detail": "Utilizatorul nu are mesaje."}, status=status.HTTP_404_NOT_FOUND)
# ----------------------------------------------------------------------------------------------------

class DownloadFilesView(APIView):
    def post(self, request):
        url = "https://fiesc.usv.ro/docs/"

        try:
            logger.info("Incepe descarcarea fisierelor .pdf/.doc/.docx de pe site: %s", url)
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            links = soup.find_all("a", href=True)
            file_urls = [link['href'] for link in links if link['href'].endswith(('.pdf', '.doc', '.docx'))]

            if not file_urls:
                logger.warning("Nu s-au gasit fisiere .pdf/.doc/.docx pe site.")
                return Response({"status": "warning", "message": "Nu s-au gasit fisiere .pdf/.doc/.docx pe site."}, status=status.HTTP_404_NOT_FOUND)
            
            base_dir = settings.BASE_DIR
            pdf_dir = os.path.join(base_dir, 'pdfs')
            docs_dir = os.path.join(base_dir, 'docs')
            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(docs_dir, exist_ok=True)

            for file_url in file_urls:
                try:
                    if not file_url.startswith("http"):
                        file_url = "https://fiesc.usv.ro" + file_url
                    file_name = file_url.split("/")[-1]
                    ext = os.path.splitext(file_name)[1].lower()

                    save_dir = pdf_dir if ext == '.pdf' else docs_dir
                    file_path = os.path.join(save_dir, file_name)

                    logger.info(f"Se descarca fisierul: {file_name}")
                    with requests.get(file_url, stream=True) as file_response:
                        file_response.raise_for_status()
                        with open(file_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                    
                    logger.info(f"Fisierul {file_name} a fost descarcat cu succes.")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Eroare la descarcarea fisierului {file_name}: {e}")
                    continue
            
            return Response({"status": "success", "message": "Fisierele au fost descarcate cu succes."}, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"erroare {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------------------------------------------------------------------------------

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        facultati = Facultate.objects.all()
        specializari = Specializare.objects.all()
        grupe = Grupa.objects.all()
        users = User.objects.all()
        user_profiles = UserProfile.objects.all()
        adeverinte = Adevetinta.objects.all()
        conversation_histories = ConversationHistory.objects.all()

        context['endpoints'] = [
            ('List Facultate', reverse_lazy('facultate-list')),
            ('Create Facultate', reverse_lazy('facultate-create')),
            *[('Update Facultate {}'.format(facultate.nume), reverse_lazy('facultate-update', kwargs={'pk': facultate.pk})) for facultate in facultati],
            *[('Delete Facultate {}'.format(facultate.nume), reverse_lazy('facultate-delete', kwargs={'pk': facultate.pk})) for facultate in facultati],
            ('Filter Facultate', reverse_lazy('facultate-filter')),

            ('List Specializare', reverse_lazy('specializare-list')),
            ('Create Specializare', reverse_lazy('specializare-create')),
            *[('Update Specializare {}'.format(specializare.nume), reverse_lazy('specializare-update', kwargs={'pk': specializare.pk})) for specializare in specializari],
            *[('Delete Specializare {}'.format(specializare.nume), reverse_lazy('specializare-delete', kwargs={'pk': specializare.pk})) for specializare in specializari],
            ('Filter Specializare', reverse_lazy('specializare-filter')),

            ('List Grupa', reverse_lazy('grupa-list')),
            ('Create Grupa', reverse_lazy('grupa-create')),
            *[('Update Grupa {}'.format(grupa.nume), reverse_lazy('grupa-update', kwargs={'pk': grupa.pk})) for grupa in grupe],
            *[('Delete Grupa {}'.format(grupa.nume), reverse_lazy('grupa-delete', kwargs={'pk': grupa.pk})) for grupa in grupe],
            ('Filter Grupa', reverse_lazy('grupa-filter')),

            ('Login', reverse_lazy('login')),

            ('List User', reverse_lazy('user-list')),
            ('Create User', reverse_lazy('user-create')),
            *[('Update User {}'.format(user.username), reverse_lazy('user-update', kwargs={'pk': user.pk})) for user in users],
            *[('Delete User {}'.format(user.username), reverse_lazy('user-delete', kwargs={'pk': user.pk})) for user in users],

            ('List User Profile', reverse_lazy('user-profile-list')),
            ('Create User Profile', reverse_lazy('user-profile-create')),
            *[('Update User Profile {}'.format(user_profile.nume), reverse_lazy('user-profile-update', kwargs={'pk': user_profile.pk})) for user_profile in user_profiles],
            *[('Delete User Profile {}'.format(user_profile.nume), reverse_lazy('user-profile-delete', kwargs={'pk': user_profile.pk})) for user_profile in user_profiles],

            ('List Adevetinta', reverse_lazy('adevetinta-list')),
            ('Create Adevetinta', reverse_lazy('adevetinta-create')),
            *[('Update Adevetinta {}'.format(adevetinta.nume), reverse_lazy('adevetinta-update', kwargs={'pk': adevetinta.pk})) for adevetinta in adeverinte],
            *[('Delete Adevetinta {}'.format(adevetinta.nume), reverse_lazy('adevetinta-delete', kwargs={'pk': adevetinta.pk})) for adevetinta in adeverinte],

            ('Conversation Chat', reverse_lazy('conversation-chat')),

            ('List Conversation History', reverse_lazy('conversation-history-list')),
            ('Create Conversation History', reverse_lazy('conversation-history-create')),
            *[('Update Conversation History {}'.format(conversation_history.nume), reverse_lazy('conversation-history-update', kwargs={'pk': conversation_history.pk})) for conversation_history in conversation_histories],
            *[('Delete Conversation History {}'.format(conversation_history.nume), reverse_lazy('conversation-history-delete', kwargs={'pk': conversation_history.pk})) for conversation_history in conversation_histories],
            *[('Filter Conversation History {}'.format(conversation_history.nume), reverse_lazy('conversation-history-filter', kwargs={'pk': conversation_history.pk})) for conversation_history in conversation_histories],

            ('Download Files', reverse_lazy('download-files'))
        ]
        return context

# ----------------------------------------------------------------------------------------------------
