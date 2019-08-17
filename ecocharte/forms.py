from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Produit, Produit_aliment, Produit_objet, Produit_service, Produit_vegetal, Adresse, Profil, Message, MessageGeneral, Choix, MessageGeneralPermacat
from captcha.fields import CaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

fieldsCommunsProduits = ['souscategorie', 'nom_produit',  'description', 'estUneOffre', 'estPublique',
                'unite_prix', 'prix',  'type_prix', 'date_debut', 'date_expiration', ]


class AdresseForm(forms.ModelForm):
    rue = forms.CharField(label="Rue", required=False)
    code_postal = forms.CharField(label="Code postal*", initial="66000")

    class Meta:
        model = Adresse


class ProfilCreationForm(UserCreationForm):
    username = forms.CharField(label="Pseudonyme*", help_text="Attention les majuscules sont importantes...")
    description = forms.CharField(label=None, help_text="Une description de vous même", required=False, widget=forms.Textarea)
    competences = forms.CharField(label=None, help_text="Par exemple: electricien, bouturage, aromatherapie, pépinieriste, etc...", required=False, widget=forms.Textarea, )
    captcha = CaptchaField()
    email= forms.EmailField(label="Email*",)

    accepter_annuaire = forms.BooleanField(required=False, label="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous les inscrits")
    accepter_conditions = forms.BooleanField(required=True, label="J'ai lu et j'accepte les Conditions Générales d'Utilisation du site",  )


    def __init__(self, request, *args, **kargs):
        super(ProfilCreationForm, self).__init__(request, *args, **kargs)
        self.fields['description'].strip = False
        self.fields['competences'].strip = False

    class Meta(UserCreationForm):
        model = Profil
        fields = ['username', 'password1',  'password2', 'first_name', 'last_name', 'email', 'description', 'inscrit_newsletter', 'accepter_conditions']
        exclude = ['slug', ]



class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100, label="Sujet",)
    msg = forms.CharField(label="Message", widget=SummernoteWidget)
    renvoi = forms.BooleanField(label="recevoir une copie",
                                     help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False
                                 )

