# -*- coding: utf-8 -*-
"""
Pages Blog (index + articles) et Équipements.
Même composition que les pages /blog et /equipment du modèle de référence,
reconstruites avec les tokens et les contenus du Centre Dentaire Chifaa.
Importé par build_pages.py (les helpers communs sont passés via le module B).
"""
import html as H, math, re
from articles import ARTICLES, AUTHOR, DATE_ISO, DATE_FR

IG = 'https://www.instagram.com/centredentairechifaa.ma/'

ARROW_DOWN = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14"/><path d="M18 13l-6 6l-6 -6"/></svg>')
CHECK = ('<span class="eq-chk" aria-hidden="true"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5l9 -9"/></svg></span>')
PLUS = ('<span class="cf-acc-ic" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 5v14"/><path d="M5 12h14"/></svg></span>')

EXTRA_ICONS = {
    'tag': '<path d="M7.5 7.5m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"/><path d="M3 6v5.172a2 2 0 0 0 .586 1.414l7.71 7.71a2.41 2.41 0 0 0 3.408 0l5.592 -5.592a2.41 2.41 0 0 0 0 -3.408l-7.71 -7.71a2 2 0 0 0 -1.414 -.586h-5.172a3 3 0 0 0 -3 3z"/>',
    'doc': '<path d="M14 3v4a1 1 0 0 0 1 1h4"/><path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    'edit': '<path d="M4 20h4l10.5 -10.5a2.828 2.828 0 1 0 -4 -4l-10.5 10.5v4"/><path d="M13.5 6.5l4 4"/>',
}


def words(a):
    txt = ' '.join([a['lead'], a['intro']] + a['points'] +
                   [' '.join(ps + li) + ' ' + h for h, ps, li in a['sections']])
    return len(txt.split())


def read_min(a):
    return max(3, math.ceil(words(a) / 180))


def art_url(a):
    return '/blog/%s/' % a['slug']


# ------------------------------------------------------------------------------------------
# Blocs du blog
# ------------------------------------------------------------------------------------------
def featured(B, items):
    big, rest = items[0], items[1:6]
    rows = ''.join(
        '<a class="bl-row" href="%s" data-fade><span class="bl-row-img"><img src="/assets/img/%s" alt="" loading="lazy"></span>'
        '<span class="bl-row-t"><span class="bl-row-h">%s</span><span class="mono bl-cat">%s</span></span></a>'
        % (art_url(a), a['img'], a['title'], a['cat'].upper()) for a in rest)
    return '''
  <section class="bl-feat" aria-labelledby="bl-feat-h">
    <h2 id="bl-feat-h" data-lines>Articles à la une</h2>
    <div class="bl-feat-grid">
      <a class="bl-big" href="%(u)s" data-fade>
        <img src="/assets/img/%(img)s" alt="%(alt)s" loading="lazy">
        <span class="bl-big-t">
          <span class="bl-big-h">%(t)s</span>
          <span class="mono bl-meta">CATÉGORIE : <b>%(cat)s</b><br>LECTURE : %(m)d MIN.</span>
        </span>
      </a>
      <div class="bl-rows">%(rows)s</div>
    </div>
  </section>
''' % dict(u=art_url(big), img=big['img'], alt=H.escape(big['alt']), t=big['title'], cat=big['cat'].upper(), m=read_min(big), rows=rows)


def follow_band():
    return '''
  <section class="bl-follow" aria-label="Suivre le cabinet">
    <h2 class="bl-follow-h" data-fade>Suivez nos conseils<br>sur Instagram</h2>
    <div class="bl-follow-r" data-fade>
      <p>Conseils de prévention, coulisses du cabinet et réponses à vos questions, publiés par l'équipe du Centre Dentaire Chifaa.</p>
      <a class="btn btn-light btn-big" href="%s" target="_blank" rel="noopener">Nous suivre%s</a>
    </div>
  </section>
''' % (IG, '%(orb)s')


def blog_index(B):
    path = '/blog/'
    latest = ARTICLES[:2]
    lat = ''.join(
        '<a class="bl-latest" href="%s" data-fade><img src="/assets/img/%s" alt="%s" loading="lazy">'
        '<span class="bl-latest-t"><span class="bl-latest-h">%s</span><span class="mono bl-meta">CATÉGORIE : <b>%s</b></span></span></a>'
        % (art_url(a), a['img'], H.escape(a['alt']), a['title'], a['cat'].upper()) for a in latest)
    allc = ''.join(
        '<a class="bl-card" href="%s" data-fade><span class="bl-card-img"><img src="/assets/img/%s" alt="%s" loading="lazy"></span>'
        '<span class="bl-card-h">%s</span><span class="mono bl-cat">%s<br>LECTURE %d MIN.</span></a>'
        % (art_url(a), a['img'], H.escape(a['alt']), a['title'], a['cat'].upper(), read_min(a)) for a in ARTICLES)
    body = '''
<main id="top">

  <section class="cf-hero">
    <div class="ph ph-dark cf-hero-bg"><span class="ph-body"><span class="ph-label mono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 7h1a2 2 0 0 0 2 -2a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1a2 2 0 0 0 2 2h1a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2"/><path d="M9 13a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/></svg>PHOTO À PRENDRE · PAYSAGE 21:9</span><span class="ph-title">Les gestes d'hygiène du quotidien</span><span class="ph-reco">Brosse à dents, fil dentaire et dentifrice posés près d'une fenêtre, lumière naturelle douce, fond clair. Laisser le centre et le bas de l'image calmes : le grand titre « BLOG » s'y superpose.</span></span></div>
    <span class="cf-hero-tint" aria-hidden="true"></span>
    <h1 class="cf-hero-title"><span class="sr-only">Le </span>Blog<span class="sr-only"> dentaire du Centre Dentaire Chifaa, dentiste à Meknès</span></h1>
  </section>
''' + featured(B, ARTICLES[2:] + ARTICLES[:2]) + '''
  <section class="bl-all" aria-label="Articles">
    <h2 data-lines>Derniers articles</h2>
    <div class="bl-latest-grid">%(lat)s</div>

    <h2 class="bl-all-h" data-lines>Tous les articles</h2>
    <div class="bl-grid">%(all)s</div>
  </section>
''' % dict(lat=lat, all=allc) + follow_band() % dict(orb=B.ORB) + book_ring() + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": B.SITE + path + "#blog", "url": B.SITE + path, "name": "Blog du Centre Dentaire Chifaa",
         "inLanguage": "fr", "publisher": {"@id": B.SITE + "/#cabinet"},
         "blogPost": [{"@type": "BlogPosting", "headline": a['title'], "url": B.SITE + art_url(a), "datePublished": DATE_ISO} for a in ARTICLES]},
        B.DENTIST,
        B.crumbs([('Accueil', '/'), ('Blog', path)])]}
    return (path, "Blog dentaire : conseils d'un dentiste à Meknès | CDC",
            "Conseils d'un cabinet dentaire de Meknès : implants, orthodontie, dents de sagesse, gencives et soins des enfants, expliqués simplement.",
            'cabinet-couloir-meknes.jpg', ld, body)


def article(B, a):
    path = art_url(a)
    m = read_min(a)
    soin_path = '/soins/%s-meknes/' % a['soin']
    secs = []
    for h, ps, li in a['sections']:
        s = '<h2 data-fade>%s</h2>' % h + ''.join('<p data-fade>%s</p>' % p for p in ps)
        if li:
            s += '<ul class="tp-check ar-check" data-fade>%s</ul>' % ''.join('<li>%s</li>' % x for x in li)
        secs.append(s)
    meta = B.meta_aside([
        [('user', 'AUTEUR', 'Équipe CDC'),
         ('tag', 'CATÉGORIE', '<a href="%s">%s</a>' % (soin_path, a['cat']))],
        [('clock', 'LECTURE', '%d min.' % m), ('doc', 'PUBLIÉ', DATE_FR), ('edit', 'MIS À JOUR', DATE_FR)]])
    others = [x for x in ARTICLES if x is not a]
    body = '''
<main id="top">

  <section class="ar-hero">
    <img class="ar-hero-bg" src="/assets/img/%(img)s" alt="%(alt)s" fetchpriority="high">
    <div class="ar-hero-copy">
      <p class="ar-date mono"><span>PUBLIÉ</span><time datetime="%(iso)s">%(date)s</time></p>
      <h1 data-lines>%(title)s</h1>
      <ul class="ar-tags mono" data-fade>
        <li>%(m)d MIN.</li><li>%(author)s</li><li><a href="/blog/">%(cat)s</a></li>
      </ul>
    </div>
    <a class="ar-down" href="#article" aria-label="Lire l'article">%(down)s</a>
  </section>

  <section class="tp-panel ar-panel" id="article">
    %(meta)s

    <article class="tp-rich ar-rich">
      <p class="ar-lead" data-lines>%(lead)s</p>
      <p class="ar-intro" data-fade>%(intro)s</p>
      <ul class="tp-check ar-check" data-fade>%(points)s</ul>
      %(secs)s
      <aside class="ar-note" data-fade>
        <p>Cet article donne des informations générales. Il ne remplace pas une consultation : seul un examen permet de poser un diagnostic et de proposer un traitement adapté à votre situation.</p>
        <p>En savoir plus : <a href="%(soin)s">%(soin_name)s à Meknès</a>, ou appelez le cabinet au <a href="tel:+212535516924">05 35 51 69 24</a>.</p>
      </aside>
    </article>
  </section>
''' % dict(img=a['img'], alt=H.escape(a['alt']), iso=DATE_ISO, date=DATE_FR.upper(), title=a['title'], m=m,
           author='CENTRE DENTAIRE CHIFAA', cat=a['cat'].upper(), down=ARROW_DOWN, meta=meta, lead=a['lead'],
           intro=a['intro'], points=''.join('<li>%s</li>' % p for p in a['points']), secs='\n      '.join(secs),
           soin=soin_path, soin_name=B.SOIN_NAME[a['soin']]) \
        + follow_band() % dict(orb=B.ORB) + featured(B, others) + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": B.SITE + path + "#article", "headline": a['title'], "description": a['lead'],
         "image": B.SITE + "/assets/img/" + a['img'], "datePublished": DATE_ISO, "dateModified": DATE_ISO,
         "inLanguage": "fr", "articleSection": a['cat'], "timeRequired": "PT%dM" % m,
         "author": {"@type": "Organization", "name": AUTHOR, "@id": B.SITE + "/#cabinet"},
         "publisher": {"@id": B.SITE + "/#cabinet"}, "mainEntityOfPage": B.SITE + path, "isPartOf": {"@id": B.SITE + "/blog/#blog"}},
        B.DENTIST,
        B.crumbs([('Accueil', '/'), ('Blog', '/blog/'), (a['title'], path)])]}
    desc = a['lead'] if len(a['lead']) <= 155 else a['lead'][:152].rsplit(' ', 1)[0] + '…'
    return (path, "%s | CDC Meknès" % a.get('seo', a['title']), desc, a['img'], ld, body)


# ------------------------------------------------------------------------------------------
# Équipements
# ------------------------------------------------------------------------------------------
EQUIP = [
    dict(name="Radiologie panoramique et 3D", img='cabinet-radiologie-3d-meknes.jpg',
         alt="Appareil de radiologie panoramique et 3D du Centre Dentaire Chifaa",
         desc="Radiographie panoramique et imagerie 3D réalisées au cabinet, sans examen à faire ailleurs. Elles servent au diagnostic et à la planification des implants, des dents de sagesse et des traitements d'orthodontie.",
         specs=["Vatech", "Panoramique 2D", "Imagerie 3D"], btn=("Implants dentaires", '/soins/implants-dentaires-meknes/')),
    dict(name="Empreinte numérique", img='cabinet-scan-3d-empreinte.jpg',
         alt="Écran affichant le scan 3D d'une arcade dentaire",
         desc="Un scanner intra-oral enregistre vos dents en 3D, sans pâte à empreinte. Plus confortable et plus précis, il sert à concevoir les aligneurs, les couronnes et les prothèses sur implants.",
         specs=["Sans pâte à empreinte", "Modèle 3D à l'écran", "Aligneurs et prothèses"], btn=("Orthodontie", '/soins/orthodontie-meknes/')),
    dict(name="Salle de soins", img='cabinet-salle-de-soins-meknes.jpg',
         alt="Salle de soins et unit dentaire du cabinet",
         desc="Un fauteuil et un unit dentaire pensés pour votre confort pendant les soins, qu'il s'agisse d'un contrôle, d'un soin conservateur ou d'une intervention de chirurgie orale.",
         specs=["Confort du patient", "Soins conservateurs", "Chirurgie orale"], btn=("Chirurgie orale", '/soins/chirurgie-orale-meknes/')),
    dict(name="Stérilisation", img='cabinet-sterilisation-meknes.jpg',
         alt="Autoclave de stérilisation des instruments",
         desc="Après chaque patient, les instruments sont nettoyés puis stérilisés en autoclave. Une étape invisible pour vous, essentielle à votre sécurité.",
         specs=["Autoclave", "Après chaque patient", "Hygiène et sécurité"], btn=("Le cabinet", '/le-cabinet/')),
]

SHOW_FEATURES = False   # page équipements : section « Ce qui fait la différence »

FEATURES = [
    ("Des soins sans douleur", "Anesthésie soignée, gestes doux et pauses quand vous en avez besoin. Les patients anxieux et les enfants sont pris en charge à leur rythme."),
    ("Une planification numérique", "La radiographie 3D et l'empreinte numérique permettent de préparer chaque traitement en amont, en particulier la pose des implants et les aligneurs."),
    ("Une équipe pluridisciplinaire", "Orthodontie, implantologie, chirurgie orale, parodontie, prothèse et pédodontie sont réunies au même endroit, pour traiter chaque cas dans sa globalité."),
    ("La transparence", "Un devis écrit et détaillé vous est remis après la consultation, avant tout engagement. Chaque étape du traitement vous est expliquée."),
]

GAL = [('cabinet-radiologie-3d-meknes.jpg', "Appareil de radiologie 3D du cabinet"),
       ('cabinet-salle-de-soins-meknes.jpg', "Salle de soins et unit dentaire"),
       ('reception-cabinet-cdc-meknes.jpg', "Accueil et comptoir de réception"),
       ('cabinet-sterilisation-meknes.jpg', "Stérilisation des instruments en autoclave"),
       ('accueil-cabinet-cdc-meknes.jpg', "Bureau du praticien et mur au logo CDC"),
       ('cabinet-couloir-meknes.jpg', "Couloir et cloisons vitrées du cabinet"),
       ('cabinet-diplomes-dr-boukadous.jpg', "Diplômes et attestations de formation du Dr Boukadous"),
       ('hero-poster.jpg', "Entrée du cabinet et mur à la citation sur le sourire")]


def equipment(B):
    path = '/equipements/'
    items = ''.join('''
      <article class="eq-item" data-eq-item>
        <figure class="eq-img"><img src="/assets/img/%(img)s" alt="%(alt)s" loading="lazy"></figure>
        <div class="eq-content">
          <h2>%(name)s</h2>
          <p>%(desc)s</p>
          <a class="btn btn-light btn-big" href="%(href)s">%(bt)s%(orb)s</a>
        </div>
        <ul class="eq-details">%(specs)s</ul>
      </article>''' % dict(img=e['img'], alt=H.escape(e['alt']), name=e['name'], desc=e['desc'], href=e['btn'][1], bt=e['btn'][0],
                           orb=B.ORB, specs=''.join('<li>%s<span>%s</span></li>' % (CHECK, s) for s in e['specs'])) for e in EQUIP)
    gal = ''.join('<figure data-fade><a class="tp-lb-link" href="/assets/img/%s" data-lightbox="equipements" aria-label="Agrandir la photo" '
                  'aria-haspopup="dialog"><img src="/assets/img/%s" alt="%s" loading="lazy">%s</a></figure>' % (f, f, H.escape(a), B.LB_IC)
                  for f, a in GAL)
    feats = ''.join(
        '<div class="cf-faq-item" data-fade><span class="cf-faq-num mono">%d</span><div class="cf-acc">'
        '<button class="cf-acc-t" type="button" aria-expanded="false"><span>%s</span>%s</button>'
        '<div class="cf-acc-d"><div><p>%s</p></div></div></div></div>' % (i + 1, q, PLUS, r) for i, (q, r) in enumerate(FEATURES))
    thumbs = ''.join('<a class="tp-lb-link" href="/assets/img/%s" data-lightbox="equipements-detail" aria-label="Agrandir la photo" '
                     'aria-haspopup="dialog"><img src="/assets/img/%s" alt="%s" loading="lazy">%s</a>' % (f, f, H.escape(a), B.LB_IC)
                     for f, a in [GAL[0], GAL[3], GAL[1], GAL[6]])
    # section « Ce qui fait la différence » : masquée pour l'instant (SHOW_FEATURES = True pour la réafficher)
    feat_block = '''
  <section class="eq-feat" aria-labelledby="eq-feat-h">
    <div class="eq-feat-l">
      <h2 id="eq-feat-h" data-lines>Ce qui fait la différence</h2>
      <p data-fade>Un plateau technique moderne et des méthodes de travail structurées, pour un diagnostic juste, des traitements efficaces et une expérience confortable.</p>
      <div class="cf-faq-list">%s</div>
    </div>
    <div class="eq-feat-r" data-fade>
      <img class="eq-feat-img" src="/assets/img/accueil-cabinet-cdc-meknes.jpg" alt="Bureau du Centre Dentaire Chifaa et mur au logo CDC" loading="lazy">
      <div class="eq-thumbs">%s</div>
    </div>
  </section>
''' % (feats, thumbs) if SHOW_FEATURES else ''
    body = '''
<main id="top">

  <section class="eq-stack" data-eq-stack>
    <div class="eq-sticky">
      <div class="eq-card" data-eq-card>
        <img class="eq-bg" src="/assets/img/cabinet-salle-de-soins-meknes.jpg" alt="" fetchpriority="high" data-eq-bg>
        <span class="eq-tint" aria-hidden="true"></span>
        <h1 class="eq-title" data-eq-title>Équipements<span class="sr-only"> du Centre Dentaire Chifaa à Meknès : radiologie 3D et empreinte numérique</span></h1>
        <p class="eq-words" aria-hidden="true"><span data-eq-word>Technologie</span><span data-eq-word>Précision</span><span data-eq-word>Confort</span></p>
      </div>
    </div>
  </section>

  <section class="eq-list" aria-label="Nos équipements">%(items)s
  </section>

  <section class="cf-gal eq-gal" aria-labelledby="eq-gal-h">
    <p class="eq-pills mono" data-fade><span>CONFORT</span><span>ENVIRONNEMENT</span></p>
    <h2 id="eq-gal-h" data-lines>Un aperçu du cabinet</h2>
    <p class="eq-gal-p" data-fade>Découvrez nos locaux et notre plateau technique, pensés pour votre confort et la précision des soins.</p>
    <a class="btn btn-light btn-big cf-gal-btn" href="/le-cabinet/">Voir le cabinet%(orb)s</a>
    <div class="cf-gal-grid">%(gal)s</div>
  </section>
%(feat_block)s
</main>
''' % dict(items=items, gal=gal, orb=B.ORB, feat_block=feat_block)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "url": B.SITE + path, "name": "Équipements – Centre Dentaire Chifaa", "about": B.DENTIST},
        B.crumbs([('Accueil', '/'), ('Équipements', path)])]}
    return (path, "Radiologie 3D et équipements dentaires à Meknès | CDC",
            "Radiologie panoramique et 3D sur place, empreinte numérique, salle de soins moderne et stérilisation en autoclave au Centre Dentaire Chifaa, Meknès.",
            'cabinet-radiologie-3d-meknes.jpg', ld, body)


def pages(B):
    B.ICONS.update(EXTRA_ICONS)
    return [equipment(B), blog_index(B)] + [article(B, a) for a in ARTICLES]



# ------------------------------------------------------------------------------------------
# Page mère des soins : /soins/ (composition de la page /treatments de la référence)
# ------------------------------------------------------------------------------------------
HUB_CARDS = [
    ('orthodontie', "Alignement", 'orthodontie-bagues-aligneurs-meknes.jpg', "Bagues métalliques et aligneurs transparents côte à côte",
     "Aligneurs invisibles et bagues métalliques ou céramiques, pour les adultes, les adolescents et les enfants. Chaque traitement est planifié en numérique."),
    ('implants-dentaires', "Remplacement", 'implant-dentaire-pose-meknes.jpg', "Implant dentaire et sa couronne en place entre deux dents",
     "Implant unitaire, bridge sur implants ou arcade complète, pour remplacer une ou plusieurs dents de façon fixe et durable."),
    ('chirurgie-orale', "Chirurgie", 'chirurgie-orale-extraction-3d.jpg', "Illustration 3D de l'extraction d'une dent",
     "Dents de sagesse, dents incluses et extractions délicates, réalisées au cabinet sous anesthésie locale, après radiographie."),
    ('parodontie', "Gencives", 'parodontie-detartrage-avant-apres.jpg', "Gencives avant et après traitement parodontal",
     "Détartrage, surfaçage et suivi des gencives, pour traiter le saignement et le déchaussement et garder vos dents."),
    ('prothese-dentaire', "Restauration", 'facette-ceramique-pose-meknes.jpg', "Pose d'une facette en céramique sur une dent",
     "Couronnes, facettes et bridges en céramique ou en zircone, pour réparer une dent abîmée ou embellir le sourire."),
    ('pedodontie', "Enfants", 'examen-dentaire-enfant.jpg', "Examen dentaire d'un enfant avec des gants",
     "Des soins doux, adaptés à l'âge de l'enfant : première visite, prévention, soins des caries et conseils aux parents."),
]

# bandeau révélé au survol des cartes (la référence y affiche des chiffres ; ici uniquement des faits vérifiables)
HUB_DETAILS = {
    'orthodontie': [("Pour", "Enfants et adultes"), ("Techniques", "Aligneurs, bagues"), ("Plan", "Numérique")],
    'implants-dentaires': [("Solutions", "1 dent à l'arcade"), ("Imagerie", "3D sur place"), ("Devis", "Écrit")],
    'chirurgie-orale': [("Anesthésie", "Locale"), ("Lieu", "Au cabinet"), ("Bilan", "Radiographie")],
    'parodontie': [("Soins", "Détartrage, surfaçage"), ("Suivi", "Maintenance"), ("Objectif", "Garder ses dents")],
    'prothese-dentaire': [("Matériaux", "Céramique, zircone"), ("Soins", "Couronnes, facettes"), ("Devis", "Écrit")],
    'pedodontie': [("Pour", "Les enfants"), ("Approche", "Douce"), ("Parents", "Présents")],
}

# carrousel : carte verticale à gauche, comparaison avant / après à faire glisser à droite.
# Paires alignées (tools : recadrage + alignement) ; ce sont des exemples de résultat, pas des cas du cabinet.
HUB_SLIDES = [
    ('orthodontie', "ORTHODONTIE", "Aligner vos dents, discrètement et à tout âge",
     "Aligneurs transparents ou bagues : la technique est choisie avec vous après l'examen, puis une contention garde le résultat.",
     'orthodontie', "sourire avec un espace entre les incisives", "sourire aux dents alignées"),
    ('parodontie', "PARODONTIE", "Soigner les gencives pour garder ses dents",
     "Une gencive qui saigne est un signal d'alerte. Le traitement arrête la progression du déchaussement et stabilise les dents.",
     'gencives', "gencives rouges et gonflées, tartre au collet", "gencives roses et saines"),
    ('parodontie', "DÉTARTRAGE", "Un détartrage pour des dents nettes",
     "Le tartre entretient l'inflammation des gencives. Un détartrage au moins une fois par an garde vos dents propres et vos gencives saines.",
     'detartrage', "dents du bas couvertes de tartre", "dents du bas nettoyées"),
]

STAR = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 17.27l6.18 3.73l-1.64 -7.03l5.46 -4.73l-7.19 -.61l-2.81 -6.63l-2.81 6.63l-7.19 .61l5.46 4.73l-1.64 7.03z"/></svg>'
ARR_L = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="M11 18l-6 -6l6 -6"/></svg>'
ARR_R = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="M13 6l6 6l-6 6"/></svg>'


def soins_hub(B):
    path = '/soins/'
    cards = ''.join('''
      <a class="st-card" href="/soins/%(s)s-meknes/">
        <span class="st-media">
          <img src="/assets/img/%(img)s" alt="%(alt)s" loading="lazy">
          <span class="st-details" aria-hidden="true">%(det)s<span class="st-details-bg"></span></span>
          <span class="st-tag">%(tag)s</span>
        </span>
        <span class="st-content">
          <h2>%(name)s</h2>
          <span class="st-about">%(desc)s</span>
          <span class="st-action"><span class="btn btn-navy">Voir le soin%(orb)s</span></span>
          <span class="st-content-bg" aria-hidden="true"></span>
        </span>
      </a>''' % dict(s=s, img=img, alt=H.escape(alt), tag=tag, name=B.SOIN_NAME[s], desc=desc, orb=B.ORB,
                     det=''.join('<span class="st-det"><span class="st-det-l">%s</span><span class="st-det-v">%s</span></span>' % d for d in HUB_DETAILS[s]))
                    for s, tag, img, alt, desc in HUB_CARDS)
    n = len(HUB_SLIDES)
    slides = ''.join('''
      <article class="st-slide%(act)s" role="group" aria-roledescription="diapositive" aria-label="%(i)d sur %(n)d"%(hid)s>
        <div class="st-vcard">
          <p class="st-pills mono"><span>SOIN</span><span>%(cat)s</span></p>
          <div class="st-vbody">
            <a class="st-slide-link" href="/soins/%(s)s-meknes/"%(tab)s><h2>%(h)s</h2></a>
            <p class="st-slide-p">%(p)s</p>
            <a class="btn btn-light btn-big" href="/soins/%(s)s-meknes/"%(tab)s>%(name)s%(orb)s</a>
          </div>
        </div>
        <div class="ba" data-ba style="--p:50%%">
          <img class="ba-img ba-after" src="/assets/img/ba-%(pair)s-apres.jpg" alt="Après : %(aa)s" loading="lazy">
          <img class="ba-img ba-before" src="/assets/img/ba-%(pair)s-avant.jpg" alt="Avant : %(ab)s" loading="lazy">
          <span class="ba-tag ba-tag-l mono" aria-hidden="true">AVANT</span>
          <span class="ba-tag ba-tag-r mono" aria-hidden="true">APRÈS</span>
          <span class="ba-line" aria-hidden="true"><span class="ba-knob"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M9 7l-5 5l5 5"/><path d="M15 7l5 5l-5 5"/></svg></span></span>
          <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Comparer avant et après, %(name)s"%(tab)s>
          <span class="ba-note mono">EXEMPLE DE RÉSULTAT</span>
        </div>
      </article>''' % dict(act=' is-active' if i == 0 else '', i=i + 1, n=n, hid='' if i == 0 else ' aria-hidden="true"', cat=cat,
                           s=s, h=h, p=p, name=B.SOIN_NAME[s], orb=B.ORB, tab='' if i == 0 else ' tabindex="-1"', pair=pair,
                           ab=H.escape(ab), aa=H.escape(aa))
                     for i, (s, cat, h, p, pair, ab, aa) in enumerate(HUB_SLIDES))
    body = '''
<main id="top">

  <section class="st-hero">
    <div class="ph ph-dark st-hero-bg"><span class="ph-body"><span class="ph-label mono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 7h1a2 2 0 0 0 2 -2a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1a2 2 0 0 0 2 2h1a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2"/><path d="M9 13a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/></svg>PHOTO À PRENDRE · PAYSAGE 16:9</span><span class="ph-title">Un soin en cours au cabinet</span><span class="ph-reco">Le praticien au travail : mains gantées, instruments et scialytique allumé, patient vu de dos ou sans visage, ou avec son accord écrit. Garder le bas de l'image calme : le titre et les boutons s'y superposent.</span></span></div>
    <div class="st-hero-l" data-st-up>
      <h1>Soins dentaires à Meknès</h1>
      <p>Six spécialités réunies au Centre Dentaire Chifaa, pour des résultats durables et votre confort.</p>
    </div>
    <div class="st-hero-r" data-st-up>
      <a class="st-proof" href="%(maps)s" target="_blank" rel="noopener">
        <span class="mono st-proof-l">NOTÉ 5,0 / 5 SUR GOOGLE<br>43 AVIS PATIENTS</span>
        <span class="st-stars" role="img" aria-label="5 étoiles sur 5">%(stars)s</span>
      </a>
      <div class="st-actions">
        <a class="st-down" href="#soins-liste" aria-label="Voir les soins">%(down)s</a>
        <a class="btn btn-light btn-big" href="#rendez-vous">Prendre rendez-vous%(orb)s</a>
      </div>
    </div>
  </section>

  <section class="st-grid" id="soins-liste" aria-label="Nos spécialités">%(cards)s
  </section>
''' % dict(maps=B.MAPS, stars=STAR * 5, down=ARROW_DOWN, orb=B.ORB, cards=cards) \
        + '''
  <section class="st-slider" data-st-slider aria-roledescription="carrousel" aria-label="Exemples de résultats, avant et après">
    <div class="st-track" data-st-track>%(slides)s
    </div>
    <span class="st-count mono" aria-hidden="true"><b data-st-cur>01</b> / %(total)02d</span>
    <div class="st-bar">
      <button class="st-arrow" type="button" data-st-prev aria-label="Diapositive précédente">%(l)s</button>
      <button class="st-arrow" type="button" data-st-next aria-label="Diapositive suivante">%(r)s</button>
    </div>
  </section>
''' % dict(slides=slides, l=ARR_L, r=ARR_R, total=len(HUB_SLIDES)) + B.booking(title='Planifiez votre visite') + B.cta_arc() + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "url": B.SITE + path, "name": "Soins dentaires à Meknès – Centre Dentaire Chifaa", "about": B.DENTIST,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": "%s à Meknès" % B.SOIN_NAME[s], "url": B.SITE + "/soins/%s-meknes/" % s}
             for i, s in enumerate(B.SOINS_ORDER)]}},
        B.crumbs([('Accueil', '/'), ('Nos soins', path)])]}
    return (path, "Soins dentaires à Meknès | Centre Dentaire Chifaa",
            "Orthodontie, implants, chirurgie orale, parodontie, prothèse et pédodontie : six spécialités au Centre Dentaire Chifaa, Meknès. Devis écrit.",
            'sourire-apres-orthodontie-meknes.jpg', ld, body)



# ------------------------------------------------------------------------------------------
# Le cabinet : /le-cabinet/ (composition de la page /about de la référence)
# Les photos sont remplacées par des blocs « photo à prendre » : ce que la photo doit montrer
# et comment la prendre. Remplacer chaque bloc par la vraie photo une fois reçue.
# ------------------------------------------------------------------------------------------
CAM = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><path d="M5 7h1a2 2 0 0 0 2 -2a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1a2 2 0 0 0 2 2h1a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2"/>'
       '<path d="M9 13a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/></svg>')


def ph(cls, n, title, fmt='', reco='', tone='light', tag='div', attrs=''):
    """Bloc « photo à prendre ». Petit bloc : numéro + titre. Grand bloc : + format et recommandations."""
    body = '<span class="ph-label mono">%sPHOTO %s%s</span><span class="ph-title">%s</span>' % (CAM, n, (' · ' + fmt) if fmt else '', title)
    if reco:
        body += '<span class="ph-reco">%s</span>' % reco
    return '<%s class="ph ph-%s %s"%s><span class="ph-body">%s</span></%s>' % (tag, tone, cls, attrs, body, tag)


# héro : 4 photos en fondu
AB_HERO = [
    ("Le bureau du praticien et le mur au logo CDC", "PAYSAGE 16:9",
     "Plan large pris depuis l'entrée, appareil à hauteur des yeux. Lumière du jour et lumières du cabinet allumées, bureau rangé, aucun écran allumé avec des données de patient."),
    ("La salle de soins", "PAYSAGE 16:9",
     "Fauteuil au centre, scialytique allumé, plan de travail dégagé. Photographier depuis un coin de la pièce pour montrer toute la salle."),
    ("L'accueil et la réception", "PAYSAGE 16:9",
     "Comptoir et logo bien visibles. Pièce vide, ou assistante à son poste avec son accord écrit."),
    ("La radiologie panoramique et 3D", "PAYSAGE 16:9",
     "L'appareil entier, marque lisible, fond dégagé. Éviter les reflets sur les parties blanches."),
]

AB_CARDS = [("Radiologie 3D sur place",
             "Panoramique et imagerie 3D réalisées au cabinet, pour un diagnostic précis sans rendez-vous extérieur.",
             "Le praticien devant l'écran de radiologie", "PORTRAIT 3:4",
             "Vue de dos ou de trois quarts, une image 3D affichée à l'écran. Aucune donnée de patient lisible."),
            ("Six spécialités réunies",
             "Orthodontie, implants, chirurgie, gencives, prothèse et soins des enfants, dans les mêmes murs.",
             "Le praticien au travail", "PORTRAIT 3:4",
             "Mains gantées et instruments en premier plan, patient cadré sans visage ou avec accord écrit."),
            ("Un devis avant chaque soin",
             "Un plan de traitement expliqué et un devis écrit, remis après la consultation et avant tout engagement.",
             "L'explication d'un plan de traitement", "PORTRAIT 3:4",
             "Le praticien montre un devis ou un écran à un patient vu de dos. Document sans nom ni montant lisible.")]

AB_VALUES = ["Écoute", "Précision", "Douceur", "Transparence", "Hygiène", "Suivi"]

# anneau de 6 petites photos carrées
AB_RING = ["Sourire après traitement", "Aligneur en main", "Couronne sur modèle", "Implant sur modèle", "Brossage et hygiène", "Enfant au fauteuil"]

AB_FEATS = [("Des soins sans douleur", "Anesthésie soignée, gestes doux et pauses quand vous en avez besoin, y compris pour les patients anxieux et les enfants."),
            ("Une planification numérique", "Radiographie 3D et empreinte numérique : chaque traitement est préparé en amont, en particulier les implants et les aligneurs."),
            ("Une équipe pluridisciplinaire", "Six spécialités réunies au même endroit, pour traiter chaque cas dans sa globalité sans multiplier les adresses."),
            ("La transparence", "Un devis écrit et détaillé vous est remis après la consultation. Chaque étape du traitement vous est expliquée."),
            ("Un plateau technique moderne", "Radiologie panoramique et 3D, scanner intra-oral et salle de soins équipée, directement au cabinet."),
            ("Hygiène et stérilisation", "Après chaque patient, les instruments sont nettoyés puis stérilisés en autoclave.")]

AB_TECH = ["Fauteuil et unit", "Scanner intra-oral", "Autoclave", "Radio 3D", "Logiciel à l'écran", "Instruments stérilisés"]

# équipe : le Dr est connu ; les autres cartes sont à compléter (supprimer celles qui ne servent pas)
TODO_T = '<span class="legal-todo">[à compléter]</span>'
AB_TEAM = [
    ("Dr Taoufik Boukadous", "CHIRURGIEN-DENTISTE",
     "Responsable du Centre Dentaire Chifaa. " + TODO_T + " : parcours, formations et domaines de prédilection, en deux phrases.",
     "Portrait du Dr Boukadous", "Tenue de travail, au cabinet, regard caméra, épaules détendues. Même cadrage et même fond pour toute l'équipe."),
    ("[Prénom Nom]", "[FONCTION]", TODO_T + " : rôle au cabinet et ce que ce membre apporte aux patients, en deux phrases.",
     "Portrait d'un membre de l'équipe", "Même fond, même lumière et même cadrage que le portrait du Dr, pour une grille homogène."),
]

TOOTH = '<span class="ab-tooth" aria-hidden="true"></span>'
ARROW_UR = ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M17 7l-10 10"/><path d="M8 7h9v9"/></svg>')


def cabinet_about(B):
    path = '/le-cabinet/'
    hero_imgs = ''.join(ph('ab-hero-img' + (' is-active' if i == 0 else ''), i + 1, t, f, r, 'dark') for i, (t, f, r) in enumerate(AB_HERO))
    thumbs = ''.join('<button class="ab-thumb%s" type="button" aria-label="Photo %d : %s" aria-pressed="%s"><span class="mono">%d</span></button>'
                     % (' is-active' if i == 0 else '', i + 1, H.escape(t), 'true' if i == 0 else 'false', i + 1) for i, (t, f, r) in enumerate(AB_HERO))
    cards = ''.join('''
    <div class="ab-card" tabindex="0">
      %s
      <span class="ab-card-ov" aria-hidden="true"></span>
      <div class="ab-card-body">
        <h3>%s</h3>
        <span class="ab-card-line" aria-hidden="true"></span>
        <p data-ab-split>%s</p>
      </div>
    </div>''' % (ph('ab-card-img', 5 + i, pt, pf, pr, 'dark'), t, d) for i, (t, d, pt, pf, pr) in enumerate(AB_CARDS))
    specs = ''.join('<li class="ab-spec"><a href="/soins/%s-meknes/"><span class="ab-spec-ic">%s</span><span class="ab-spec-n">%s</span><span class="ab-spec-i mono">%d</span></a></li>'
                    % (s, TOOTH, B.SOIN_NAME[s], i + 1) for i, s in enumerate(B.SOINS_ORDER))
    values = ''.join('<li style="--k:%d">%s</li>' % (i, v) for i, v in enumerate(AB_VALUES))
    ring = ''.join(ph('ab-ring-img', 13 + i, t, 'CARRÉ', tone='light', tag='div', attrs=' style="--a:%ddeg"' % (i * 60)) for i, t in enumerate(AB_RING))
    feats = ''.join('<li class="ab-feat-card">%s<div><h3>%s</h3><p>%s</p></div></li>' % (TOOTH, t, d) for t, d in AB_FEATS)
    tech_thumbs = ''.join(ph('ab-tech-thumb', 21 + i, t) for i, t in enumerate(AB_TECH))
    team_html = ''.join('''
      <article class="ab-member">
        %s
        <div class="ab-member-body">
          <h3 class="ab-member-name">%s<span class="mono">%s</span></h3>
          <p class="ab-member-about">%s</p>
          <p class="ab-member-links">%s</p>
        </div>
      </article>''' % (ph('ab-member-img', 27 + i, pt, 'PORTRAIT 4:5', pr), n, r, d,
                       ('<a href="%s" target="_blank" rel="noopener">Prendre rendez-vous</a><a href="tel:+212535516924">05 35 51 69 24</a>' % B.BOOK) if i == 0 else '')
                        for i, (n, r, d, pt, pr) in enumerate(AB_TEAM))
    stats = [B.stat('NOTE GOOGLE', '5,0 / 5', B.MAPS), B.stat('AVIS PATIENTS', '43'), B.stat('SPÉCIALITÉS', '6')]
    body = '''
<main id="top">

  <section class="ab-hero" data-ab-hero aria-label="Le cabinet en images">
    <div class="ab-hero-slides">%(hero_imgs)s</div>
    <span class="ab-hero-tint" aria-hidden="true"></span>
    <h1 class="ab-hero-h"><span class="ab-hl">Votre cabinet dentaire</span> <span class="ab-hl">au cœur de Meknès</span></h1>
    <div class="ab-thumbs" aria-label="Choisir une photo">%(thumbs)s</div>
  </section>

  <section class="ab-approach" aria-labelledby="ab-approach-h">
    <p class="ab-pills mono" data-ab-label><span>NOTRE</span><span>APPROCHE</span></p>
    <h2 id="ab-approach-h" class="ab-approach-h" data-ab-split data-ab-reveal>Des soins dentaires de qualité, adaptés à chacun, de la prévention aux traitements complexes. Une approche claire et structurée, centrée sur votre confort, la précision et des résultats durables.</h2>
  </section>

  <section class="ab-stats tp-stats" aria-label="Le centre en chiffres">
    %(stats)s
  </section>

  <section class="ab-cards" aria-label="Ce qui distingue le centre">%(cards)s
  </section>

  <section class="ab-about" aria-labelledby="ab-about-h">
    <p class="ab-pills mono"><span>LE</span><span>CENTRE</span></p>
    <h2 id="ab-about-h" class="ab-about-h">Le Centre Dentaire Chifaa réunit six spécialités et un plateau technique moderne, avenue des FAR. De la prévention aux traitements complexes, nous visons des résultats sur lesquels vous pouvez compter.</h2>
    <div class="ab-bento">
      <div class="ab-bento-l">
        %(ph_bento)s
        <ul class="ab-specs" data-ab-in>%(specs)s</ul>
      </div>
      <div class="ab-bento-r">
        <div class="ab-locs" data-ab-in>
          <div class="ab-loc"><span class="ab-loc-tag mono">MEKNÈS</span><h3>Av des FAR</h3><p>Bureau N1, Imm Bureaux El Menzah N5<br>Meknès 50000</p></div>
          <div class="ab-loc"><span class="ab-loc-tag mono">HORAIRES</span><h3>Lun – Sam</h3><p>Lun – Ven : 8h30 – 17h30<br>Sam : 9h00 – 14h30</p></div>
        </div>
        <div class="ab-media" data-ab-in>
          <a class="ab-media-rating" href="%(maps)s" target="_blank" rel="noopener">
            <span class="ab-circles" aria-hidden="true">
              <span class="ab-circle ph-circle mono">PHOTO 9<br>DÉTAIL</span>
              <span class="ab-circle ph-circle mono">PHOTO 10<br>DÉTAIL</span>
              <span class="ab-circle ph-circle mono">PHOTO 11<br>DÉTAIL</span>
            </span>
            <span class="ab-rating mono">NOTÉ 5,0 / 5 · 43 AVIS GOOGLE</span>
          </a>
          <div class="ab-media-cover">%(ph_cover)s</div>
        </div>
      </div>
    </div>
  </section>

  <section class="ab-values" aria-labelledby="ab-values-p">
    <div class="ab-values-l">%(tooth)s<p id="ab-values-p">Ce qui guide chaque soin</p></div>
    <ul class="ab-values-list">%(values)s</ul>
  </section>

  <section class="ab-feat" aria-label="Nos engagements">
    %(ph_feat)s
    <div class="ab-feat-r">
      <p class="ab-pills mono"><span>PRÉCISION</span><span>DOUCEUR</span></p>
      <ul class="ab-feat-list">%(feats)s</ul>
    </div>
  </section>

  <section class="ab-tech" aria-labelledby="ab-tech-h">
    <div class="ab-tech-c">
      <p class="ab-pills ab-pills-dark mono"><span>PLATEAU</span><span>TECHNIQUE</span></p>
      <h2 id="ab-tech-h">Des salles de soins<br>à la technologie</h2>
      <a class="btn btn-navy btn-big" href="/equipements/">Nos équipements%(orb)s</a>
    </div>
    %(ph_tech)s
    <div class="ab-tech-thumbs" data-ab-thumbs>%(tech_thumbs)s</div>
  </section>

  <section class="ab-team" aria-labelledby="ab-team-h">
    <p class="ab-pills mono"><span>NOTRE</span><span>ÉQUIPE</span></p>
    <h2 id="ab-team-h">Une équipe à votre écoute.</h2>
    <p class="ab-team-p">Les femmes et les hommes du Centre Dentaire Chifaa vous accompagnent du premier rendez-vous au suivi de votre traitement.</p>
    <div class="ab-team-grid">%(team)s
    </div>
  </section>
''' % dict(hero_imgs=hero_imgs, thumbs=thumbs, stats='\n    '.join(stats), cards=cards, specs=specs, maps=B.MAPS, tooth=TOOTH, values=values,
           ring=ring, arrow=ARROW_UR, feats=feats, orb=B.ORB, tech_thumbs=tech_thumbs, team=team_html,
           ph_bento=ph('ab-bento-img', 8, "L'entrée du cabinet", 'PAYSAGE 4:3',
                       "Porte d'entrée ou plaque du cabinet dans l'immeuble El Menzah, pour que les patients reconnaissent les lieux.", attrs=' data-ab-in'),
           ph_cover=ph('ab-cover', 12, "La salle d'attente", 'PAYSAGE 4:3', "Sièges et décoration, pièce vide, lumière naturelle."),
           ph_feat=ph('ab-feat-img', 19, "Le Dr Boukadous au cabinet", 'PORTRAIT 3:4, HAUTE',
                      "Photo verticale en pied ou à mi-corps, dans la salle de soins, tenue de travail, regard caméra. Elle accompagne nos engagements.", tag='figure'),
           ph_tech=ph('ab-tech-main', 20, "Le scanner intra-oral en action", 'PORTRAIT 4:5',
                      "Le scanner en main devant l'écran qui affiche une empreinte 3D. Patient de dos ou hors cadre.", 'dark', attrs=' data-ab-main')) \
        + B.lieu('accueil-cabinet-cdc-meknes.jpg', "").replace(
            '<img class="lieu-bg" src="/assets/img/accueil-cabinet-cdc-meknes.jpg" alt="" loading="lazy" data-lieu-parallax>',
            ph('lieu-bg', 30, "La façade sur l'avenue des FAR", 'PAYSAGE 21:9',
               "Façade de l'immeuble El Menzah prise de jour depuis le trottoir d'en face, entrée bien visible.", 'dark', attrs=' data-lieu-parallax')) \
        + '\n</main>\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "url": B.SITE + path, "name": "Le cabinet – Centre Dentaire Chifaa", "about": B.DENTIST},
        B.crumbs([('Accueil', '/'), ('Le cabinet', path)])]}
    return (path, "Le cabinet | Centre Dentaire Chifaa, dentiste à Meknès",
            "Le Centre Dentaire Chifaa du Dr Taoufik Boukadous, avenue des FAR à Meknès : six spécialités, radiologie 3D sur place et empreinte numérique.",
            'reception-cabinet-cdc-meknes.jpg', ld, body)


# ------------------------------------------------------------------------------------------
# Bloc « Prenez rendez-vous » avec l'anneau de photos qui tourne au scroll (page /blog/)
# Photos libres de droits sur les thèmes de la référence
# ------------------------------------------------------------------------------------------
# anneau : photos libres de droits (CC0, StockSnap et Rawpixel), crédits dans tools/credits-photos.json
RING_IMGS = ['ring-brosse-main.jpg', 'ring-couple.jpg', 'ring-sourire-serviette.jpg', 'ring-sourire.jpg', 'ring-salle-de-bain.jpg', 'ring-brosses-verre.jpg']

def book_ring():
    """Photos dispersées autour du titre ; au scroll elles jaillissent du centre (effet de la page services du Cabinet Chorfi)."""
    imgs = ''.join('<figure class="fl-img fl-%d"><img src="/assets/img/%s" alt="" loading="lazy"></figure>' % (i + 1, f)
                   for i, f in enumerate(RING_IMGS))
    return '''
  <section class="ab-book ab-book-fl" aria-labelledby="ab-book-h" data-fl>
    <div class="fl-imgs" aria-hidden="true">%s</div>
    <div class="ab-book-c">
      <h2 id="ab-book-h">Prenez<br>rendez-vous</h2>
      <a class="ab-link" href="/contact/"><span>Planifier ma visite</span>%s<i aria-hidden="true"></i></a>
    </div>
  </section>
''' % (imgs, ARROW_UR)
