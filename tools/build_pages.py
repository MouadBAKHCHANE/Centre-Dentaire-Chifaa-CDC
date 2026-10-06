# -*- coding: utf-8 -*-
"""
Générateur des pages internes du site Centre Dentaire Chifaa.

L'accueil (index.html) est la source unique du header, du menu mobile, du footer
et des boutons flottants : ce script les recopie sur chaque page en convertissant
les liens en chemins absolus (/...). Modifier le header ou le footer = modifier
index.html puis relancer :

    python tools/build_pages.py

Pages produites (dossier/index.html, URL propres sur Vercel) :
  /soins/ (page mère), /soins/<spécialité>-meknes/  x6, /le-cabinet/, /contact/,
  /mentions-legales/, /politique-de-confidentialite/, /equipements/,
  /blog/ + /blog/<article>/ (contenus dans tools/articles.py), + sitemap.xml
"""
import json, os, re, sys, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.centredentairechifaa.ma'
VER = '20261006e'          # version de dark.css / dark.js (cache navigateur)
EMAIL = 'centredentairechifaa@gmail.com'
ICE = '003546775000034'
ORDRE = '7326'
BOOK = 'https://dentisto.ma/rendez-vous/docteurs/taoufik-boukadous-2112'
MAPS = 'https://maps.app.goo.gl/aMVAGuZqDNjD9A5PA'
WA = 'https://wa.me/message/MDYCV375HLAJO1'

ORB = ('<span class="btn-orb" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M17 7l-10 10"/><path d="M8 7h9v9"/></svg></span>')
LB_IC = ('<span class="tp-lb-ic" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h4v4"/>'
         '<path d="M14 10l6 -6"/><path d="M8 20h-4v-4"/><path d="M4 20l6 -6"/></svg></span>')

def ic(d):
    return ('<span class="tp-meta-ic" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</svg></span>' % d)

ICONS = {
    'shield': '<path d="M12 3a12 12 0 0 0 8.5 3a12 12 0 0 1 -8.5 15a12 12 0 0 1 -8.5 -15a12 12 0 0 0 8.5 -3"/><path d="M9 12l2 2l4 -4"/>',
    'users': '<path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"/><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/><path d="M21 21v-2a4 4 0 0 0 -3 -3.85"/>',
    'tool': '<path d="M7 10h3v-3l-3.5 -3.5a6 6 0 0 1 8 8l6 6a2 2 0 0 1 -3 3l-6 -6a6 6 0 0 1 -8 -8l3.5 3.5"/>',
    'cal': '<path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z"/><path d="M16 3v4"/><path d="M8 3v4"/><path d="M4 11h16"/>',
    'clock': '<path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"/><path d="M12 7v5l3 3"/>',
    'user': '<path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/>',
    'pin': '<path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/><path d="M17.657 16.657l-4.243 4.243a2 2 0 0 1 -2.827 0l-4.244 -4.243a8 8 0 1 1 11.314 0z"/>',
    'phone': '<path d="M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2"/>',
    'scan': '<path d="M4 8v-2a2 2 0 0 1 2 -2h2"/><path d="M4 16v2a2 2 0 0 0 2 2h2"/><path d="M16 4h2a2 2 0 0 1 2 2v2"/><path d="M16 20h2a2 2 0 0 0 2 -2v-2"/><path d="M7 12h10"/>',
    'mail': '<path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10z"/><path d="M3 7l9 6l9 -6"/>',
    'heart': '<path d="M19.5 12.572l-7.5 7.428l-7.5 -7.428a5 5 0 1 1 7.5 -6.566a5 5 0 1 1 7.5 6.572"/>',
    'sparkle': '<path d="M16 18a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2zm0 -12a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2zm-7 12a6 6 0 0 1 6 -6a6 6 0 0 1 -6 -6a6 6 0 0 1 -6 6a6 6 0 0 1 6 6z"/>',
}

SOINS_ORDER = ['orthodontie', 'implants-dentaires', 'chirurgie-orale', 'parodontie', 'prothese-dentaire', 'pedodontie']
SOIN_NAME = {'orthodontie': 'Orthodontie', 'implants-dentaires': 'Implants dentaires', 'chirurgie-orale': 'Chirurgie orale',
             'parodontie': 'Parodontie', 'prothese-dentaire': 'Prothèse dentaire', 'pedodontie': 'Pédodontie'}

# --------------------------------------------------------------------------------------------
# Contenu des pages soins
# --------------------------------------------------------------------------------------------
SOINS = {
 'orthodontie': dict(
  title="Orthodontie à Meknès | Aligneurs & bagues – CDC",
  desc="Orthodontiste à Meknès : aligneurs invisibles et bagues métalliques, pour enfants et adultes. Devis écrit, noté 5,0/5. Tél 05 35 51 69 24.",
  h1="Orthodontiste à Meknès,<br>pour un sourire aligné.",
  hero=('orthodontie-bagues-aligneurs-meknes.jpg', 1200, 655),
  gallery=[('orthodontie-bagues-dents-meknes.jpg', "Bagues orthodontiques sur les dents, orthodontie à Meknès"),
           ('sourire-avant-orthodontie-meknes.jpg', "Dents chevauchées avant un traitement orthodontique"),
           ('sourire-apres-orthodontie-meknes.jpg', "Sourire aligné après un traitement orthodontique"),
           ('aligneurs-invisibles-orthodontie-meknes.jpg', "Aligneurs invisibles transparents pour l'orthodontie")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Orthodontie'), ('users', 'PATIENTS', 'Adultes, ados, enfants'), ('tool', 'TECHNIQUES', 'Aligneurs, bagues')],
        [('cal', 'DURÉE', '6 à 24 mois'), ('clock', 'CONTRÔLES', 'Toutes les 4 à 8 sem.'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Un traitement orthodontique planifié,<br>suivi et expliqué.",
  intro=["L'orthodontie corrige la position des dents et des mâchoires. Un sourire aligné n'est pas qu'une question d'esthétique : des dents bien placées se brossent mieux, s'usent moins et répartissent correctement les forces de mastication. Une occlusion déséquilibrée favorise au contraire caries, déchaussement, douleurs articulaires et usure prématurée.",
         "Au Centre Dentaire Chifaa, l'orthodontie à Meknès se pratique dans un centre pluridisciplinaire. Cela compte : un traitement s'accompagne souvent d'un bilan parodontal, d'une extraction ou d'une réhabilitation prothétique. Ici, tout est coordonné dans les mêmes murs."],
  who_h="Pour qui, et quand consulter ?",
  who_p="Il n'y a pas d'âge limite pour aligner ses dents. Les techniques actuelles traitent les adultes discrètement, et de plus en plus de patients de 30, 40 ou 50 ans entreprennent un traitement à Meknès. Chez l'enfant, une première consultation vers 7 ans permet de repérer tôt un décalage de croissance et de le corriger simplement, avant l'adolescence. Consultez si vous observez :",
  who=["Dents chevauchées ou espacées, par manque ou excès de place sur l'arcade",
       "Dents du haut trop en avant, menton en retrait ou décalage des mâchoires",
       "Béance ou supraclusion : les dents ne se touchent pas, ou se recouvrent trop",
       "Respiration par la bouche ou succion du pouce chez l'enfant",
       "Besoin de recréer l'espace avant un implant ou une prothèse"],
  treat_h="Nos traitements orthodontiques",
  treat=[("Aligneurs invisibles", "gouttières transparentes et amovibles, renouvelées toutes les une à deux semaines, conçues par empreinte numérique avec simulation du résultat. La solution privilégiée des adultes actifs."),
         ("Bagues métalliques", "l'appareil multi-attaches reste la référence pour les corrections complexes."),
         ("Orthodontie enfants et adolescents", "traitement interceptif dès 7 ans pour guider la croissance des mâchoires, puis traitement complet à l'adolescence."),
         ("Contention et suivi", "fil collé derrière les dents ou gouttière de nuit pour maintenir le résultat. Sans contention, les dents tendent à reprendre leur position initiale.")],
  steps=[("Consultation et radiographie 3D.", "Examen clinique, photos et radiographie panoramique ou cone beam sur place. Nous analysons la position des dents, des racines et des mâchoires."),
         ("Empreinte numérique.", "Un scanner intra-oral remplace la pâte à empreinte. Plus confortable, plus précis, et le plan de traitement est simulé à l'écran."),
         ("Plan de traitement et devis écrit.", "Technique, durée estimée, nombre de rendez-vous et devis détaillé. Rien ne commence sans votre accord."),
         ("Traitement actif.", "Pose de l'appareil ou remise des premières gouttières, puis contrôles toutes les 4 à 8 semaines, pendant 6 à 24 mois selon le cas."),
         ("Contention.", "Une fois l'alignement obtenu, la contention stabilise le résultat et des contrôles espacés vérifient que tout reste en place.")],
  price="Le coût d'un traitement orthodontique à Meknès dépend de la technique, de la complexité du cas et de sa durée. Nous préférons ne pas afficher de prix qui ne correspondrait pas à votre situation.",
  faq=[("À quel âge commencer un traitement orthodontique ?", "Une première visite vers 7 ans permet de dépister les problèmes de croissance. Le traitement complet se fait généralement entre 11 et 14 ans. Pour les adultes, il n'y a pas de limite : seul l'état des gencives et de l'os conditionne la faisabilité."),
       ("Combien de temps dure un traitement ?", "De 6 mois pour une correction légère par aligneurs à 18 ou 24 mois pour un cas complexe avec bagues. La durée précise vous est annoncée dans le plan de traitement."),
       ("Les aligneurs invisibles sont-ils aussi efficaces que les bagues ?", "Pour la majorité des cas, oui, à condition de les porter 20 à 22 heures par jour. Certains mouvements complexes restent mieux contrôlés avec des bagues. Nous vous indiquons honnêtement ce qui convient à votre cas."),
       ("Est-ce que ça fait mal ?", "Une gêne de quelques jours est normale après chaque activation ou changement de gouttière. Elle se gère avec un antalgique simple. La pose elle-même est indolore."),
       ("Peut-on faire de l'orthodontie avec des dents manquantes ou des couronnes ?", "Oui. C'est souvent l'occasion de préparer un implant ou une prothèse en recréant l'espace nécessaire. Orthodontie, implants et prothèse sont planifiés ensemble dans le même centre.")],
  related=[('parodontie', "des gencives saines avant et pendant le traitement"),
           ('chirurgie-orale', "extractions et dents de sagesse quand la place manque"),
           ('prothese-dentaire', "couronnes et facettes une fois l'alignement obtenu"),
           ('implants-dentaires', "remplacer une dent absente après avoir recréé l'espace")],
  proc_desc="Traitements orthodontiques pour adultes, adolescents et enfants au Centre Dentaire Chifaa, Meknès : aligneurs invisibles, bagues métalliques, orthodontie interceptive, contention.",
  proc_type="NoninvasiveProcedure",
 ),

 'implants-dentaires': dict(
  title="Implant dentaire à Meknès | Unitaire, All-on-4 – CDC",
  desc="Implants dentaires à Meknès : implant unitaire, bridge, All-on-4 et greffe osseuse, planifiés en radiographie 3D. Devis écrit. Tél 05 35 51 69 24.",
  h1="Implants dentaires à Meknès,<br>pour une dentition fixe.",
  hero=('implant-dentaire-pose-meknes.jpg', 1024, 768),
  gallery=[('implant-unitaire-couronne-3d.jpg', "Implant unitaire avec pilier et couronne"),
           ('implants-dentaires-3d.jpg', "Deux implants dentaires avec leurs couronnes"),
           ('all-on-4-implants-3d.jpg', "Prothèse complète All-on-4 sur quatre implants"),
           ('3d-implanto.jpg', "Planification d'un implant sur radiographie 3D")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Implantologie'), ('users', 'INDICATION', 'Une ou plusieurs dents'), ('tool', 'SOLUTIONS', 'Unitaire, bridge, All-on-4')],
        [('scan', 'PLANIFICATION', 'Radiographie 3D'), ('cal', 'CICATRISATION', '3 à 6 mois'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Remplacer une dent absente,<br>durablement et sans toucher aux voisines.",
  intro=["Un implant dentaire est une racine artificielle en titane, placée dans l'os de la mâchoire. Une fois intégré à l'os, il porte une couronne, un bridge ou une prothèse complète. Le résultat se comporte comme une dent naturelle : on mâche, on sourit et on parle sans y penser.",
         "Remplacer une dent manquante n'est pas qu'une question d'esthétique. Sans racine, l'os se résorbe, les dents voisines se déplacent et la mastication se déséquilibre. Contrairement au bridge classique, l'implant ne demande pas de tailler les dents adjacentes. Au Centre Dentaire Chifaa, chaque implant à Meknès est planifié sur une radiographie 3D réalisée au cabinet."],
  who_h="Pour qui, et dans quelles conditions ?",
  who_p="La pose d'implants concerne la plupart des adultes qui ont perdu une ou plusieurs dents, ou dont le dentier ne tient plus. Le bilan préalable vérifie que les conditions sont réunies. On en parle si vous êtes dans l'une de ces situations :",
  who=["Une dent absente ou à extraire, à l'avant comme à l'arrière",
       "Plusieurs dents manquantes côte à côte, à remplacer sans prothèse amovible",
       "Un dentier qui bouge et gêne pour manger ou parler",
       "Un volume d'os réduit, qui peut être reconstruit par greffe avant la pose",
       "Un tabagisme ou un diabète, à équilibrer pour sécuriser la cicatrisation"],
  treat_h="Nos solutions implantaires",
  treat=[("Implant unitaire", "une dent remplacée par un implant et une couronne en céramique, sans toucher aux dents voisines."),
         ("Bridge sur implants", "deux implants portent plusieurs dents fixes : la solution quand plusieurs dents manquent côte à côte."),
         ("All-on-4 et All-on-6", "une arcade complète fixe portée par quatre à six implants, pour les patients édentés ou dont les dents ne sont plus conservables."),
         ("Prothèse stabilisée sur implants", "un dentier clipsé sur deux à quatre implants : il ne bouge plus, tout en restant amovible pour le nettoyage."),
         ("Greffe osseuse et sinus lift", "quand l'os manque, il est reconstruit avant ou pendant la pose pour offrir une base solide à l'implant.")],
  steps=[("Consultation et radiographie 3D.", "Examen de la bouche, des gencives et de l'os. La radiographie 3D faite sur place mesure précisément le volume osseux disponible."),
         ("Plan de traitement et devis écrit.", "Nombre d'implants, type de prothèse, greffe éventuelle, calendrier et devis détaillé. Rien ne commence sans votre accord."),
         ("Pose de l'implant.", "Sous anesthésie locale, au cabinet. Une dent provisoire peut être prévue pour ne jamais rester sans sourire."),
         ("Cicatrisation.", "L'implant s'intègre à l'os pendant 3 à 6 mois selon la situation. Des contrôles vérifient la bonne évolution."),
         ("Prothèse définitive et suivi.", "Pose de la couronne ou du bridge sur mesure, réglage de l'occlusion, puis une visite de contrôle chaque année.")],
  price="Le coût d'un traitement implantaire à Meknès dépend du nombre d'implants, d'une éventuelle greffe osseuse et du type de prothèse posée dessus. Nous préférons ne pas afficher de prix qui ne correspondrait pas à votre situation.",
  faq=[("La pose d'un implant est-elle douloureuse ?", "La pose se fait sous anesthésie locale et n'est pas douloureuse. Les jours suivants, une gêne comparable à une extraction se gère avec des antalgiques simples et un peu de glace."),
       ("Combien de temps dure un implant ?", "Bien entretenu, un implant peut durer de très nombreuses années. Sa longévité dépend surtout de l'hygiène, de l'absence de tabac et des contrôles réguliers au cabinet."),
       ("Peut-on poser un implant quand l'os manque ?", "Souvent, oui. Une greffe osseuse ou un sinus lift reconstruit le volume nécessaire. La radiographie 3D permet de décider de la meilleure approche dès la première consultation."),
       ("Peut-on avoir des dents fixes le jour même ?", "Dans certains cas, une dent ou une arcade provisoire peut être posée le jour de l'intervention. Cela dépend de la qualité de l'os et se décide après l'examen."),
       ("Le diabète ou le tabac empêchent-ils la pose ?", "Pas forcément. Un diabète équilibré est compatible avec les implants. Le tabac augmente le risque d'échec : l'arrêter, au moins autour de la pose, améliore nettement le résultat.")],
  related=[('prothese-dentaire', "couronnes et bridges posés sur les implants"),
           ('chirurgie-orale', "extractions et greffes osseuses avant la pose"),
           ('parodontie', "des gencives saines pour protéger les implants"),
           ('orthodontie', "recréer l'espace avant de remplacer une dent")],
  proc_desc="Pose d'implants dentaires au Centre Dentaire Chifaa, Meknès : implant unitaire, bridge sur implants, All-on-4, prothèse stabilisée sur implants, greffe osseuse, planification sur radiographie 3D.",
  proc_type="SurgicalProcedure",
 ),

 'chirurgie-orale': dict(
  title="Chirurgie orale à Meknès | Dents de sagesse – CDC",
  desc="Chirurgie orale à Meknès : dents de sagesse, extractions complexes et chirurgie pré-implantaire, sous anesthésie locale. Tél 05 35 51 69 24.",
  h1="Chirurgie orale à Meknès,<br>au cabinet, sous anesthésie locale.",
  hero=('chirurgie-orale-extraction-3d.jpg', 800, 600),
  gallery=[('radio-panoramique-dents-sagesse.jpg', "Radiographie panoramique des mâchoires et des dents de sagesse"),
           ('dent-de-sagesse-incluse.jpg', "Illustration d'une dent de sagesse incluse"),
           ('dent-extraction-gros-plan.jpg', "Gencive bien cicatrisée après une extraction"),
           ('3d-implanto.jpg', "Planification chirurgicale sur radiographie 3D")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Chirurgie orale'), ('tool', 'ACTES', 'Extractions, sagesse'), ('heart', 'ANESTHÉSIE', 'Locale')],
        [('clock', 'DURÉE DE L\'ACTE', '30 à 90 min'), ('cal', 'CICATRISATION', '1 à 2 semaines'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Des interventions précises,<br>préparées et expliquées.",
  intro=["La chirurgie orale regroupe les interventions sur les dents, l'os et les gencives : extraction d'une dent abîmée, retrait des dents de sagesse, préparation de l'os avant un implant. Elle se pratique au cabinet, sous anesthésie locale, avec un plan établi à l'avance.",
         "Au Centre Dentaire Chifaa, chaque intervention de chirurgie orale à Meknès est préparée sur radiographie. On sait avant de commencer où passent les racines et les nerfs, combien de temps prendra l'acte et quelles seront les suites. Vous repartez avec des consignes écrites et un numéro à appeler."],
  who_h="Pour qui, et quand consulter ?",
  who_p="Une intervention n'est proposée que lorsqu'elle est utile. Les situations les plus fréquentes sont les suivantes :",
  who=["Dent de sagesse incluse, mal positionnée, douloureuse ou source d'infections répétées",
       "Dent trop abîmée ou fracturée pour être conservée",
       "Infection ou kyste autour d'une racine",
       "Préparation d'un implant : extraction, greffe osseuse ou sinus lift",
       "Frein de lèvre ou de langue gênant, à la demande de l'orthodontiste"],
  treat_h="Nos interventions",
  treat=[("Extractions simples et complexes", "retrait d'une dent non conservable, en préservant au maximum l'os et la gencive pour la suite."),
         ("Dents de sagesse", "extraction d'une ou plusieurs dents de sagesse, incluses ou non, le plus souvent en une seule séance."),
         ("Chirurgie pré-implantaire", "greffe osseuse et sinus lift pour reconstruire le volume nécessaire à un implant."),
         ("Chirurgie guidée", "l'intervention est planifiée sur la radiographie 3D pour gagner en précision et en confort."),
         ("Chirurgie des tissus mous", "frein de lèvre ou de langue, petites lésions de la bouche.")],
  steps=[("Consultation et radiographie.", "Examen clinique et radiographie panoramique ou 3D pour localiser précisément les racines et les nerfs."),
         ("Explications et devis écrit.", "Déroulement de l'intervention, suites prévisibles et devis détaillé. Rien ne commence sans votre accord."),
         ("Intervention.", "Sous anesthésie locale, au cabinet. La durée varie de 30 à 90 minutes selon l'acte."),
         ("Suites opératoires.", "Consignes écrites, glace, antalgiques et alimentation tiède les premiers jours. Nous restons joignables."),
         ("Contrôle.", "Un rendez-vous de contrôle vérifie la cicatrisation et retire les points si besoin.")],
  price="Le coût d'une intervention de chirurgie orale à Meknès dépend de l'acte, du nombre de dents et de leur position. Nous préférons ne pas afficher de prix qui ne correspondrait pas à votre situation.",
  faq=[("Faut-il toujours enlever les dents de sagesse ?", "Non. Une dent de sagesse bien placée, saine et facile à nettoyer peut être conservée. L'extraction est conseillée quand elle provoque des douleurs, des infections ou qu'elle abîme la dent voisine."),
       ("Est-ce douloureux ?", "L'intervention se fait sous anesthésie locale et n'est pas douloureuse. Les suites, souvent un gonflement et une gêne pendant quelques jours, se gèrent avec des antalgiques et de la glace."),
       ("Combien de jours de repos prévoir ?", "Pour une extraction simple, souvent aucun ou une journée. Pour des dents de sagesse incluses, prévoyez deux à trois jours calmes. Nous vous indiquons la durée adaptée à votre cas."),
       ("Que manger après l'intervention ?", "Des aliments tièdes ou froids et mous les premiers jours : yaourts, purées, soupes tiédies. Évitez les boissons chaudes, l'alcool, le tabac et la paille."),
       ("Un léger saignement est-il normal ?", "Oui, les premières heures. Mordez sur une compresse pendant vingt minutes. Si le saignement persiste ou si la douleur augmente après trois jours, appelez le cabinet.")],
  related=[('implants-dentaires', "remplacer la dent extraite par un implant"),
           ('orthodontie', "extractions prévues dans un plan orthodontique"),
           ('parodontie', "traiter les gencives autour des dents conservées"),
           ('prothese-dentaire', "restaurer la mastication après l'extraction")],
  proc_desc="Chirurgie orale au Centre Dentaire Chifaa, Meknès : extraction des dents de sagesse, extractions complexes, chirurgie pré-implantaire, greffe osseuse, chirurgie guidée, sous anesthésie locale.",
  proc_type="SurgicalProcedure",
 ),

 'parodontie': dict(
  title="Parodontie à Meknès | Gencives, déchaussement – CDC",
  desc="Parodontie à Meknès : gencives qui saignent, déchaussement, dents qui bougent. Bilan, détartrage, surfaçage et suivi. Tél 05 35 51 69 24.",
  h1="Parodontie à Meknès,<br>des gencives saines et solides.",
  hero=('3d-cosmetic.jpg', 900, 900),
  gallery=[('parodontie-detartrage-avant-apres.jpg', "Dents avant et après un détartrage"),
           ('sonde-parodontale.jpg', "Sonde parodontale utilisée pour le bilan des gencives"),
           ('schema-parodonte.jpg', "Schéma d'une dent atteinte de parodontite, avec perte de l'os"),
           ('gencives-saines-parodontie.jpg', "Gencives avant et après le traitement d'une gingivite")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Parodontie'), ('heart', 'SIGNES', 'Saignement, mobilité'), ('tool', 'TRAITEMENTS', 'Détartrage, surfaçage')],
        [('cal', 'SÉANCES', '2 à 4 en général'), ('clock', 'MAINTENANCE', 'Tous les 3 à 6 mois'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Soigner les gencives,<br>c'est garder ses dents.",
  intro=["La parodontie soigne les tissus qui tiennent les dents : la gencive, l'os et les ligaments. Tout commence souvent par une gingivite, une gencive rouge qui saigne au brossage. Non traitée, elle peut évoluer en parodontite : l'os se résorbe, les dents se déchaussent et finissent par bouger.",
         "C'est l'une des premières causes de perte de dents chez l'adulte, alors qu'elle se soigne bien lorsqu'on s'en occupe tôt. Au Centre Dentaire Chifaa, le bilan parodontal à Meknès fait partie de la prise en charge : il précède aussi les implants, les prothèses et l'orthodontie de l'adulte."],
  who_h="Les signes qui doivent alerter",
  who_p="La maladie des gencives est souvent indolore au début. Consultez si vous remarquez l'un de ces signes :",
  who=["Des gencives qui saignent au brossage ou spontanément",
       "Des gencives rouges, gonflées ou sensibles",
       "Une mauvaise haleine qui persiste malgré le brossage",
       "Des dents qui paraissent plus longues, ou des espaces qui apparaissent",
       "Des dents qui bougent, ou une sensibilité au chaud et au froid"],
  treat_h="Nos traitements parodontaux",
  treat=[("Détartrage et polissage", "élimination du tartre et de la plaque au-dessus et juste sous la gencive."),
         ("Surfaçage radiculaire", "nettoyage en profondeur des racines sous anesthésie locale, pour arrêter l'infection et permettre à la gencive de se recoller."),
         ("Chirurgie parodontale", "dans les formes avancées, accès direct aux racines ou greffe de gencive pour couvrir une racine exposée."),
         ("Maintenance parodontale", "des visites régulières pour garder les résultats dans le temps.")],
  steps=[("Bilan parodontal.", "Mesure de la profondeur des poches autour de chaque dent, radiographies et évaluation des facteurs de risque."),
         ("Plan de traitement et devis écrit.", "Nombre de séances, soins prévus et devis détaillé. Rien ne commence sans votre accord."),
         ("Hygiène sur mesure.", "Technique de brossage, brossettes et fil adaptés à votre bouche : la base du résultat."),
         ("Traitement.", "Détartrage et surfaçage, en général en deux à quatre séances sous anesthésie locale si nécessaire."),
         ("Réévaluation et maintenance.", "Contrôle de la guérison après quelques semaines, puis visites de maintenance tous les 3 à 6 mois.")],
  price="Le coût d'un traitement parodontal à Meknès dépend du nombre de séances et de l'étendue de la maladie. Nous préférons ne pas afficher de prix qui ne correspondrait pas à votre situation.",
  faq=[("Mes gencives saignent au brossage, est-ce grave ?", "C'est le premier signe d'une inflammation. Ce n'est pas une urgence, mais cela mérite un contrôle : une gingivite prise tôt se soigne entièrement."),
       ("Le déchaussement est-il réversible ?", "Le traitement arrête la maladie et stabilise les dents. L'os perdu ne repousse pas de lui-même, mais certaines techniques permettent de régénérer une partie des tissus."),
       ("Le surfaçage fait-il mal ?", "Il se fait sous anesthésie locale. Une sensibilité au froid peut apparaître quelques jours après, elle disparaît progressivement."),
       ("Y a-t-il un lien avec le diabète ou la grossesse ?", "Oui. Le diabète favorise la maladie des gencives, et la traiter aide à équilibrer la glycémie. Pendant la grossesse, les gencives saignent plus facilement : un contrôle est conseillé."),
       ("À quelle fréquence faire un détartrage ?", "Au moins une fois par an pour la plupart des patients, tous les 3 à 6 mois après un traitement parodontal.")],
  related=[('implants-dentaires', "des gencives saines avant et autour des implants"),
           ('orthodontie', "aligner les dents une fois les gencives stabilisées"),
           ('prothese-dentaire', "restaurer les dents une fois la gencive soignée"),
           ('chirurgie-orale', "greffe de gencive et chirurgie des tissus")],
  proc_desc="Traitements parodontaux au Centre Dentaire Chifaa, Meknès : bilan parodontal, détartrage, surfaçage radiculaire, chirurgie parodontale et maintenance.",
  proc_type="TherapeuticProcedure",
 ),

 'prothese-dentaire': dict(
  title="Prothèse dentaire à Meknès | Couronnes, bridges – CDC",
  desc="Prothèse dentaire à Meknès : couronnes céramique et zircone, facettes, bridges et prothèses amovibles, par empreinte numérique. Devis écrit.",
  h1="Prothèse dentaire à Meknès,<br>couronnes, facettes et bridges.",
  hero=('facette-ceramique-pose-meknes.jpg', 960, 960),
  gallery=[('facettes-ceramiques-resultat-meknes.jpg', "Facettes céramiques posées, résultat final"),
           ('couronne-zircone.jpg', "Couronne en zircone sur son modèle"),
           ('bridge-ceramique.jpg', "Bridge céramique de trois dents"),
           ('prothese-sur-implants.jpg', "Prothèse complète fixée sur implants")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Prothèse dentaire'), ('tool', 'SOLUTIONS', 'Fixe ou amovible'), ('sparkle', 'MATÉRIAUX', 'Céramique, zircone')],
        [('scan', 'EMPREINTE', 'Numérique'), ('cal', 'RENDEZ-VOUS', '2 à 4 en général'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Restaurer une dent,<br>jusque dans les détails.",
  intro=["La prothèse dentaire restaure les dents abîmées et remplace celles qui manquent. Une couronne protège une dent fragilisée, une facette corrige la forme et la teinte d'une dent visible, un bridge ou une prothèse amovible comble un espace. Le but est double : manger normalement et retrouver un sourire naturel.",
         "Au Centre Dentaire Chifaa, les prothèses dentaires à Meknès sont conçues à partir d'une empreinte numérique, puis réalisées sur mesure avec le laboratoire. La teinte, la forme et l'occlusion sont validées avec vous avant la pose définitive."],
  who_h="Pour qui, et dans quels cas ?",
  who_p="Une prothèse est proposée quand une dent ne peut plus être restaurée par un simple soin, ou quand une ou plusieurs dents manquent :",
  who=["Dent très abîmée, dévitalisée ou fracturée",
       "Dent visible de forme, de teinte ou de taille disgracieuse",
       "Une ou plusieurs dents manquantes à remplacer",
       "Ancienne prothèse usée, mal ajustée ou inesthétique",
       "Dentier qui gêne et que l'on souhaite stabiliser"],
  treat_h="Nos solutions prothétiques",
  treat=[("Couronnes céramique et zircone", "une coiffe sur mesure qui protège la dent et reproduit son aspect naturel."),
         ("Facettes céramiques", "de fines pellicules collées sur les dents de devant pour corriger la forme, la teinte ou de petits espaces."),
         ("Inlays et onlays", "des restaurations partielles en céramique, plus conservatrices qu'une couronne."),
         ("Bridges", "des dents fixes appuyées sur les dents voisines ou sur des implants pour combler un espace."),
         ("Prothèses amovibles", "partielles ou complètes, et stabilisées sur implants pour ne plus bouger.")],
  steps=[("Consultation et photos.", "Examen, radiographies et photos du sourire pour définir la solution adaptée."),
         ("Plan de traitement et devis écrit.", "Type de prothèse, matériau, nombre de séances et devis détaillé. Rien ne commence sans votre accord."),
         ("Préparation et empreinte numérique.", "La dent est préparée, puis un scanner intra-oral enregistre sa forme. Une prothèse provisoire vous est posée si besoin."),
         ("Essayage.", "Teinte, forme et occlusion sont vérifiées avec vous avant la finition au laboratoire."),
         ("Pose définitive et suivi.", "Scellement ou collage, réglage de l'occlusion et conseils d'entretien, puis contrôle régulier.")],
  price="Le coût d'une prothèse dentaire à Meknès dépend du type de restauration, du matériau et du nombre de dents concernées. Nous préférons ne pas afficher de prix qui ne correspondrait pas à votre situation.",
  faq=[("Couronne ou facette : quelle différence ?", "La couronne recouvre toute la dent et la protège quand elle est très abîmée. La facette ne couvre que la face visible et sert surtout à corriger l'esthétique d'une dent saine."),
       ("Combien de temps dure une couronne ?", "Bien entretenue, une couronne en céramique ou en zircone dure de nombreuses années. Sa longévité dépend de l'hygiène, du grincement éventuel des dents et des contrôles réguliers."),
       ("Les facettes abîment-elles les dents ?", "La préparation est minime et se limite à la surface de l'émail. Dans certains cas, elle n'est même pas nécessaire. Nous vous indiquons ce qui est possible pour vos dents."),
       ("Prothèse amovible ou implants ?", "La prothèse amovible est plus simple et moins coûteuse. Les implants offrent une tenue fixe et un meilleur confort. Les deux peuvent se combiner : un dentier stabilisé sur implants."),
       ("La prothèse aura-t-elle l'air naturelle ?", "Oui. La teinte est choisie avec vous et la céramique reproduit la transparence de l'émail. Un essayage est prévu avant la pose définitive.")],
  related=[('implants-dentaires', "une racine fixe pour porter couronnes et bridges"),
           ('orthodontie', "aligner les dents avant de poser des facettes"),
           ('parodontie', "des gencives saines autour de la prothèse"),
           ('chirurgie-orale', "extraire une dent non conservable avant la prothèse")],
  proc_desc="Prothèses dentaires au Centre Dentaire Chifaa, Meknès : couronnes céramique et zircone, facettes, inlays, onlays, bridges, prothèses amovibles et prothèses sur implants, empreinte numérique.",
  proc_type="TherapeuticProcedure",
 ),

 'pedodontie': dict(
  title="Dentiste enfant à Meknès | Pédodontie – CDC",
  desc="Dentiste pour enfants à Meknès : première visite, prévention des caries, vernis fluoré et soins des dents de lait, dans le calme. Tél 05 35 51 69 24.",
  h1="Pédodontie à Meknès,<br>des soins doux pour les enfants.",
  hero=('examen-dentaire-enfant.jpg', 1400, 933),
  gallery=[('dents-de-lait-enfant.jpg', "Sourire d'enfant avec des dents de lait qui tombent"),
           ('radio-dentition-mixte-enfant.jpg', "Radiographie d'une dentition mixte d'enfant"),
           ('faq-clip.jpg', "Soin d'une carie sur une molaire")],
  meta=[[('shield', 'SPÉCIALITÉ', 'Pédodontie'), ('users', 'ÂGE', 'Dès les premières dents'), ('heart', 'APPROCHE', 'Douce, à son rythme')],
        [('cal', 'PREMIÈRE VISITE', 'Vers 1 an'), ('clock', 'CONTRÔLES', 'Tous les 6 mois'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]],
  h2="Une première expérience du dentiste<br>qui donne confiance.",
  intro=["La pédodontie est la dentisterie de l'enfant, des premières dents jusqu'à l'adolescence. Elle soigne, mais surtout elle prévient : les bonnes habitudes prises tôt protègent les dents de lait comme les dents définitives, et évitent des soins plus lourds plus tard.",
         "Au Centre Dentaire Chifaa, chaque enfant est accueilli à son rythme. On explique avec des mots simples, on montre les instruments et on avance sans forcer. Les parents restent présents. L'objectif du dentiste pour enfant à Meknès est simple : que votre enfant revienne sans appréhension."],
  who_h="Quand consulter ?",
  who_p="Une première visite est conseillée vers l'âge d'un an, puis un contrôle tous les six mois. Consultez aussi dès que vous remarquez :",
  who=["Une tache blanche, marron ou noire sur une dent",
       "Une douleur, une sensibilité au sucré ou au froid",
       "Une dent cassée ou déplacée après une chute",
       "Des dents définitives qui poussent derrière les dents de lait",
       "Une succion du pouce ou de la tétine qui se prolonge"],
  treat_h="Nos soins pour les enfants",
  treat=[("Prévention", "conseils de brossage et d'alimentation, vernis fluoré et scellement des sillons des molaires pour les protéger des caries."),
         ("Soins des dents de lait", "traitement des caries pour éviter la douleur, l'infection et préserver la place des dents définitives."),
         ("Traumatismes dentaires", "prise en charge rapide d'une dent cassée, déplacée ou expulsée après une chute."),
         ("Dépistage orthodontique", "surveillance de la croissance des mâchoires et orientation précoce vers un traitement si nécessaire.")],
  steps=[("Accueil et découverte.", "Votre enfant découvre le cabinet, le fauteuil et les instruments, sans soin lors de la première approche si besoin."),
         ("Examen et conseils.", "Contrôle des dents et des gencives, radiographie si nécessaire, conseils adaptés à l'âge pour les parents."),
         ("Prévention.", "Vernis fluoré et scellement des sillons selon le risque de carie de l'enfant."),
         ("Soins si nécessaire.", "Les soins sont expliqués à l'enfant et réalisés en douceur, en plusieurs séances courtes si besoin."),
         ("Suivi.", "Un contrôle tous les six mois pour suivre la croissance et intervenir tôt.")],
  price="Le coût des soins pour enfants dépend des actes réalisés. Nous préférons ne pas afficher de prix qui ne correspondrait pas à la situation de votre enfant.",
  faq=[("Faut-il soigner les dents de lait ?", "Oui. Une carie sur une dent de lait peut faire mal, s'infecter et abîmer la dent définitive qui se forme dessous. Les dents de lait gardent aussi la place des dents définitives."),
       ("À quel âge faire la première visite ?", "Vers un an, ou à l'apparition des premières dents. Une visite précoce permet de donner les bons conseils et d'habituer l'enfant au cabinet."),
       ("Mon enfant a peur du dentiste, que faire ?", "Parlez-en simplement, sans mots qui inquiètent. Au cabinet, nous prenons le temps d'expliquer et de montrer. Si besoin, la première visite sert seulement à faire connaissance."),
       ("Que faire si une dent est cassée après une chute ?", "Gardez le morceau de dent et appelez le cabinet rapidement. Si une dent définitive est tombée entière, tenez-la par la couronne, conservez-la dans du lait et consultez sans attendre."),
       ("La tétine ou le pouce abîment-ils les dents ?", "Une succion prolongée au-delà de 3 à 4 ans peut déformer les dents et le palais. Nous vous conseillons pour aider l'enfant à arrêter en douceur.")],
  related=[('orthodontie', "dépistage et traitement précoce des mâchoires"),
           ('chirurgie-orale', "extraction d'une dent de lait qui ne tombe pas"),
           ('parodontie', "de bonnes habitudes pour des gencives saines")],
  proc_desc="Soins dentaires pour enfants au Centre Dentaire Chifaa, Meknès : première visite, prévention des caries, vernis fluoré, scellement des sillons, soins des dents de lait, traumatismes.",
  proc_type="TherapeuticProcedure",
 ),
}

# --------------------------------------------------------------------------------------------
# Header / footer depuis index.html
# --------------------------------------------------------------------------------------------
def load_chrome():
    src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    def cut(a, b):
        i = src.index(a); j = src.index(b, i); return src[i:j]
    header = cut('<header class="nav"', '<main').rstrip()
    footer = cut('<footer class="foot"', '<div class="fabs">').rstrip()
    fabs = cut('<div class="fabs">', '<script src="vendor/gsap').rstrip()
    return header, footer, fabs

def absolutize(chunk):
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|data:|/)', url):
            return m.group(0)
        if url == 'index.html' or url == '#accueil':
            url = '/'
        elif url.startswith('index.html#'):
            url = '/' + url[len('index.html'):]
        elif url.startswith('#'):
            url = '/' + url
        else:
            url = '/' + url
        return '%s="%s"' % (attr, url)
    return re.sub(r'\b(href|src)="([^"]*)"', fix, chunk)

def mark_current(header, footer, path):
    # onglet actif du menu et du footer (un article active l'onglet Articles)
    if path.startswith('/blog/'):
        path = '/blog/'
    header = header.replace('href="%s"' % path, 'href="%s" aria-current="page"' % path)
    footer = footer.replace('href="%s"' % path, 'href="%s" aria-current="page"' % path)
    return header, footer

def head(title, desc, path, og_img, jsonld, noindex=False, preload=None):
    url = SITE + path
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ''
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(t)s</title>
<meta name="description" content="%(d)s">
%(robots)s<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website">
<meta property="og:title" content="%(t)s">
<meta property="og:description" content="%(d)s">
<meta property="og:image" content="%(site)s/assets/img/%(img)s">
<meta property="og:url" content="%(url)s">
<meta property="og:locale" content="fr_MA">
<meta property="og:site_name" content="Centre Dentaire Chifaa">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png">
<link rel="icon" type="image/x-icon" sizes="48x48" href="/favicon.ico">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png?v=2">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
<link rel="preload" href="/assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/geist-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">
%(ld)s
</script>
%(pre)s<link rel="stylesheet" href="/dark.css?v=%(v)s">
</head>
<body>

''' % dict(t=H.escape(title), d=H.escape(desc), url=url, site=SITE, img=og_img, robots=robots,
           ld=json.dumps(jsonld, ensure_ascii=False, indent=1), v=VER,
           pre=('<link rel="preload" as="image" href="/assets/img/%s" fetchpriority="high">\n' % preload) if preload else '')

SCRIPTS = '''

<script src="/vendor/gsap.min.js"></script>
<script src="/vendor/ScrollTrigger.min.js"></script>
<script src="/vendor/lenis.min.js"></script>
<script src="/dark.js?v=%s"></script>

</body>
</html>
''' % VER

DENTIST = {"@type": "Dentist", "@id": SITE + "/#cabinet", "name": "Centre Dentaire Chifaa", "telephone": "+212535516924", "email": EMAIL,
           "address": {"@type": "PostalAddress", "streetAddress": "Bureau N1, Imm Bureaux El Menzah N5, Av des FAR",
                       "addressLocality": "Meknès", "postalCode": "50000", "addressCountry": "MA"},
           "geo": {"@type": "GeoCoordinates", "latitude": 33.8947626, "longitude": -5.5497537},
           "url": SITE + "/", "hasMap": MAPS, "logo": SITE + "/assets/logo-cdc-light.png",
           "image": SITE + "/assets/img/og-centre-dentaire-chifaa.jpg", "medicalSpecialty": "https://schema.org/Dentistry",
           "openingHoursSpecification": [
               {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "17:30"},
               {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:30"}],
           "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "43"}}

# --------------------------------------------------------------------------------------------
# Schéma : graphe JSON-LD commun à toutes les pages (identifiants stables, liés par @id)
# --------------------------------------------------------------------------------------------
ID_SITE, ID_ORG, ID_DR = SITE + '/#website', SITE + '/#cabinet', SITE + '/#dr-boukadous'
INSTAGRAM = 'https://www.instagram.com/centredentairechifaa.ma/'

WEBSITE = {"@type": "WebSite", "@id": ID_SITE, "url": SITE + "/", "name": "Centre Dentaire Chifaa",
           "alternateName": "CDC Meknès", "inLanguage": "fr", "publisher": {"@id": ID_ORG}}

PERSON = {"@type": "Person", "@id": ID_DR, "name": "Dr Taoufik Boukadous", "givenName": "Taoufik", "familyName": "Boukadous",
          "honorificPrefix": "Dr", "jobTitle": "Chirurgien-dentiste", "url": SITE + "/le-cabinet/",
          "worksFor": {"@id": ID_ORG},
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Université Internationale de Rabat (UIR)"},
          "hasCredential": [
              {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Diplôme de Docteur en Médecine Dentaire"},
              {"@type": "EducationalOccupationalCredential", "credentialCategory": "certificate", "name": "Diplôme Universitaire d'Implantologie et de Chirurgie Orale"}],
          "knowsAbout": ["Implantologie", "Chirurgie orale", "Chirurgie implantaire guidée", "Esthétique du sourire", "Endodontie", "Restaurations en composite"],
          "knowsLanguage": ["fr", "ar"]}


def org_full():
    d = dict(DENTIST)
    d.update({
        "alternateName": "CDC Meknès",
        "description": "Centre dentaire pluridisciplinaire à Meknès : orthodontie, implants dentaires, chirurgie orale, parodontie, prothèse dentaire et pédodontie.",
        "logo": {"@type": "ImageObject", "@id": SITE + "/#logo", "url": SITE + "/assets/logo-cdc.png", "width": 1156, "height": 479, "caption": "Centre Dentaire Chifaa"},
        "image": [SITE + "/assets/img/og-centre-dentaire-chifaa.jpg", SITE + "/assets/img/reception-cabinet-cdc-meknes.jpg",
                  SITE + "/assets/img/cabinet-salle-de-soins-meknes.jpg"],
        "priceRange": "$$", "currenciesAccepted": "MAD", "isAcceptingNewPatients": True,
        "knowsLanguage": ["fr", "ar"],
        "areaServed": {"@type": "City", "name": "Meknès"},
        "founder": {"@id": ID_DR}, "employee": [{"@id": ID_DR}],
        "sameAs": [INSTAGRAM, BOOK, MAPS],
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+212535516924",
                         "email": EMAIL, "availableLanguage": ["fr", "ar"], "areaServed": "MA"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Soins dentaires", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "MedicalProcedure", "@id": SITE + "/soins/%s-meknes/#procedure" % s,
                                               "name": SOIN_NAME[s], "url": SITE + "/soins/%s-meknes/" % s}} for s in SOINS_ORDER]},
    })
    return d


PAGE_TYPES = ('WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'MedicalWebPage', 'ProfilePage')


def _refs(node):
    """Remplace les copies complètes du cabinet par une référence @id."""
    if isinstance(node, dict):
        if node.get('@id') == ID_ORG and len(node) > 2:
            return {"@id": ID_ORG}
        return {k: _refs(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_refs(x) for x in node]
    return node


def build_graph(ld, path, title, desc, img):
    url = SITE + path
    nodes = ld.get('@graph', [ld]) if isinstance(ld, dict) else list(ld)
    nodes = [dict(n) for n in nodes if n.get('@type') not in ('WebSite',) and n.get('@id') not in (ID_ORG, ID_DR)]
    nodes = [_refs(n) if n.get('@type') != 'Dentist' else n for n in nodes]
    nodes = [n for n in nodes if not (n.get('@type') == 'Dentist')]
    crumb = next((n for n in nodes if n.get('@type') == 'BreadcrumbList'), None)
    if crumb:
        crumb['@id'] = url + '#breadcrumb'
    page = next((n for n in nodes if n.get('@type') in PAGE_TYPES), None)
    proc = next((n for n in nodes if n.get('@type') == 'MedicalProcedure'), None)
    post = next((n for n in nodes if n.get('@type') == 'BlogPosting'), None)
    if page is None:
        page = {"@type": "MedicalWebPage" if proc else "WebPage"}
        nodes.insert(0, page)
    page.update({"@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "fr",
                 "isPartOf": {"@id": ID_SITE},
                 "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/" + img}})
    page.setdefault("about", {"@id": ID_ORG})
    if crumb:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if proc:
        proc.pop("provider", None)
        page["mainEntity"] = {"@id": proc["@id"]}
        page["about"] = {"@id": proc["@id"]}
        page["audience"] = {"@type": "MedicalAudience", "audienceType": "Patient"}
        page["reviewedBy"] = {"@id": ID_DR}
    if post:
        post["mainEntityOfPage"] = {"@id": url + "#webpage"}
        post["publisher"] = {"@id": ID_ORG}
        post["author"] = {"@id": ID_ORG}
        post["isPartOf"] = {"@type": "Blog", "@id": SITE + "/blog/#blog", "name": "Blog du Centre Dentaire Chifaa", "url": SITE + "/blog/"}
        if isinstance(post.get("image"), str):
            post["image"] = {"@type": "ImageObject", "url": post["image"]}
        art = next((a for a in ARTICLES_REF if path.endswith('/%s/' % a['slug'])), None)
        if art and art.get('soin'):
            post["about"] = {"@id": SITE + "/soins/%s-meknes/#procedure" % art['soin'], "name": SOIN_NAME[art['soin']]}
        page["mainEntity"] = {"@id": post["@id"]}
    if path == '/le-cabinet/':
        page["mainEntity"] = {"@id": ID_ORG}
        page["mentions"] = {"@id": ID_DR}
    return {"@context": "https://schema.org", "@graph": [WEBSITE, org_full(), PERSON] + nodes}


ARTICLES_REF = []

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

# --------------------------------------------------------------------------------------------
# Blocs communs
# --------------------------------------------------------------------------------------------
def stat(label, value, href=None):
    v = ('<a class="tp-stat-v" href="%s" target="_blank" rel="noopener">%s</a>' % (href, value)) if href \
        else '<span class="tp-stat-v">%s</span>' % value
    return ('<div class="tp-stat"><span class="tp-stat-line" aria-hidden="true"><i></i></span>'
            '<span class="mono tp-stat-l">%s</span>%s</div>' % (label, v))

STATS_TRUST = [stat('NOTE GOOGLE', '5,0 / 5', MAPS), stat('AVIS PATIENTS', '43'), stat('DEVIS AVANT SOIN', 'Écrit')]

def hero(img, w, h, pills, h1, stats):
    pl = ''.join(('<a class="tp-pill" href="%s">%s</a>' % (p, n)) if p else
                 '<span class="tp-pill is-cur" aria-current="page">%s</span>' % n for n, p in pills)
    return '''
  <section class="tp-hero">
    <img class="tp-hero-fill" src="/assets/img/%s" alt="" aria-hidden="true">
    <img class="tp-hero-bg" src="/assets/img/%s" alt="" width="%d" height="%d" fetchpriority="high" decoding="async">
    <div class="tp-hero-copy">
      <nav class="tp-pills" aria-label="Fil d'Ariane">%s</nav>
      <h1 data-lines>%s</h1>
    </div>
    <div class="tp-stats" data-fade>
      %s
    </div>
  </section>
''' % (img.replace('.jpg', '.webp'), img.replace('.jpg', '.webp'), w, h, pl, h1, '\n      '.join(stats))

def gallery(items, group):
    figs = ''.join('    <figure data-fade><a class="tp-lb-link" href="/assets/img/%s" data-lightbox="%s" aria-label="Agrandir la photo" '
                   'aria-haspopup="dialog"><img src="/assets/img/%s" alt="%s" loading="lazy">%s</a></figure>\n'
                   % (f, group, f, H.escape(a), LB_IC) for f, a in items)
    return '''
  <section class="tp-gallery" aria-label="En images" style="--cols:%d">
%s  </section>
''' % (min(len(items), 4), figs)

def meta_aside(groups):
    out = []
    for g in groups:
        rows = ''.join('<div><dt class="mono">%s%s</dt><dd>%s</dd></div>' % (ic(ICONS[i]), l, v) for i, l, v in g)
        out.append('<dl>%s</dl>' % rows)
    return '<aside class="tp-meta" data-fade>\n      %s\n    </aside>' % '\n      '.join(out)

def cta_arc():
    return '''
  <section class="tp-cta" id="rendez-vous">
    <div class="tp-cta-top">
      <div class="tp-cta-copy">
        <h2>Des soins dentaires<br>de qualité, à Meknès</h2>
        <a class="tp-cta-link" href="%(book)s" target="_blank" rel="noopener">Prendre rendez-vous<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6l-6 6"/></svg></a>
      </div>
      <div class="tp-cta-faces" aria-hidden="true">
        <img src="/assets/img/cabinet-salle-de-soins-meknes.jpg" alt="" loading="lazy">
        <img src="/assets/img/accueil-cabinet-cdc-meknes.jpg" alt="" loading="lazy">
        <img src="/assets/img/cabinet-radiologie-3d-meknes.jpg" alt="" loading="lazy">
      </div>
      <ul class="tp-cta-list">
        <li><span class="tp-cta-chk" aria-hidden="true"></span>Des soins confortables, sans douleur</li>
        <li><span class="tp-cta-chk" aria-hidden="true"></span>Chaque cas planifié en numérique</li>
        <li><span class="tp-cta-chk" aria-hidden="true"></span>Spécialistes sur place, sans orientation extérieure</li>
      </ul>
    </div>
    <div class="tp-arc" aria-hidden="true">
      <svg class="tp-arc-svg" viewBox="0 95 1600 317" preserveAspectRatio="xMidYMid meet" data-arc>
        <defs><path id="tp-arc-path" d="M -60 440 Q 800 -70 1660 440" fill="none"/></defs>
        <text class="tp-arc-text" text-anchor="middle"><textPath href="#tp-arc-path" startOffset="50%%">Prendre rendez-vous<tspan class="tp-arc-sep">  –  </tspan>Prendre rendez-vous</textPath></text>
      </svg>
    </div>
  </section>
''' % dict(book=BOOK)

def clink(icon, text, href, ext=False):
    t = ' rel="noopener" target="_blank"' if ext else ''
    return ('<a class="tp-clink" href="%s"%s><span class="tp-clink-ic" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg></span>'
            '<span class="tp-clink-t">%s</span><span class="tp-clink-bg" aria-hidden="true"></span></a>' % (href, t, ICONS[icon] if icon in ICONS else icon, text))

WA_IC = '<path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9"/><path d="M9 10a.5 .5 0 0 0 1 0v-1a.5 .5 0 0 0 -1 0v1a5 5 0 0 0 5 5h1a.5 .5 0 0 0 0 -1h-1a.5 .5 0 0 0 0 1"/>'

SHOW_FORM = False   # formulaire de demande de rendez-vous masqué pour l'instant (True pour le réafficher)

def booking(checked=None, title='Planifiez votre visite'):
    tabs = ''.join('<label class="tp-tab"><input type="radio" name="traitement" value="%s"%s><span>%s</span></label>'
                   % (SOIN_NAME[s], ' checked' if s == checked else '', SOIN_NAME[s]) for s in SOINS_ORDER)
    html = '''
  <section class="tp-book" id="rendez-vous">
    <div class="tp-book-copy">
      <h2 data-lines>%(title)s</h2>
      <div class="tp-book-links" data-fade>
        <div class="tp-book-row">%(l1)s%(l3)s</div>
        %(l5)s
        <a class="btn btn-navy btn-big tp-book-cta" href="%(book)s" target="_blank" rel="noopener">Prendre rendez-vous%(orb)s</a>%(l2)s
      </div>
      <p class="tp-book-hours" data-fade><span>Lundi au vendredi de 8h30 à 17h30,</span> <span>samedi de 9h00 à 14h30.</span></p>
    </div>

    <div class="tp-form-card" data-fade>
      <form class="tp-form" id="tp-form" novalidate>
        <div class="tp-field"><label class="tp-flabel" for="f-nom">Nom</label><input class="tp-input" id="f-nom" type="text" name="nom" autocomplete="name" required minlength="2"></div>
        <div class="tp-field"><label class="tp-flabel" for="f-tel">Téléphone</label><input class="tp-input" id="f-tel" type="tel" name="tel" autocomplete="tel" inputmode="tel" required></div>
        <div class="tp-field"><label class="tp-flabel" for="f-email">E-mail</label><input class="tp-input" id="f-email" type="email" name="email" autocomplete="email"></div>
        <div class="tp-field"><label class="tp-flabel" for="f-msg">Motif de la visite</label><textarea class="tp-input tp-textarea" id="f-msg" name="motif" rows="3"></textarea></div>

        <fieldset class="tp-fs">
          <legend class="tp-legend">Type de traitement</legend>
          <div class="tp-tabs">%(tabs)s</div>
        </fieldset>

        <fieldset class="tp-fs">
          <legend class="tp-legend">Quand souhaitez-vous venir ?</legend>
          <div class="tp-radios">
            <label class="tp-radio"><input type="radio" name="quand" value="Dès que possible" checked><span class="tp-radio-dot" aria-hidden="true"></span><span>Dès que possible</span></label>
            <label class="tp-radio"><input type="radio" name="quand" value="Dans la semaine"><span class="tp-radio-dot" aria-hidden="true"></span><span>Dans la semaine</span></label>
            <label class="tp-radio"><input type="radio" name="quand" value="Dans 2 à 3 semaines"><span class="tp-radio-dot" aria-hidden="true"></span><span>Dans 2 à 3 semaines</span></label>
            <label class="tp-radio"><input type="radio" name="quand" value="Je me renseigne"><span class="tp-radio-dot" aria-hidden="true"></span><span>Je me renseigne simplement</span></label>
          </div>
        </fieldset>

        <details class="tp-dd">
          <summary class="tp-dd-t"><span>Quelle est votre priorité ?</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6l6 -6"/></svg></summary>
          <div class="tp-dd-list">
            <label class="tp-check-l"><input type="checkbox" name="priorite" value="Soulager une douleur"><span class="tp-check-box" aria-hidden="true"></span><span>Soulager une douleur</span></label>
            <label class="tp-check-l"><input type="checkbox" name="priorite" value="Un résultat discret"><span class="tp-check-box" aria-hidden="true"></span><span>Un résultat discret</span></label>
            <label class="tp-check-l"><input type="checkbox" name="priorite" value="Un traitement rapide"><span class="tp-check-box" aria-hidden="true"></span><span>Un traitement rapide</span></label>
            <label class="tp-check-l"><input type="checkbox" name="priorite" value="Un devis clair"><span class="tp-check-box" aria-hidden="true"></span><span>Un devis clair</span></label>
          </div>
        </details>

        <p class="tp-form-err" id="tp-form-err" role="alert" hidden>Indiquez votre nom et un numéro de téléphone valide.</p>
        <div class="tp-form-row">
          <button class="tp-submit" type="submit">Envoyer la demande%(orb)s</button>
          <span class="tp-form-note">Réponse via WhatsApp, aux heures d'ouverture.</span>
        </div>
      </form>
    </div>
  </section>
''' % dict(title=title, tabs=tabs, orb=ORB, book=BOOK, l5=clink('mail', EMAIL, 'mailto:' + EMAIL),
           l1=clink('phone', '05 35 51 69 24', 'tel:+212535516924'),
           l2='',
           l3=clink(WA_IC, 'WhatsApp', WA, True),
           l4=clink('pin', 'Av des FAR, Meknès', MAPS, True))
    if not SHOW_FORM:
        i = html.index('    <div class="tp-form-card"'); j = html.index('  </section>', i)
        html = html[:i].rstrip() + '\n' + html[j:]
        html = html.replace('<section class="tp-book" id="rendez-vous">', '<section class="tp-book tp-book-solo" id="rendez-vous">')
    return html

def lieu(img='reception-cabinet-cdc-meknes.jpg', alt="Accueil du Centre Dentaire Chifaa à Meknès : comptoir de réception et logo CDC"):
    return '''
  <section class="lieu" aria-label="Le cabinet à Meknès">
    <img class="lieu-bg" src="/assets/img/%s" alt="%s" loading="lazy" data-lieu-parallax>
    <a class="lieu-card" href="%s" target="_blank" rel="noopener" data-fade>
      <span class="lieu-title">
        <span class="lieu-h">Meknès, Maroc</span>
        <span class="lieu-arrow" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 7l-10 10"/><path d="M8 7h9v9"/></svg></span>
      </span>
      <span class="lieu-space" aria-hidden="true"></span>
      <span class="lieu-address"><span>Bureau N1, Imm Bureaux El Menzah N5</span><span>Av des FAR, Meknès 50000</span></span>
      <span class="lieu-hours"><span>Lun – Ven : 8h30 – 17h30</span><span>Sam : 9h00 – 14h30</span></span>
    </a>
  </section>
''' % (img, H.escape(alt), MAPS)

# --------------------------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------------------------
def soin_page(slug):
    d = SOINS[slug]; name = SOIN_NAME[slug]; path = '/soins/%s-meknes/' % slug
    who = ''.join('<li>%s</li>' % x for x in d['who'])
    treat = ''.join('<li><b>%s</b> : %s</li>' % t for t in d['treat'])
    steps = ''.join('<li data-fade><span><b>%s</b> %s</span></li>' % s for s in d['steps'])
    faq = ''.join('<details data-fade><summary>%s</summary><p>%s</p></details>' % f for f in d['faq'])
    rel = ''.join('<li><a href="/soins/%s-meknes/"><b>%s</b><span>%s</span></a></li>' % (s, SOIN_NAME[s], t) for s, t in d['related'])
    intro = ''.join('<p data-fade>%s</p>' % p for p in d['intro'])
    body = '\n<main id="top">\n' + hero(d['hero'][0], d['hero'][1], d['hero'][2], [('Nos soins', '/soins/'), (name, None)], d['h1'], STATS_TRUST) \
        + gallery(d['gallery'], slug) + '''
  <section class="tp-panel">
    %(meta)s

    <div class="tp-rich">
      <h2 data-lines>%(h2)s</h2>
      %(intro)s

      <h3 data-fade>%(who_h)s</h3>
      <p data-fade>%(who_p)s</p>
      <ul class="tp-check" data-fade>%(who)s</ul>

      <h3 data-fade>%(treat_h)s</h3>
      <ul class="tp-check" data-fade>%(treat)s</ul>

      <h3 data-fade>Le déroulement au cabinet</h3>
      <ol class="tp-steps">%(steps)s</ol>

      <h3 data-fade>Tarifs et devis</h3>
      <p data-fade>%(price)s Ce que nous garantissons : un <b>devis écrit et détaillé</b>, remis après la consultation et avant tout engagement. Demandez-nous les documents nécessaires pour votre mutuelle ou votre assurance.</p>

      <h3 data-fade>Questions fréquentes</h3>
      <div class="tp-faq">%(faq)s</div>

      <h3 data-fade>Soins associés</h3>
      <ul class="tp-links" data-fade>%(rel)s</ul>
    </div>
  </section>
''' % dict(meta=meta_aside(d['meta']), h2=d['h2'], intro=intro, who_h=d['who_h'], who_p=d['who_p'], who=who,
           treat_h=d['treat_h'], treat=treat, steps=steps, price=d['price'], faq=faq, rel=rel) \
        + cta_arc() + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalProcedure", "@id": SITE + path + "#procedure", "name": "%s à Meknès" % name,
         "description": d['proc_desc'], "procedureType": "https://schema.org/" + d['proc_type'],
         "provider": DENTIST, "url": SITE + path},
        crumbs([('Accueil', '/'), ('Nos soins', '/soins/'), ('%s à Meknès' % name, path)])]}
    return path, d['title'], d['desc'], d['hero'][0], ld, body

def cabinet_page():
    path = '/le-cabinet/'
    gal = [('cabinet-radiologie-3d-meknes.jpg', "Appareil de radiologie 3D du Centre Dentaire Chifaa"),
           ('cabinet-salle-de-soins-meknes.jpg', "Salle de soins et unit dentaire du cabinet"),
           ('cabinet-sterilisation-meknes.jpg', "Autoclave de stérilisation des instruments"),
           ('cabinet-diplomes-dr-boukadous.jpg', "Diplômes et attestations de formation du Dr Boukadous")]
    specs = ''.join('<li><a href="/soins/%s-meknes/"><b>%s</b><span>%s</span></a></li>' % (s, SOIN_NAME[s], t) for s, t in [
        ('orthodontie', "aligneurs et bagues, adultes et enfants"), ('implants-dentaires', "implant unitaire, bridge, All-on-4"),
        ('chirurgie-orale', "dents de sagesse et extractions"), ('parodontie', "gencives et déchaussement"),
        ('prothese-dentaire', "couronnes, facettes et bridges"), ('pedodontie', "des soins doux pour les enfants")])
    body = '\n<main id="top">\n' + hero('reception-cabinet-cdc-meknes.jpg', 1920, 2640, [('Le centre', '/'), ('Le cabinet', None)],
                                         "Un centre dentaire pluridisciplinaire,<br>au cœur de Meknès.", STATS_TRUST) \
        + gallery(gal, 'cabinet') + '''
  <section class="tp-panel">
    %(meta)s

    <div class="tp-rich">
      <h2 data-lines>Toutes les spécialités,<br>dans les mêmes murs.</h2>
      <p data-fade>Le Centre Dentaire Chifaa accueille ses patients avenue des FAR, au centre de Meknès. Sous la responsabilité du Dr Taoufik Boukadous, le cabinet réunit l'orthodontie, l'implantologie, la chirurgie orale, la parodontie, la prothèse et la pédodontie.</p>
      <p data-fade>Cette organisation change beaucoup de choses pour vous. Un traitement complexe, qui associe par exemple une extraction, un implant et une couronne, est planifié d'un bout à l'autre par la même équipe. Vous n'avez pas à multiplier les adresses ni à répéter votre histoire.</p>

      <h3 data-fade>Nos engagements</h3>
      <ul class="tp-check" data-fade>
        <li><b>Une équipe pluridisciplinaire</b> : toutes les spécialités réunies pour traiter chaque cas dans sa globalité.</li>
        <li><b>Des soins sans douleur</b> : anesthésie soignée et protocoles doux, y compris pour les patients anxieux.</li>
        <li><b>Un devis écrit avant chaque traitement</b> : vous connaissez le plan, la durée et le coût avant de commencer.</li>
        <li><b>Des explications claires</b> : chaque étape vous est présentée, avec les alternatives possibles.</li>
      </ul>

      <h3 data-fade>Le plateau technique</h3>
      <ul class="tp-check" data-fade>
        <li><b>Radiologie et scanner sur place</b> : radiographie panoramique et 3D réalisées au cabinet, sans rendez-vous extérieur.</li>
        <li><b>Empreinte numérique</b> : un scanner intra-oral remplace la pâte à empreinte, pour plus de confort et de précision.</li>
        <li><b>Chirurgie guidée</b> : les interventions implantaires sont planifiées sur la radiographie 3D.</li>
        <li><b>Stérilisation</b> : les instruments sont stérilisés en autoclave après chaque patient.</li>
      </ul>

      <h3 data-fade>Nos spécialités</h3>
      <ul class="tp-links" data-fade>%(specs)s</ul>

      <h3 data-fade>Venir au cabinet</h3>
      <p data-fade>Bureau N1, Imm Bureaux El Menzah N5, avenue des FAR, Meknès 50000. Le cabinet est ouvert du lundi au vendredi de 8h30 à 17h30 et le samedi de 9h00 à 14h30. <a href="%(maps)s" target="_blank" rel="noopener">Ouvrir l'itinéraire dans Google Maps</a>.</p>
    </div>
  </section>
''' % dict(meta=meta_aside([[('pin', 'ADRESSE', 'Av des FAR, Meknès'), ('clock', 'LUN – VEN', '8h30 – 17h30'), ('cal', 'SAMEDI', '9h00 – 14h30')],
                             [('shield', 'SPÉCIALITÉS', '6 réunies'), ('scan', 'RADIOLOGIE', '2D et 3D sur place'), ('user', 'PRATICIEN', 'Dr T. Boukadous')]]),
           specs=specs, maps=MAPS) \
        + lieu('accueil-cabinet-cdc-meknes.jpg', "Bureau du Centre Dentaire Chifaa et mur au logo CDC") + cta_arc() + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "url": SITE + path, "name": "Le cabinet – Centre Dentaire Chifaa", "about": DENTIST},
        crumbs([('Accueil', '/'), ('Le cabinet', path)])]}
    return (path, "Le cabinet | Centre Dentaire Chifaa, dentiste à Meknès",
            "Le Centre Dentaire Chifaa du Dr Taoufik Boukadous, avenue des FAR à Meknès : six spécialités, radiologie 3D sur place et empreinte numérique.",
            'reception-cabinet-cdc-meknes.jpg', ld, body)

SHOW_CF_LOC = False   # contact : photo du bureau + carte « Meknès, Maroc » masquée pour l'instant
CF_LOC = '''
  <section class="cf-loc" aria-label="Adresse et coordonnées">
    <img class="cf-loc-bg" src="/assets/img/accueil-cabinet-cdc-meknes.jpg" alt="Bureau du Centre Dentaire Chifaa à Meknès et mur au logo CDC" loading="lazy" data-lieu-parallax>
    <div class="cf-loc-list">
      <a class="lieu-card" href="%(maps)s" target="_blank" rel="noopener" data-fade>
        <span class="lieu-title"><span class="lieu-h">Meknès, Maroc</span><span class="lieu-arrow" aria-hidden="true">%(arrow)s</span></span>
        <span class="lieu-space" aria-hidden="true"></span>
        <span class="lieu-address"><span>Bureau N1, Imm Bureaux El Menzah N5</span><span>Av des FAR, Meknès 50000</span></span>
        <span class="lieu-hours"><span>Lun – Ven : 8h30 – 17h30</span><span>Sam : 9h00 – 14h30</span></span>
      </a>
    </div>
  </section>
'''

def contact_page():
    """Page contact : même composition que la page contact de la référence (Caliora)."""
    path = '/contact/'
    PLUS = ('<span class="cf-acc-ic" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 5v14"/><path d="M5 12h14"/></svg></span>')
    ARROW = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 7l-10 10"/><path d="M8 7h9v9"/></svg>')
    faqs = [
        ("Comment prendre rendez-vous ?", "Appelez le cabinet au 05 35 51 69 24, écrivez-nous sur WhatsApp ou réservez directement en ligne sur Dentisto. Nous vous proposons un créneau aux horaires d'ouverture."),
        ("Que faut-il apporter à la première consultation ?", "Votre pièce d'identité, vos radiographies ou comptes rendus récents s'ils existent, la liste de vos traitements en cours et, le cas échéant, les documents de votre mutuelle ou de votre assurance."),
        ("Que faire en cas d'urgence dentaire ?", "Appelez le cabinet pendant les horaires d'ouverture et expliquez la situation : douleur, dent cassée, gonflement. Nous faisons notre possible pour vous recevoir rapidement. En dehors des horaires, laissez-nous un message sur WhatsApp."),
        ("Le cabinet travaille-t-il avec les mutuelles et assurances ?", "Un devis écrit et détaillé vous est remis avant tout traitement. Nous vous fournissons les documents nécessaires pour vos démarches de remboursement auprès de votre mutuelle ou de votre assurance."),
    ]
    faq_html = ''.join(
        '<div class="cf-faq-item" data-fade><span class="cf-faq-num mono">%d</span><div class="cf-acc">'
        '<button class="cf-acc-t" type="button" aria-expanded="false"><span>%s</span>%s</button>'
        '<div class="cf-acc-d"><div><p>%s</p></div></div></div></div>' % (i + 1, q, PLUS, r) for i, (q, r) in enumerate(faqs))
    gal = [('cabinet-radiologie-3d-meknes.jpg', "Appareil de radiologie 3D du cabinet"),
           ('cabinet-salle-de-soins-meknes.jpg', "Salle de soins et unit dentaire"),
           ('reception-cabinet-cdc-meknes.jpg', "Accueil et comptoir de réception"),
           ('cabinet-sterilisation-meknes.jpg', "Stérilisation des instruments en autoclave"),
           ('accueil-cabinet-cdc-meknes.jpg', "Bureau du praticien et mur au logo CDC"),
           ('cabinet-couloir-meknes.jpg', "Couloir et cloisons vitrées du cabinet"),
           ('cabinet-diplomes-dr-boukadous.jpg', "Diplômes et attestations de formation du Dr Boukadous"),
           ('hero-poster.jpg', "Entrée du cabinet et mur à la citation sur le sourire")]
    gal_html = ''.join('<figure data-fade><a class="tp-lb-link" href="/assets/img/%s" data-lightbox="contact" aria-label="Agrandir la photo" '
                       'aria-haspopup="dialog"><img src="/assets/img/%s" alt="%s" loading="lazy">%s</a></figure>' % (f, f, H.escape(a), LB_IC)
                       for f, a in gal)
    body = '''
<main id="top">

  <section class="cf-hero">
    <img class="cf-hero-bg" src="/assets/img/reception-cabinet-cdc-meknes.jpg" alt="Accueil et comptoir de réception du Centre Dentaire Chifaa à Meknès" fetchpriority="high">
    <span class="cf-hero-tint" aria-hidden="true"></span>
    <h1 class="cf-hero-title">Contact<span class="sr-only"> du Centre Dentaire Chifaa, dentiste à Meknès</span></h1>
  </section>
  <div class="cf-duo">
''' + booking(title='Planifiez votre visite') + '''
  <section class="cf-map cf-map-pin" aria-label="Trouver le cabinet">
    <img class="cf-map-bg" src="/assets/img/plan-quartier-cabinet-meknes.jpg" alt="Plan du quartier de l'avenue des FAR à Meknès, avec l'emplacement du cabinet" loading="lazy">
    <span class="cf-map-fade" aria-hidden="true"></span>
    <div class="cf-map-head">
      <h2 class="cf-map-h">Trouver le cabinet</h2>
      <a class="cf-map-link" href="%(maps)s" target="_blank" rel="noopener"><span>Itinéraire</span><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6l-6 6"/></svg><i aria-hidden="true"></i></a>
    </div>
    <a class="cf-pin" href="%(maps)s" target="_blank" rel="noopener" aria-label="Centre Dentaire Chifaa, Av des FAR : ouvrir dans Google Maps">
      <span class="cf-pin-pulse" aria-hidden="true"></span><span class="cf-pin-pulse" aria-hidden="true"></span>
      <svg class="cf-pin-ic" width="34" height="44" viewBox="0 0 34 44" aria-hidden="true"><path d="M17 43s15-14.6 15-26A15 15 0 0 0 2 17c0 11.4 15 26 15 26z" fill="#0E3E68" stroke="#F4F2F0" stroke-width="2"/><circle cx="17" cy="17" r="5.5" fill="#F4F2F0"/></svg>
      <span class="cf-pin-label">Centre Dentaire Chifaa</span>
    </a>
    <small class="cf-map-credit">© contributeurs OpenStreetMap</small>
  </section>
  </div>

  <section class="cf-faq" aria-labelledby="cf-faq-h">
    <h2 id="cf-faq-h" data-lines>Questions fréquentes</h2>
    <div class="cf-faq-list">%(faq)s</div>
  </section>

  <section class="cf-gal" aria-labelledby="cf-gal-h">
    <h2 id="cf-gal-h" data-lines>Pensé pour votre confort et la précision</h2>
    <a class="btn btn-light cf-gal-btn" href="/le-cabinet/">Voir le cabinet%(orb)s</a>
    <div class="cf-gal-grid">%(gal)s</div>
  </section>
%(loc)s

</main>
''' % dict(maps=MAPS, arrow=ARROW, faq=faq_html, gal=gal_html, orb=ORB,
           loc=(CF_LOC % dict(maps=MAPS, arrow=ARROW)) if SHOW_CF_LOC else '')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ContactPage", "url": SITE + path, "name": "Contact – Centre Dentaire Chifaa", "about": DENTIST},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faqs]},
        crumbs([('Accueil', '/'), ('Contact', path)])]}
    return (path, "Contact | Centre Dentaire Chifaa, dentiste à Meknès",
            "Centre Dentaire Chifaa, Av des FAR à Meknès : 05 35 51 69 24, WhatsApp ou réservation en ligne. Lun-ven 8h30-17h30, sam 9h00-14h30.",
            'reception-cabinet-cdc-meknes.jpg', ld, body)

def legal_page(path, title, h1, sections, desc):
    secs = ''.join('<h2>%s</h2>%s' % (h, c) for h, c in sections)
    body = '''
<main id="top">
  <section class="legal">
    <nav class="tp-pills" aria-label="Fil d'Ariane"><a class="tp-pill" href="/">Accueil</a><span class="tp-pill is-cur" aria-current="page">%s</span></nav>
    <h1>%s</h1>
    <p class="legal-date">Dernière mise à jour : septembre 2026</p>
    <div class="legal-body">%s</div>
  </section>
</main>
''' % (h1, h1, secs)
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "url": SITE + path, "name": title},
                                                        crumbs([('Accueil', '/'), (h1, path)])]}
    return path, title, desc, 'reception-cabinet-cdc-meknes.jpg', ld, body

def credits_html():
    p = os.path.join(ROOT, 'tools', 'credits-photos.json')
    items = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
    rows = ''.join('<li><b>%s</b> : « %s », %s, licence %s, <a href="%s" target="_blank" rel="noopener">%s</a>.</li>'
                   % (H.escape(c['file']), H.escape(c['title'].replace('File:', '')), H.escape(c['author'] or 'auteur non précisé'),
                      H.escape(c['license']), H.escape(c['url']), H.escape(c.get('source', 'Wikimedia Commons'))) for c in items)
    return '<ul>%s</ul>' % rows

def credits_short():
    """Crédits photo en une ligne : auteur (licence) par photo source, sans les images propres au cabinet."""
    p = os.path.join(ROOT, 'tools', 'credits-photos.json')
    items = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
    seen, parts = set(), []
    for c in items:
        if 'CDC' in (c.get('license') or '') or c.get('source', 'Wikimedia Commons') != 'Wikimedia Commons':
            continue
        lic = c['license']
        if lic in ('CC0', 'Public domain'):
            continue   # aucune attribution exigée
        author = (c['author'] or 'auteur non précisé').split(',')[0].strip()
        author = re.sub(r'^w:\s*', '', author)
        author = re.sub(r'^The original uploader was (\S+).*$', r'\1', author)
        key = (author, lic)
        if key in seen:
            continue
        seen.add(key)
        parts.append('<a href="%s" target="_blank" rel="noopener">%s</a> (%s)' % (H.escape(c['url']), H.escape(author), H.escape(lic)))
    return ("<p>Certaines photos d'illustration proviennent de Wikimedia Commons et sont utilisées selon leur licence : "
            + ', '.join(parts) + '.</p>')

TODO = '<span class="legal-todo">[à compléter]</span>'

def mentions_page():
    s = [
     ("Éditeur du site", "<p>Le site www.centredentairechifaa.ma est édité par le Centre Dentaire Chifaa, cabinet de chirurgie dentaire du Dr Taoufik Boukadous.</p>"
      "<ul><li><b>Adresse</b> : Bureau N1, Imm Bureaux El Menzah N5, Av des FAR, Meknès 50000, Maroc</li>"
      "<li><b>Téléphone</b> : 05 35 51 69 24</li>"
      "<li><b>E-mail</b> : <a href=\"mailto:%(mail)s\">%(mail)s</a></li>"
      "<li><b>Identifiant commun de l'entreprise (ICE)</b> : %(ice)s</li>"
      "<li><b>Numéro d'inscription au Conseil national de l'Ordre des médecins dentistes</b> : %(ordre)s</li></ul>"
      "<p><b>Directeur de la publication</b> : Dr Taoufik Boukadous.</p>" % dict(mail=EMAIL, ice=ICE, ordre=ORDRE)),
     ("Conception et réalisation", "<p>Site conçu et développé par MouaDev.</p>"),
     ("Hébergement", "<p>Le site est hébergé par Vercel Inc., <a href=\"https://vercel.com\" target=\"_blank\" rel=\"noopener\">vercel.com</a>.</p>"),
     ("Nature des informations", "<p>Les contenus de ce site sont fournis à titre d'information générale sur les soins proposés par le cabinet. Ils ne remplacent pas une consultation : seul un examen clinique permet d'établir un diagnostic et un plan de traitement adaptés. Aucun tarif n'est affiché ; un devis écrit est remis après la consultation.</p>"),
     ("Propriété intellectuelle", "<p>Le logo, les textes et les photographies du cabinet sont la propriété du Centre Dentaire Chifaa. Toute reproduction sans autorisation écrite est interdite. Certaines photographies d'illustration proviennent de Wikimedia Commons et de banques d'images libres (StockSnap, Rawpixel) et sont utilisées selon leur licence Creative Commons, CC0 ou domaine public ; leurs auteurs sont crédités ci-dessous.</p>"),
     ("Crédits photographiques", credits_short()),
     ("Liens externes", "<p>Le site contient des liens vers des services tiers : Google Maps, WhatsApp, Instagram et la plateforme de réservation Dentisto. Le cabinet n'est pas responsable du contenu de ces services.</p>"),
     ("Données personnelles", "<p>Le traitement des données personnelles est décrit dans notre <a href=\"/politique-de-confidentialite/\">politique de confidentialité</a>.</p>"),
    ]
    return legal_page('/mentions-legales/', "Mentions légales | Centre Dentaire Chifaa, Meknès", "Mentions légales", s,
                      "Mentions légales du Centre Dentaire Chifaa, cabinet du Dr Taoufik Boukadous à Meknès : éditeur, hébergement, propriété intellectuelle, crédits.")

def privacy_page():
    s = [
     ("Qui est responsable de vos données ?", "<p>Le Centre Dentaire Chifaa, cabinet du Dr Taoufik Boukadous, Bureau N1, Imm Bureaux El Menzah N5, Av des FAR, Meknès 50000, est responsable des données collectées par ce site. Le traitement respecte la loi marocaine n° 09-08 relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel.</p>"),
     ("Quelles données, et pourquoi ?", "<p>Le site ne crée pas de compte et n'enregistre aucune donnée dans une base en ligne. Lorsque vous utilisez le formulaire de demande de rendez-vous, les informations saisies (nom, téléphone, e-mail facultatif, motif, traitement souhaité, disponibilité) servent uniquement à préparer un message WhatsApp que vous envoyez vous-même au cabinet. Elles sont utilisées pour organiser votre rendez-vous et vous recontacter.</p>"),
     ("Services tiers", "<ul><li><b>WhatsApp</b> : les messages envoyés au cabinet sont soumis aux conditions de WhatsApp (Meta).</li>"
      "<li><b>Dentisto</b> : la réservation en ligne est gérée par la plateforme Dentisto, selon sa propre politique de confidentialité.</li>"
      "<li><b>Google Maps et Google Fonts</b> : l'affichage du plan et des polices de caractères implique une connexion aux serveurs de Google, qui reçoit votre adresse IP.</li>"
      "<li><b>Hébergement</b> : Vercel Inc. conserve des journaux techniques de connexion nécessaires au fonctionnement et à la sécurité du site.</li></ul>"),
     ("Cookies", "<p>Le site n'utilise pas de cookies publicitaires ni d'outil de mesure d'audience. Les services tiers intégrés, comme la carte Google Maps, peuvent déposer leurs propres cookies.</p>"),
     ("Durée de conservation", "<p>Les échanges liés à une demande de rendez-vous sont conservés le temps nécessaire à la prise en charge. Les données médicales de votre dossier patient sont conservées au cabinet selon les obligations légales applicables aux professionnels de santé.</p>"),
     ("Vos droits", "<p>Vous disposez d'un droit d'accès, de rectification et d'opposition au traitement de vos données. Pour l'exercer, contactez le cabinet au 05 35 51 69 24 ou par e-mail à <a href=\"mailto:centredentairechifaa@gmail.com\">centredentairechifaa@gmail.com</a>. Vous pouvez également saisir la Commission nationale de contrôle de la protection des données à caractère personnel (CNDP), <a href=\"https://www.cndp.ma\" target=\"_blank\" rel=\"noopener\">www.cndp.ma</a>.</p>"
),
    ]
    return legal_page('/politique-de-confidentialite/', "Politique de confidentialité | Centre Dentaire Chifaa", "Politique de confidentialité", s,
                      "Politique de confidentialité du site du Centre Dentaire Chifaa à Meknès : données collectées, services tiers, cookies et droits selon la loi 09-08.")

# --------------------------------------------------------------------------------------------
def write(page, header, footer, fabs):
    path, title, desc, img, ld, body = page
    noindex = path in ('/mentions-legales/', '/politique-de-confidentialite/')
    h, f = mark_current(header, footer, path)
    pre = re.search(r'class="tp-hero-bg" src="/assets/img/([^"]+)"', body)
    ld = build_graph(ld, path, title, desc, img)
    out = head(title, desc, path, img, ld, noindex, pre.group(1) if pre else None) + h + '\n' + body + '\n' + f + '\n\n' + fabs.replace('href="/"', 'href="#top"') + SCRIPTS
    target = os.path.join(ROOT, path.strip('/').replace('/', os.sep), 'index.html')
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, 'w', encoding='utf-8').write(out)
    words = len(re.sub(r'<script.*?</script>|<[^>]+>', ' ', body, flags=re.S).split())
    print('%-38s %5d mots' % (path, words))

def lastmods(urls):
    """Date du dernier changement réel de chaque page, mémorisée dans tools/lastmod.json."""
    import hashlib, datetime
    store_path = os.path.join(ROOT, 'tools', 'lastmod.json')
    try:
        store = json.load(open(store_path, encoding='utf-8'))
    except (OSError, ValueError):
        store = {}
    today = datetime.date.today().isoformat()
    out = {}
    for p in urls:
        f = os.path.join(ROOT, p.strip('/').replace('/', os.sep), 'index.html')
        html = re.sub(r'\?v=[0-9a-z]+', '', open(f, encoding='utf-8').read())
        h = hashlib.sha1(html.encode('utf-8')).hexdigest()
        if store.get(p, {}).get('hash') != h:
            store[p] = {'hash': h, 'date': today}
        out[p] = store[p]['date']
    json.dump(store, open(store_path, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    return out

def sitemap(paths):
    urls = ['/'] + [p for p in paths if p not in ('/mentions-legales/', '/politique-de-confidentialite/')]
    pri = {'/': '1.0'}
    mod = lastmods(urls)
    items = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>\n'
                    % (SITE, p, mod[p], pri.get(p, '0.9' if p.startswith('/soins/') else '0.7' if p.startswith('/blog/') else '0.6')) for p in urls)
    # version texte (une URL par ligne), acceptée aussi par Google et Bing
    open(os.path.join(ROOT, 'sitemap.txt'), 'w', encoding='utf-8', newline='\n').write(''.join(SITE + p + '\n' for p in urls))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % items)

def main():
    header, footer, fabs = load_chrome()
    header, footer, fabs = absolutize(header), absolutize(footer), absolutize(fabs)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pages_extra
    from articles import ARTICLES
    ARTICLES_REF.extend(ARTICLES)
    pages = [pages_extra.soins_hub(sys.modules[__name__])] + [soin_page(s) for s in SOINS_ORDER] + [pages_extra.cabinet_about(sys.modules[__name__]), contact_page()] + pages_extra.pages(sys.modules[__name__])         + [mentions_page(), privacy_page()]
    for p in pages:
        write(p, header, footer, fabs)
    sitemap([p[0] for p in pages])
    home_ld = build_graph({"@graph": [{"@type": "WebPage"}]}, '/',
                          'Dentiste à Meknès | Centre Dentaire Chifaa – Dr Boukadous',
                          'Centre Dentaire Chifaa, dentiste à Meknès (Av. des FAR) : implants, orthodontie, parodontie, pédodontie. Devis écrit.',
                          'og-centre-dentaire-chifaa.jpg')
    home_ld['@graph'][3]['mainEntity'] = {'@id': ID_ORG}
    idx = os.path.join(ROOT, 'index.html')
    src = open(idx, encoding='utf-8', newline='').read()
    blk = json.dumps(home_ld, ensure_ascii=False, indent=1)
    src2 = re.sub(r'(<script type="application/ld\+json">\r?\n).*?(\r?\n</script>)', lambda m: m.group(1) + blk + m.group(2), src, count=1, flags=re.S)
    if src2 != src:
        open(idx, 'w', encoding='utf-8', newline='').write(src2)
    print('sitemap.xml mis à jour')

if __name__ == '__main__':
    main()
