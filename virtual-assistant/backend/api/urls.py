from django.urls import path
from .views import *

# ----------------------------------------------------------------------------------------------------

urlpatterns = [
    path('facultate/list/', FacultateListView.as_view(), name='facultate-list'),
    path('facultate/create/', FacultateCreateView.as_view(), name='facultate-create'),
    path('facultate/update/<int:pk>/', FacultateUpdateView.as_view(), name='facultate-update'),
    path('facultate/delete/<int:pk>/', FacultateUpdateView.as_view(), name='facultate-delete'),
    path('facultate/filter/', FacultateFilteredView.as_view(), name='facultate-filter'),

    path('specializare/list/', SpecializareListView.as_view(), name='specializare-list'),
    path('specializare/create/', SpecializareCreateView.as_view(), name='specializare-create'),
    path('specializare/update/<int:pk>/', SpecializareUpdateView.as_view(), name='specializare-update'),
    path('specializare/delete/<int:pk>/', SpecializareDeleteView.as_view(), name='specializare-delete'),
    path('specializare/filter/', SpecializareFilteredView.as_view(), name='specializare-filter'),

    path('grupa/list/', GrupaListView.as_view(), name='grupa-list'),
    path('grupa/create/', GrupaCreateView.as_view(), name='grupa-create'),
    path('grupa/update/<int:pk>/', GrupaUpdateView.as_view(), name='grupa-update'),
    path('grupa/delete/<int:pk>/', GrupaDeleteView.as_view(), name='grupa-delete'),
    path('grupa/filter/', GrupaFilteredView.as_view(), name='grupa-filter'),

    path('login/', LoginView.as_view(), name='login'),

    path('user/list/', UserListView.as_view(), name='user-list'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),

    path('user/profile/list/', UserProfileListView.as_view(), name='user-profile-list'),
    path('user/profile/create/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('user/profile/update/<int:pk>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('user/profile/delete/<int:pk>/', UserProfileDeleteView.as_view(), name='user-profile-delete'),

    path('adevetinta/list/', AdevetintaListView.as_view(), name='adevetinta-list'),
    path('adevetinta/create/', AdevetintaCreateView.as_view(), name='adevetinta-create'),
    path('adevetinta/update/<int:pk>/', AdevetintaUpdateView.as_view(), name='adevetinta-update'),
    path('adevetinta/delete/<int:pk>/', AdevetintaDeleteView.as_view(), name='adevetinta-delete'),

    path('conversation/chat/', ConversationChat.as_view(), name='conversation-chat'),

    path('conversation/history/list/', ConversationHistoryListView.as_view(), name='conversation-history-list'),
    path('conversation/history/create/', ConversationHistoryCreateView.as_view(), name='conversation-history-create'),
    path('conversation/history/update/<int:pk>/', ConversationHistoryUpdateView.as_view(), name='conversation-history-update'),
    path('conversation/history/delete/<int:pk>/', ConversationHistoryDeleteView.as_view(), name='conversation-history-delete'),
    path('conversation/history/filter/<int:pk>/', ConversationHistoryFilteredView.as_view(), name='conversation-history-filter'),

    path('download/files/', DownloadFilesView.as_view(), name='download-files'),
]
