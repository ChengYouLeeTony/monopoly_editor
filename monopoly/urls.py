from django.urls import re_path, path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from monopoly.views.game_view import GameView
from monopoly.views.join_view import JoinView
from monopoly.views.login_view import LoginView
from monopoly.views.profile_view import ProfileView
from monopoly.views.register_confirm_view import ConfirmRegistrationView
from monopoly.views.register_view import RegisterView
from monopoly.views.creator_view import CreatorHomeView, CreatorMyCardsetsListView, CreatorCardsetDetailView, PermissionRequiredView
from monopoly.views.cardset_form_view import CardsetCreateView
from monopoly.views.card_form_view import CardCreateView, CardEditView
from monopoly.views.map_form_view import MapCreateView, MapEditView, MapVariableView, MapRuleView, MapScoreBoardView, MapMusicSettingView, MapBackgroundSettingView, MapBasicSettingView
from monopoly.views.music_view import MusicListView
from monopoly.views.tutorial_view import TutorialView
from monopoly.views.cardset_gallery_view import CardsetGalleryView
from monopoly.views.map_gallery_view import MapGalleryView
from monopoly.views.thanks_view import ThanksView
from monopoly.views.img_download_view import ImgDownloadView
from monopoly.views.map_sample_view import MapSampleView

urlpatterns = [
    re_path(r'^$', CreatorHomeView.as_view(), name='creator-home-page'),
    re_path(r'^game/(?P<host_name>[@+-\.\w]+)/(?P<mode>.*)', login_required(GameView.as_view()), name='game'),
    re_path(r'^logout$', auth_views.logout_then_login, name='logout'),
    re_path(r'^login', LoginView.as_view(), name='login'),
    re_path(r'^profile/(?P<profile_user>.+)$', login_required(ProfileView.as_view()), name='profile'),
    re_path(r'^join/(?P<host_name>[@+-\.\w]*)/(?P<map_id>[-\w]+)', login_required(JoinView.as_view()), name="join"),
    re_path(r'^register', RegisterView.as_view(), name='register'),
    re_path(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        ConfirmRegistrationView.as_view(), name='confirm'),
    # re_path(r'^.*$', login_required(JoinView.as_view()), name="join"),
]

"""For cardset, card"""
urlpatterns += [
    path('creator/', CreatorHomeView.as_view(), name='creator-home-page'),
    #if user does not have permission to edit, redirect to here
    path('creator/permission-required',PermissionRequiredView.as_view(), name='permission-required'),
    #display user's cardsets
    path('creator/my-cardsets', login_required(CreatorMyCardsetsListView.as_view()), name='creator-my-cardsets'),
    #including update, delete cardset
    re_path(r'^creator/cardset/(?P<stub>[-\w]+)$', login_required(CreatorCardsetDetailView.as_view()), name='cardset-detail'),
    #create cardset
    path('creator/my-cardsets/create', login_required(CardsetCreateView.as_view()), name='cardset-create'),
    #create single card
    re_path(r'^creator/cardset/(?P<stub>[-\w]+)/card-create', login_required(CardCreateView.as_view()), name='card-create'),
    #edit single card
    re_path(r'^creator/cardset/(?P<stub>[-\w]+)/card-edit/(?P<card_id>\d+)', login_required(CardEditView.as_view()), name='card-edit'),
]


"""For map"""
from monopoly.views.creator_view import CreatorMyMapsListView, CreatorMapDetailView

urlpatterns += [
    #display user's maps
    path('creator/my-maps', login_required(CreatorMyMapsListView.as_view()), name='creator-my-maps'),
    #create new map
    path('creator/my-maps/create', login_required(MapCreateView.as_view()), name='map-create'),
    #edit or delete old map
    re_path(r'^creator/map/(?P<stub>[-\w]+)/edit', login_required(MapEditView.as_view()), name='map-edit'),
    #update map
    re_path(r'^creator/map/(?P<stub>[-\w]+)$', login_required(CreatorMapDetailView.as_view()), name='map-detail'),
    #making user define varible name
    re_path(r'^creator/map/(?P<stub>[-\w]+)/variables', login_required(MapVariableView.as_view()), name='map-making-variables'),
    #making user define rules
    re_path(r'^creator/map/(?P<stub>[-\w]+)/rules', login_required(MapRuleView.as_view()), name='map-making-rules'),
    #score board setting
    re_path(r'^creator/map/(?P<stub>[-\w]+)/score-board-setting', login_required(MapScoreBoardView.as_view()), name='map-score-board-setting'),
    #score board setting
    re_path(r'^creator/map/(?P<stub>[-\w]+)/music-setting', login_required(MapMusicSettingView.as_view()), name='music-setting'),
    #background setting
    re_path(r'^creator/map/(?P<stub>[-\w]+)/background-setting', login_required(MapBackgroundSettingView.as_view()), name='background-setting'),
    #basic setting
    re_path(r'^creator/map/(?P<stub>[-\w]+)/basic-setting', login_required(MapBasicSettingView.as_view()), name='basic-setting'),
]

"""For music and others"""
urlpatterns += [
    re_path(r'^creator/music/(?P<author>[-\w]+)', login_required(MusicListView.as_view()), name='music'),
    re_path(r'^creator/tutorial', login_required(TutorialView.as_view()), name='tutorial'),
    re_path(r'^creator/cardset-gallery', login_required(CardsetGalleryView.as_view()), name='cardset-gallery'),
    re_path(r'^creator/map-gallery', login_required(MapGalleryView.as_view()), name='map-gallery'),
    re_path(r'^creator/thanks', login_required(ThanksView.as_view()), name='thanks'),
    re_path(r'^creator/img-download', login_required(ImgDownloadView.as_view()), name='img-download'),
    re_path(r'^creator/map-sample', login_required(MapSampleView.as_view()), name='map-sample'),
]







