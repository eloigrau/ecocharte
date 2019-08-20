from django.shortcuts import render, redirect
from django.db.models import CharField
from django.db.models.functions import Lower
from django.views.decorators.debug import sensitive_variables
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import mail_admins, send_mail, BadHeaderError
from .forms import ProfilCreationForm, ContactForm, AdresseForm, SignerForm, ProfilChangeForm, MessageForm
from .models import Profil, Adresse, Message
from django.views.generic import ListView, UpdateView, DeleteView

CharField.register_lookup(Lower, "lower")


def handler404(request, template_name="404.html"):  #page not found
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler500(request, template_name="500.html"):   #erreur du serveur
    response = render(request, "500.html")
    response.status_code = 500
    return response

def handler403(request, template_name="403.html"):   #non autorisé
    response = render(request, "403.html")
    response.status_code = 403
    return response

def handler400(request, template_name="400.html"):   #requete invalide
    response = render(request, "400.html")
    response.status_code = 400
    return response

def bienvenue(request):
    commentaires = Message.objects.filter(type_article="5").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article="5"
        comment.save()
        return redirect(request.path)

    return render(request, 'bienvenue.html', { 'form': form, 'commentaires': commentaires})


def presentation_site(request):
    return render(request, 'presentation_site.html')

def merci(request):
    return render(request, 'merci.html')

def gallerie(request):
    return render(request, 'gallerie.html')

def faq(request):
    return render(request, 'faq.html')

def statuts(request):
    return render(request, 'statuts.html')



@sensitive_variables('user', 'password1', 'password2')
def register(request):
    if request.user.is_authenticated:
        return render(request, "erreur.html", {"msg": "Vous etes déjà inscrit et authentifié !"})

    form_adresse = AdresseForm(request.POST or None)
    form_profil = ProfilCreationForm(request.POST or None)
    if form_adresse.is_valid() and form_profil.is_valid():
        adresse = form_adresse.save()
        profil_courant = form_profil.save(commit=False, is_active=False)
        profil_courant.adresse = adresse
        profil_courant.save()
        return render(request, 'userenattente.html')

    return render(request, 'register.html', {"form_adresse": form_adresse, "form_profil": form_profil, })


@login_required
class profil_modifier_user(UpdateView):
    model = Profil
    form_class = ProfilChangeForm
    template_name_suffix = '_modifier'
    fields = ['username', 'first_name', 'last_name', 'email', 'site_web', 'description', 'competences', 'pseudo_june',
              'accepter_annuaire', 'inscrit_newsletter']

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)


class profil_modifier_adresse(UpdateView):
    model = Adresse
    form_class = AdresseForm
    template_name_suffix = '_modifier'

    def get_object(self):
        return Adresse.objects.get(id=self.request.user.id)


class profil_modifier(UpdateView):
    model = Profil
    form_class = ProfilChangeForm
    template_name_suffix = '_modifier'

    # fields = ['username','email','first_name','last_name', 'site_web','description', 'competences', 'inscrit_newsletter']

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)


class profil_supprimer(DeleteView):
    model = Profil
    success_url = reverse_lazy('bienvenue')

    def get_object(self):
        return Profil.objects.get(id=self.request.user.id)


@sensitive_variables('password')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_changer_form.html', {
        'form': form
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None, )
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message_txt = request.user.username + " a envoyé le message suivant : "
            message_html = form.cleaned_data['msg']
            try:
                mail_admins(sujet, message_txt, html_message=message_html)
                if form.cleaned_data['renvoi']:
                    send_mail(sujet, message_txt, request.user.email, request.user.email, fail_silently=False, html_message=message_html)

                return render(request, 'message_envoye.html', {'sujet': sujet, 'msg': message_html,
                                                       'envoyeur': request.user.username + " (" + request.user.email + ")",
                                                       "destinataire": "administrateurs "})
            except BadHeaderError:
                return render(request, 'erreur.html', {'msg':'Invalid header found.'})

            return render(request, 'erreur.html', {'msg':"Désolé, une ereur s'est produite"})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, "isContactProfil":False})


def contact_admins(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None, )
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message_txt = request.user.username + " a envoyé le message suivant : "
            message_html = form.cleaned_data['msg']
            try:
                mail_admins(sujet, message_txt, html_message=message_html)
                if form.cleaned_data['renvoi']:
                    send_mail(sujet, message_txt, request.user.email, request.user.email, fail_silently=False, html_message=message_html)

                return render(request, 'message_envoye.html', {'sujet': sujet, 'msg': message_html,
                                                       'envoyeur': request.user.username + " (" + request.user.email + ")",
                                                       "destinataire": "administrateurs "})
            except BadHeaderError:
                return render(request, 'erreur.html', {'msg':'Invalid header found.'})

            return render(request, 'erreur.html', {'msg':"Désolé, une ereur s'est produite"})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, "isContactProducteur":False})

def cgu(request):
    return render(request, 'cgu.html', )

def fairedon(request):
    return render(request, 'fairedon.html', )

def liens(request):
    liens = [
        'https://jancovici.com/',
        'https://alternatiba.eu/alternatiba66/',
        'https://www.colibris-lemouvement.org/',
        'https://colibris-universite.org/mooc-permaculture/wakka.php?wiki=PagePrincipale',
        'https://ponteillanature.wixsite.com/eco-nature',
        'https://cce-66.wixsite.com/mysite',
        'https://jardindenat.wixsite.com/website',
        'https://www.permapat.com',
        'http://sel66.free.fr',
        'https://www.perma.cat',
        'http://soudaqui.cat/wordpress/',
        'https://framasoft.org',
        'http://www.le-message.org/?lang=fr',
        'https://reporterre.net/',
        'https://la-bas.org/',
        'https://www.monnaielibreoccitanie.org/',
        'http://lejeu.org/',
    ]
    #commentaires = Message.objects.filter(type_article="4", valide=True).order_by("date_creation")
    commentaires = Message.objects.filter(type_article="4").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article="4"
        comment.save()
        return redirect(request.path)

    return render(request, 'liens.html', {'liens':liens, 'form': form, 'commentaires': commentaires})



def introduction(request):
    commentaires = Message.objects.filter(type_article="0").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article="0"
        comment.save()
        return redirect(request.path)

    return render(request, '1_introduction.html', {'form': form, 'commentaires': commentaires}, )

def risques(request):
    dico_risques = [
        ("Ressources en berne :", "<ol><li>l'eau en danger: nappes phréatiques en net recul, pollués et salinisées, précipitations en forte diminution, assèchement des cours d'eau et des sols, </li><li> les sols pollués/détruits par l'agro-industrie, </li><li> l'approvisionnement énergétique en danger (principalement le pétrole), </li><li> approvisionnement en nourriture en danger (perte du secteur agricole local, diminution des rendements) </li><li> matériaux de construction importés, sans filières locales écologiques efficientes (bois, paille, briques, sable de construction, matériel électrique comme le cuivre qui s'épuise, etc)</li></ol>"),
        ("Risques naturels ", "<ol> <li> érosion des sols, </li>  <li> érosion du trait de cote, </li><li> inondations, </li><li> sécheresses,  </li><li>canicules,  </li><li>incendies. </li></ol>" \
                              "<p>Tous ces risquent augmentent considérablement et de façon non-linéaire (par paliers et donc 'crises') à cause du changement climatique</p>"),
        ("Agriculture en danger ", "disparition des terres agricoles, perte de rendements, disparition/pollution/salinisation de l'eau, sécheresses répétitives, perte des pollinisateurs de la biodiversité qui est nécessaire à l'agriculture. Modèle économique mondialisé, polluant, émetteur de CO2, dépendant du pétrole, appauvrissant la grande majorité des agriculteurs, et proche du krach."),
        ("Economie malade ", "seul le tourisme de masse et 'l'économie résidentielle' semblent être mis en valeur, détruisant ainsi nos nappes, folklorisant notre identité, ne créant que peu d'emplois et souvent saisonniers, à faible valeur ajoutée. Un fort trafic (encore du pétrole) dû à la métropolisation de Perpignan et l’éloignement des zones d'habitation avec les zones commerciales. Chômage massif, et travail au noir généralisé sont le lot de notre département."),
        ("Aménagement du territoire", " nos paysages sont modifiés par l'Homme de façon désordonnée, irresponsable et inadaptée aux futures crises, par <ol><li> l’appât du gain à court terme (champs d’éoliennes qui défigurent nos paysages sans être une réelle solution écologique, construction sur des terres agricoles fertiles, extension des grands centres commerciaux totalement inadaptés en cas de crise pétrolière, etc), sans parler de la corruption de nos 'élites locales', </li><li> la démographie excessive, sans contrôle du foncier </li><li> Un réseau de transport entièrement pensé avec un pétrole abondant, donc très vulnérable et polluant."),
        ("Identité ", " perte de notre culture catalane, de notre patrimoine culturel, artistique et linguistique. Ainsi c'est toute la cohésion du territoire qui est mise à mal. Sans reconnaissance de notre identité, il ne peut y avoir de solidarité, de projet commun et in fine d'organisation politique démocratique locale. Sans identité collective propre, point de salut collectif."),
        ("dépendance totale vis-à-vis de l’extérieur ", " approvisionnement en pétrole, monnaie sous contrôle des banques et des industries polluantes et émettrices de CO2,etc.. décisions politiques centralisées hors de nos frontières"),
    ]
    commentaires = Message.objects.filter(type_article="1").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article = "1"
        comment.save()
        return redirect(request.path)

    return render(request, '2_risques.html', {"dico_risques":dico_risques, 'form': form, 'commentaires': commentaires})

def preconisations(request):
    dico_risques = [ ("Soutien à l'agriculture (biologique et permacole) ",
                      " tous les agriculteurs doivent a minima passer en bio, et les collectivités doivent aider à la mise en place de fermes agro-écologiques. Ce sont des lieux individualisés ou collectifs de production (agricole et artisanale) qui peuvent : <ol><li> fournir de la nourriture locale et saine </li><li> gérer l'eau de façon durable </li><li> fournir du travail aux gens d'ici </li><li> gérer les stock de bois (énergie renouvelable et construction), </li><li> maintenir la biodiversité indispensable à notre survie, </li><li>créer du lien social, </li><li> optimiser l'usage des ressources, </li><li> être des lieux d'éducation, de formation et de citoyenneté.</li></ol>Il est aussi nécessaire de lutter contre tous les pesticides et engrais chimiques (qui dépendent aussi du pétrole, et qui polluent durablement nos sols et notre eau), et cela passe obligatoirement par des fermes agro-écologiques qui par leur multiples activités (élevage, maraichage, foresterie, etc) sont plus résilientes et peuvent amener des solutions alternatives aux pesticides et engrais."),

    ("Reforestation",
        "La reforestation du territoire doit être commencée au plus vite, en restaurant toutes les haies, les corridors écologiques (trame verte et bleue, etc), et en plantant des forets mixtes (fruitiers et non-fruitiers), y compris en zones urbaines. Les arbres sont un atout majeur et indispensable : ils apportent des fruits, du fourrage, de l'énergie renouvelable, stockent du carbone, créent des milieux favorables pour la faune et la flore (protection des oiseaux, des insectes, et de toute la chaine alimentaire), protègent les champignons, apportent de l'humus, protègent de l'évaporation et donc de la sécheresse mais aussi des inondations, apportent de l'ombre, et font remonter les minéraux et l'eau du sous-sol par leur système racinaire. Par ailleurs, il faut repenser la place des animaux dans notre société, dont une partie doit être traitée éthiquement (l'élevage non intensif) et une partie doit rester sauvage (protection renforcée des réserves naturelles) pour que le système agro-écologique soit résilient. Les races endémiques de notre région doivent être protégées (chèvre et vach de l'Albère, âne des pyrenées, etc.)"),
     ("Economie",
      "Le développement économique doit être re-pensé en incluant des limites : limites d'usage du sol, d'usage du pétrole, limite de la démographie. Refonder l'économie autour de l'agriculture est une solution possible. Le développement d'alternatives à la monnaie-dette 'euro' doit être encouragé et progressivement développé, pour se protéger d'une crise économique majeure de la zone euro (qui ne saurait tarder selon toute vraisemblance). La solution passe par l'utilisation croissante du Soudaqui (monnaie locale adossée à l'euro, pour l'instant) ou de la Monnaie Libre (monnaie sur internet basée sur la technologie de la 'blockchain''), dans une économie locale circulaire et équitable, notamment en payant une partie des salaires des fonctionnaires et élus locaux en monnaie alternative. Mais aussi en les utilisant dans les coopératives agricoles et les différentes filières restaurées ou crées ad hoc  (bois/énergie, paille/fourrage/construction, briques/construction. etc.)" ),
     ("Création d'assemblées citoyennes ", "pour informer, débattre, créer du lien, s'organiser localement sans attendre que les autres le fassent pour nous. Pour résoudre aussi les conflits qui vont se multiplier entre nous (la justice française n'est plus à la hauteur, et de plus en plus débordée et inefficace). Chaque commune doit pouvoir créer à sa façon des assemblées régulières et ayant un certain pouvoir sur les prises de décision au nom de la commune. Il est nécessaire d'impliquer toutes les bonnes volontés, et la population dans son ensemble doit pouvoir participer. Il s'agit d'inventer de nouvelles formes de gouvernance qui tiennent compte des enjeux et aspirations de notre époque. Cela va de pair avec la formation et l'éducation de la jeunesse, et de la population en général, aux enjeux écologiques, économiques, politiques et sociaux."),
     ("Créer des médias/réseaux sociaux locaux ", " Des plateformes open-source et libres comme www.perma.cat, ou bien des médias locaux (par exemple 'La Clau') peuvent être des exemples ou une base, qui permettent de s'affranchir des GAFA (Google Amazon Facebook, Apple), immenses pollueurs, et outils puissants de contrôle de la population à notre insu, et d'avoir une information locale plurielle, démocratique et utile à notre cohésion."),
     ("Formation aux (et développement des) 'low technologies' ", "diffusion des techniques non-industrielles que chacun peut se réapproprier avec peu de pétrole et peu de connaissances spécialisées (four solaire, 'rocket stove', velorution, etc)"),
     ("Gestion de l'eau", "réduction drastique de l'usage de l'eau pour préserver nos nappes phréatiques : toilettes sèches et récupération des eaux grises et des eaux de pluie. restauration des canaux historiques pour l'agriculture, création de retenues collinaires pour stocker les pluies, contrôle des forages, interdiction d'arroser les pelouses et limitation des piscines."),
     ("Décroissance", "limitation prévisionnelle des usages  (industries, transport, domestique) de l'énergie, afin d'anticiper leur diminution d'approvisionnement.")
    ]

    commentaires = Message.objects.filter(type_article="2").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article = "2"
        comment.save()
        return redirect(request.path)

    return render(request, '3_preconisations.html', {"dico_risques":dico_risques, 'form': form, 'commentaires': commentaires})

def charte(request):
    dico_charte =[
        ("1) Promouvoir l'agriculture ",
      ("Aider à la création de fermes agro-ecologiques",
       "Interdire tous les pesticides dans la commune",
       "Replanter les haies et créer des espaces arborés",
       "Que les cantines scolaires soient fournies de plus en plus par l'agriculture locale biologique ou permacole",
       "Faire un jardin potager au sein des établissement scolaires en lien avec les maraichers locaux",
       "Favoriser l'agriculture biologique et la permaculture dans ma commune",
       "Soutenir ou aider à la création de jardins partagés, ou jardins familiaux",
       "Soutenir ou aider à la création de coopératives agricoles",
      ),),

      ("2) Préserver les ressources",
       (" Limiter l'usage de l'eau au strict minimum",
        " Penser les transports du futur pour économiser l'energie: <ol><li> mobilité douce (vélo, charrettes, bateaux),</li><li>transports en commun (bus, taxi collectifs, espaces dédiés au covoiturage au sein de la commune, etc).</li><li>nouvelles technologies : bornes de rechargement pour les véhicules électriques, à partir d'énergie renouvelable et locale. Usine d'hydrogène, centrales solaires (thermiques et électriques), etc.</li></ol>",
        " Encourager la création d'une filière bois/énergie locale et durable",
        " Encourager la création d'une filière solaire et d'énergies renouvelables locale et durable",
        " Arrêter toute artificialisation des terres (n'accepter aucun nouveaux projet de construction qui ne soit pas vraiment eco-responsable)"
        ),),

     ("3) Développer l'économie locale en tenant compte de l'environnement en priorité",
      (" Préserver et valoriser notre patrimoine culturel, foncier et historique",
       " Aider au déploiement des monnaies alternatives",
       " Participer à la création de filières locales, en créant de l'économie circulaire",
       " Aider à la création de syndicats et coopératives agricoles citoyennes",
       " Créer une caisse de solidarité pour indemniser les victimes des futures catastrophes naturelles (pourquoi pas en monnaie alternative ?)",
       " Encourager le tourisme éco-responsable, et limiter les activités touristiques polluantes ou consommatrices  d'eau (golf, piscine privées, etc)",
       ),),

     ("4) Urbaniser intelligemment",
     (" préserver notre identité paysagère, respecter notre patrimoine architectural",
      " Végétaliser, reboiser, replanter les haies", "préserver les canaux d'arrosage",
      " Intégrer les activités agricoles dans la vie des villes et villages",
      " Utiliser des espaces pour organiser des lieux de vie et des assemblées collectifs",
      " Contrôler le foncier en n'oubliant pas d'intégrer les logements sociaux aux activités économiques",
      " Limiter l'étalement urbain", " favoriser les habitats légers, ou eco-responsables", "aménager des voies cyclables et de covoiturage",
      " Laisser de la place pour la faune et la flore sauvage",
      " Prendre soin des cours d'eau, et des canaux d'irrigation"),
      ),
      ("5) Contrôler la démographie ",
      ( " Limiter le tourisme de masse à basse valeur ajoutée en imposant des normes écologiques (par exemple taxer les ordures au delà d'un certain seuil, ou imposer un 'visa touristique' qui permette de traiter les dégats écologiques du tourisme)",
        " Contrôler le foncier",
        " Densifier les zones d'habitat",
        " Intégrer les nouveaux arrivants en les sensibilisant aux questions écologiques, politiques, économiques et identitaire.",
        " Inclure les personnes âgées dans les activités de la commune, notamment pour animer les assemblées locales.",
        " Accueillir dignement les migrants, du nord ou du sud, en les faisant participer à la vie des communes, notammant dans les activités des fermes agro-écologiques", ),
       ),
     ("6) Respecter notre identité et  ncourager la  citoyenneté ",
     ("Adopter la signalétique de la commune (nom des voies, monuments, affiches, etc) en catalan",
      "Respecter les traditions séculaires catalanes",
      "Favoriser le bilinguisme au sein des établissements scolaires",
      "Favoriser le bilinguisme au sein de la mairie et des actes publics",
      "Créer des assemblées locales citoyennes pour informer et débattre autour des enjeux du changement climatique et de la fin du pétrole.",
      "Proposer des salles pour développer le domaine associatif local",
      "Créer du lien et de la solidarité entre catalans (habitants et sympathisants du Pays Catalan)",
      ),)
    ]
    commentaires = Message.objects.filter(type_article="3").order_by("date_creation")
    form = MessageForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('login')
        comment = form.save(commit=False)
        comment.auteur = request.user
        comment.type_article="3"
        comment.save()
        return redirect(request.path)

    return render(request, 'charte.html', {"dico_charte":dico_charte, 'form': form, 'commentaires': commentaires})



@login_required
def profil_courant(request, ):
    return render(request, 'profil.html', {'user': request.user})


@login_required
def profil(request, user_id):
    try:
        user = Profil.objects.get(id=user_id)
        distance = user.getDistance(request.user)
        return render(request, 'profil.html', {'user': user, 'distance':distance})
    except User.DoesNotExist:
            return render(request, 'profil_inconnu.html', {'userid': user_id})

@login_required
def profil_nom(request, user_username):
    try:
        user = Profil.objects.get(username=user_username)
        distance = user.getDistance(request.user)
        return render(request, 'profil.html', {'user': user, 'distance':distance})
    except User.DoesNotExist:
        return render(request, 'profil_inconnu.html', {'userid': user_username})

@login_required
def signer(request):
    form_signer = SignerForm(request.POST or None)
    if form_signer.is_valid():
        profil_courant = Profil.objects.get(username=request.user.username)
        profil_courant.a_signe = True
        profil_courant.save()
        return render(request, 'merci.html')

    return render(request, 'signer.html', {"form_signer": form_signer, })