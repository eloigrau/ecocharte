from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Adresse, Profil, Message, Choix, Commentaire_charte
from captcha.fields import CaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

no_space_validator = RegexValidator(
      r' ',
      ("Le pseudonyme ne doit pas contenir d'espaces"),
      inverse_match=True,
      code='invalid_tag',
  )

class AdresseForm(forms.ModelForm):
    code_postal = forms.CharField(label="Code postal*", )
    commune = forms.CharField(label="Commune*", )
    latitude = forms.FloatField(label="Latitude", initial="42", required=False,widget = forms.HiddenInput())
    longitude = forms.FloatField(label="Longitude", initial="2", required=False,widget = forms.HiddenInput())

    class Meta:
        model = Adresse
        exclude = ('latitude', 'longitude')

    def save(self, *args, **kwargs):
        adresse = super(AdresseForm, self).save(commit=False)
        adresse.set_latlon_from_adresse()
        adresse.save()
        return adresse

class ProfilCreationForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme*", help_text="Attention les majuscules sont importantes...", validators=[no_space_validator,])
    description = forms.CharField(label=None, help_text="Une description de vous même", required=False, widget=forms.Textarea)
    captcha = CaptchaField()
    email= forms.EmailField(label="Email*",)
    accepter_annuaire = forms.BooleanField(required=False, label="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous les inscrits")
    accepter_conditions = forms.BooleanField(required=True, label="J'ai lu et j'accepte les Conditions Générales d'Utilisation du site",  )

    class Meta(UserCreationForm):
        model = Profil
        fields = ['username', 'password1',  'password2', 'first_name', 'last_name', 'email',  'description', 'inscrit_newsletter', 'accepter_annuaire', 'accepter_conditions']
        exclude = ['slug', ]

    def save(self, commit = True, is_active=False):
        return super(ProfilCreationForm, self).save(commit)
        self.is_active=is_active



class ProfilChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme", validators=[no_space_validator,])
    description = forms.CharField(label="Description", help_text="Une description de vous-même", required=False)
    inscrit_newsletter = forms.BooleanField(required=False, label="J'accepte de recevoir des emails")
    accepter_annuaire = forms.BooleanField(required=False, label="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous")
    password=None

    class Meta:
        model = Profil
        fields = ['username', 'first_name', 'last_name', 'email',  'description', 'accepter_annuaire', 'inscrit_newsletter', 'a_signe']


class ProfilChangeForm_admin(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Pseudonyme", validators=[no_space_validator,])
    description = forms.CharField(label="Description", initial="Une description de vous même (facultatif)", widget=forms.Textarea)
    inscrit_newsletter = forms.BooleanField(required=False)
    accepter_annuaire = forms.BooleanField(required=False)
    a_signe = forms.BooleanField(required=False)
    password = None

    class Meta:
        model = Profil
        fields = ['username', 'email', 'description', 'inscrit_newsletter', 'accepter_annuaire', ]

    def __init__(self, *args, **kwargs):
        super(ProfilChangeForm_admin, self).__init__(*args, **kwargs)
class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100, label="Sujet",)
    msg = forms.CharField(label="Message", widget=forms.Textarea)
    renvoi = forms.BooleanField(label="recevoir une copie",
                                     help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False
                                 )


class MessageForm(forms.ModelForm):
    message = forms.CharField(max_length=100, label="Laisser un commentaire...",)

    class Meta:
        model = Message
        exclude = ['auteur', 'date_creation', 'type_article', 'type_message', 'valide']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 2}),
            }

    def __init__(self, request, message=None, *args, **kwargs):
        super(MessageForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['message'].initial = message



class CommentaireForm(forms.ModelForm):
    message = forms.CharField(max_length=500, label="Laisser un commentaire...",)

    class Meta:
        model = Commentaire_charte
        exclude = ['auteur', 'date_creation', 'type_message', 'valide', 'proposition']

        widgets = {
                'message': forms.Textarea(attrs={'rows': 2}),
            }

    def __init__(self, request, message=None, *args, **kwargs):
        super(CommentaireForm, self).__init__(request, *args, **kwargs)
        if message:
           self.fields['message'].initial = message


class SignerForm(forms.Form):
    renvoi = forms.BooleanField(label="J'ai lu la charte", required=True
                                 )
    accepter = forms.BooleanField(label="J'accepte les termes de la charte, et je m'engage à les appliquer", required=True
                                 )