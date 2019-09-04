# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
from django.urls import reverse, reverse_lazy
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
import decimal, math
import os
import requests
from django.template.defaultfilters import slugify

DEGTORAD=3.141592654/180

LATITUDE_DEFAUT = '42.6976'
LONGITUDE_DEFAUT = '2.8954'

class Choix():
    type_message = ('0','Commentaire'), ("1","Coquille"), ('2','Réflexion')
    type_article = ('0','intro'), ("1","constat"), ('2','preconisations'), ('3','charte'), ('4','liens'), ('5','accueil')

class Adresse(models.Model):
    code_postal = models.CharField(max_length=5, blank=True, null=True, default="66000")
    commune = models.CharField(max_length=50, blank=True, null=True, default="Perpignan")
    latitude = models.FloatField(blank=True, null=True, default=LATITUDE_DEFAUT)
    longitude = models.FloatField(blank=True, null=True, default=LONGITUDE_DEFAUT)


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.set_latlon_from_adresse()
        return super(Adresse, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('profil_courant')

    def __str__(self):
        if self.commune:
            return "("+str(self.id)+") "+self.commune 
        else:
            return "("+str(self.id)+") "+self.code_postal

    def __unicode__(self):
        return self.__str__()

    def set_latlon_from_adresse(self):
        address = self.code_postal
        if self.commune:
            address += " " + self.commune
        address += ", France"
        try:
            api_key = os.environ["GAPI_KEY"]
            api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
            api_response_dict = api_response.json()

            if api_response_dict['status'] == 'OK':
                self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        except:
            pass

    def get_latitude(self):
        if not self.latitude:
            return LATITUDE_DEFAUT
        return str(self.latitude).replace(",",".")

    def get_longitude(self):
        if not self.longitude:
            return LONGITUDE_DEFAUT
        return str(self.longitude).replace(",",".")


class Profil(AbstractUser):
    description = models.TextField(null=True, blank=True)
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
    date_registration = models.DateTimeField(verbose_name="Date de création", editable=False)
    inscrit_newsletter = models.BooleanField(verbose_name="J'accepte de recevoir des emails", default=False)
    accepter_conditions = models.BooleanField(verbose_name="J'ai lu et j'accepte les conditions d'utilisation du site", default=False, null=False)
    accepter_annuaire = models.BooleanField(verbose_name="J'accepte d'apparaitre dans l'annuaire du site et la carte et rend mon profil visible par tous", default=True)
    a_signe = models.BooleanField(verbose_name="J'ai signé la charte", default=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_registration = now()
        if not hasattr(self, 'adresse') or not self.adresse:
             self.adresse = Adresse.objects.create()
        return super(Profil, self).save(*args, **kwargs)

    def get_nom_class(self):
        return "Profil"

    def get_absolute_url(self):
        return reverse('profil', kwargs={'user_id':self.id})

    def getDistance(self, profil):
        x1 = float(self.adresse.latitude)*DEGTORAD
        y1 = float(self.adresse.longitude)*DEGTORAD
        x2 = float(profil.adresse.latitude)*DEGTORAD
        y2 = float(profil.adresse.longitude)*DEGTORAD
        x = (y2-y1) * math.cos((x1+x2)/2)
        y = (x2-x1)
        return math.sqrt(x*x + y*y) * 6371


    @property
    def inscrit_newsletter_str(self):
       return "oui" if self.inscrit_newsletter else "non"

class Message(models.Model):
    message = models.TextField(null=False, blank=False)
    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    type_message = models.CharField(max_length=10,
        choices=(Choix.type_message),
        default='0', verbose_name="type de commentaire")
    type_article = models.CharField(max_length=10,
        choices=(Choix.type_article),
        default='0', verbose_name="reaction à")
    valide = models.BooleanField(verbose_name="validé", default=False)

    def __unicode__(self):
        return self.__str()

    def __str__(self):
        return "(" + str(self.id) + ") " + str(self.auteur) + " " + str(self.date_creation)



class Domaine_charte(models.Model):
    titre = models.TextField(null=False, blank=False)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre)[:99]
        super(Domaine_charte, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

class Proposition_charte(models.Model):
    domaine = models.ForeignKey(Domaine_charte, on_delete=models.CASCADE)
    titre = models.TextField(null=False, blank=False)
    explication = models.TextField(blank=True)
    compteur_plus = models.IntegerField(default=0)
    compteur_moins = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre)[:99]
        super(Proposition_charte, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('voirPropositionCharte', kwargs={'slug':self.slug})


class Commentaire_charte(models.Model):
    proposition = models.ForeignKey(Proposition_charte, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    message = models.TextField(null=False, blank=True,)
    date_creation = models.DateTimeField(auto_now_add=True)
    type_message = models.CharField(max_length=10,
        choices=(Choix.type_message),
        default='0', verbose_name="type de commentaire")

    def __str__(self):
        return self.message

class Vote(models.Model):
    proposition = models.ForeignKey(Proposition_charte, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Profil, on_delete=models.CASCADE)
    type_vote=models.CharField(max_length=10,
        choices=((0, "neutre"), (1, "plus"), (2, "moins"), ),
        default='0', verbose_name="type de commentaire")


    def __str__(self):
        return self.type_vote