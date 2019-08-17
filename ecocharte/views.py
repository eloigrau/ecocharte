
from django.shortcuts import render, redirect
from django.db.models import CharField
from django.db.models.functions import Lower
from django.views.decorators.debug import sensitive_variables


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins, send_mail, BadHeaderError
#from django.views.generic import ListView, UpdateView, DeleteView
#from django.urls import reverse_lazy, reverse
#from django_summernote.widgets import SummernoteWidget
#from django import forms
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
    return render(request, 'bienvenue.html', {})


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

    form_profil = ProfilCreationForm(request.POST or None)
    if form_profil.is_valid():
        profil_courant = form_profil.save(commit=False, is_active=False)
        profil_courant.save()
        return render(request, 'userenattente.html')

    return render(request, 'register.html', {"form_profil": form_profil, })


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


def charte(request):
    return render(request, 'asso/charte.html', )

def cgu(request):
    return render(request, 'cgu.html', )

@login_required
def liens(request):
    liens = [
        'http://soudaqui.cat/wordpress/',
        'https://www.colibris-lemouvement.org/',
        'https://colibris-universite.org/mooc-permaculture/wakka.php?wiki=PagePrincipale',
        'https://ponteillanature.wixsite.com/eco-nature',
        'https://cce-66.wixsite.com/mysite',
        'https://jardindenat.wixsite.com/website',
        'https://www.permapat.com',
        'https://framasoft.org',
        'https://alternatiba.eu/alternatiba66/',
        'http://www.le-message.org/?lang=fr',
        'https://reporterre.net/',
        'https://la-bas.org/',
        'http://sel66.free.fr',
        'https://www.monnaielibreoccitanie.org/',
        'http://lejeu.org/',
    ]
    return render(request, 'liens.html', {'liens':liens})

def fairedon(request):
    return render(request, 'fairedon.html', )


def introduction(request):
    return render(request, '1_introduction.html', )

def risques(request):
    dico_risques = [
        ("Ressources en berne :", "<ol><li>l'eau en danger: nappes phréatiques en net recul, pollués et salinisées, précipitations en forte diminution, assèchement des cours d'eau et des sols, </li><li> les sols pollués/détruits par l'agro-industrie, </li><li> l'approvisionnement énergétique en danger (principalement le pétrole), </li><li> approvisionnement en nourriture en danger (perte du secteur agricole local, diminution des rendements) </li>²<li> matériaux de construction importés, sans filières locales écologiques efficientes (bois, paille, briques, sable de construction, matériel électrique comme le cuivre qui s'épuise, etc)</li></ol>"),
        ("Risques naturels ", "<ol> <li> érosion des sols, </li>  <li> érosion du trait de cote, </li><li> inondations, </li><li> sécheresses,  </li><li>canicules,  </li><li>incendies. </li></ol>" \
                              "<p>Tous ces risquent augmentent considérablement et de façon non -linéaire (par paliers et donc 'crises') à cause du changement climatique</p>"),
        ("Agriculture en danger ", "disparition des terres agricoles, perte de rendements, disparition/pollution/salinisation de l'eau, sécheresses répétitives, perte des pollinisateurs de la biodiversité qui est nécessaire à l'agriculture. Modèle économique mondialisé, polluant, émetteur de CO2, dépendant du pétrole, appauvrissant la grande majorité des agriculteurs, et proche du krach."),
        ("Economie malade ", "seul le tourisme de masse et 'l'économie résidentielle' semblent être mis en valeur, détruisant ainsi nos nappes, folklorisant notre identité, ne créant que peu d'emplois et souvent saisonniers, à faible valeur ajoutée. Un fort trafic (encore du pétrole) dû à la métropolisation de Perpignan et l’éloignement des zones d'habitation avec les zones commerciales. Chômage massif, et travail au noir généralisé sont le lot de notre département."),
        ("Aménagement du territoire", " nos paysages sont modifiés par l'Homme de façon désordonnée, irresponsable et inadaptée aux futures crises, par <ol><li> l’appât du gain à court terme (champs d’éoliennes qui défigurent nos paysages sans être une réelle solution écologique, construction sur des terres agricoles fertiles, extension des grands centres commerciaux totalement inadaptés en cas de crise pétrolière, etc), sans parler de la corruption de nos 'élites locales', </li><li> la démographie excessive, sans contrôle du foncier </li><li> Un réseau de transport entièrement pensé avec un pétrole abondant, donc très vulnérable et polluant."),
        ("Identité ", " perte de notre culture catalane, de notre patrimoine culturel, artistique et linguistique. Ainsi c'est toute la cohésion du territoire qui est mise à mal. Sans reconnaissance de notre identité, il ne peut y avoir de solidarité, de projet commun et in fine d'organisation politique démocratique locale. Sans identité collective propre, point de salut collectif."),
        ("dépendance totale vis-à-vis de l’extérieur ", " approvisionnement en pétrole, monnaie sous contrôle des banques et des industries polluantes et émettrices de CO2,etc.. décisions politiques centralisées hors de nos frontières"),
    ]
    return render(request, '2_risques.html', {"dico_risques":dico_risques})

def preconisations(request):
    dico_risques = [ ("Soutien à l'agriculture (biologique et permacole) ", " tous les agriculteurs doivent a minima passer en bio, et les collectivités doivent aider à la mise en place de fermes agro-écologiques. Ce sont des lieux individualisés ou collectifs de production (agricole et artisanale) qui peuvent : <ol><li> fournir de la nourriture locale et saine </li><li> gérer l'eau de façon durable </li><li> fournir du travail aux gens d'ici </li><li> gérer les stock de bois (énergie renouvelable et construction), </li><li> maintenir la biodiversité indispensable à notre survie, </li><li>créer du lien social, </li><li> optimiser l'usage des ressources, </li><li> être des lieux d'éducation, de formation et de citoyenneté.</li></ol>Il est aussi nécessaire de lutter contre tous les pesticides et engrais chimiques (qui dépendent aussi du pétrole, et qui polluent durablement nos sols et notre eau), et cela passe obligatoirement par des fermes agro-écologiques qui par leur multiples activités (élevage, maraichage, foresterie, etc) sont plus résilientes et peuvent amener des solutions alternatives aux pesticides et engrais.")
        , ("Reforestation",
        "La reforestation du territoire doit être commencée au plus vite, en restaurant toutes les haies, les corridors écologiques (trame verte et bleue, etc), et en plantant des forets mixtes (fruitiers et non-fruitiers), y compris en zones urbaines. Les arbres sont un atout majeur et indispensable : ils apportent des fruits, du fourrage, de l'énergie renouvelable, stockent du carbone, créent des milieux favorables pour la faune et la flore (protection des oiseaux, des insectes, et de toute la chaine alimentaire), protègent les champignons, apportent de l'humus, protègent de l'évaporation et donc de la sécheresse mais aussi des inondations, apportent de l'ombre, et font remonter les minéraux et l'eau du sous-sol par leur système racinaire. Par ailleurs, il faut repenser la place des animaux dans notre société, dont une partie doit être traitée éthiquement (l'élevage non intensif) et une partie doit rester sauvage (protection renforcée des réserves naturelles) pour que le système agro-écologique soit résilient. Les races endémiques de notre région doivent être protégées (chèvre et vach de l'Albère, âne des pyrenées, etc.)"),
     ("Economie", "Le développement économique doit être re-pensé en incluant des limites : limites d'usage du sol, d'usage du pétrole, limite de la démographie. Refonder l'économie autour de l'agriculture est une solution possible. Le développement d'alternatives à la monnaie-dette 'euro' doit être encouragé et progressivement développé, pour se protéger d'une crise économique majeure de la zone euro (qui ne saurait tarder selon toute vraisemblance). La solution passe par l'utilisation croissante du Soudaqui (monnaie locale adossée à l'euro, pour l'instant) ou de la Monnaie Libre (monnaie sur internet basée sur la technologie de la 'blockchain''), dans une économie locale circulaire et équitable, notamment en payant une partie des salaires des fonctionnaires et élus locaux en monnaie alternative. Mais aussi en les utilisant dans les coopératives agricoles et les différentes filières restaurées ou crées ad hoc  (bois/énergie, paille/fourrage/construction, briques/construction. etc.)" ),
     ("Création d'assemblées citoyennes ", "pour informer, débattre, créer du lien, s'organiser localement sans attendre que les autres le fassent pour nous. Pour résoudre aussi les conflits qui vont se multiplier entre nous (la justice française n'est plus à la hauteur, et de plus en plus débordée et inefficace). Chaque commune doit pouvoir créer à sa façon des assemblées régulières et ayant un certain pouvoir sur les prises de décision au nom de la commune. Il est nécessaire d'impliquer toutes les bonnes volontés, et la population dans son ensemble doit pouvoir participer. Il s'agit d'inventer de nouvelles formes de gouvernance qui tiennent compte des enjeux et aspirations de notre époque. Cela va de pair avec la formation et l'éducation de la jeunesse, et de la population en général, aux enjeux écologiques, économiques, politiques et sociaux."),
     ("Créer des médias/réseaux sociaux locaux ", " (www.perma.cat peut être un exemple ou une base), qui permettent de s'affranchir des GAFA (Google Amazon Facebook, Apple), immenses pollueurs, et outils puissants de contrôle de la population à notre insu, et d'avoir une information locale plurielle, démocratique et utile à notre cohésion."),
     ("Formation aux (et développement des) 'low technologies' ", "diffusion des techniques non-industrielles que chacun peut se réapproprier avec peu de pétrole et peu de connaissances spécialisées (four solaire, 'rocket stove', velorution, etc)"),
     ("Gestion de l'eau", "réduction drastique de l'usage de l'eau pour préserver nos nappes phréatiques : toilettes sèches et récupération des eaux grises et des eaux de pluie. restauration des canaux historiques pour l'agriculture, création de retenues collinaires pour stocker les pluies, contrôle des forages, interdiction d'arroser les pelouses et limitation des piscines."),
     ("Décroissance", "limitation prévisionnelle des usages  (industries, transport, domestique) de l'énergie, afin d'anticiper leur diminution d'approvisionnement.")
    ]

    return render(request, '3_preconisations.html', {"dico_risques":dico_risques})


def charte(request):
    dico_charte = [


                     ]

    return render(request, '3_preconisations.html', {"charte":charte})
def fairedon(request):
    return render(request, 'fairedon.html', )

def contact(request):
    return render(request, 'contact.html', )
