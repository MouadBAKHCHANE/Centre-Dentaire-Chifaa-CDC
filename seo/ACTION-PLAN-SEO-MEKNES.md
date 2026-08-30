# Plan d'action SEO — « dentiste à Meknès » · Centre Dentaire Chifaa
*Dérivé de l'analyse des 5 concurrents de Rabat (voir ANALYSE-CONCURRENTS-RABAT.md). Priorité aux 6 spécialités : Orthodontie, Implants dentaires, Chirurgie orale, Parodontie, Prothèse dentaire, Pédodontie.*

**Avantage de départ : Meknès est bien moins disputée que Rabat, et le cabinet a déjà un 5,0★ (43 avis) sur Google — aucun des 5 concurrents n'affiche mieux.**

---

## 1. Architecture cible (le modèle dentiste-rabat.net, en propre)

```
/                                   → « dentiste à Meknès » (accueil)
/soins/orthodontie-meknes/          → orthodontiste à Meknès (adultes)
/soins/orthodontie-enfant-meknes/   → orthodontie enfants & ados (page séparée = 2e requête)
/soins/implants-dentaires-meknes/   → implant dentaire Meknès (page phare, déjà votre force)
/soins/chirurgie-orale-meknes/      → chirurgie orale / dents de sagesse / extractions
/soins/parodontie-meknes/           → parodontie / déchaussement / gencives
/soins/prothese-dentaire-meknes/    → prothèse dentaire / couronne / bridge
/soins/pedodontie-meknes/           → dentiste enfant Meknès
/urgences-dentaires-meknes/         → urgence dentiste Meknès (forte intention, cf. 3 concurrents)
/le-cabinet/   /dr-taoufik-boukadous/   /contact/
/blog/…
sitemap.xml + robots.txt propres (2 concurrents sur 5 les négligent et plafonnent)
```

Règles : slug = **spécialité + meknes** ; une page par spécialité, jamais tout sur l'accueil ; le nom du Dr Boukadous visible sur chaque page (E-E-A-T).

## 2. Titles / metas / H1 prêts à coller

| Page | Title (≤ 62 car.) | H1 |
|---|---|---|
| Accueil | `Dentiste à Meknès \| Centre Dentaire Chifaa – Dr Boukadous` | `Dentiste à Meknès — Implants, orthodontie et soins dentaires` |
| Orthodontie | `Orthodontie à Meknès \| Aligneurs & bagues – CDC` | `Orthodontiste à Meknès : aligneurs et traitements adultes` |
| Ortho enfant | `Orthodontie enfant à Meknès \| Enfants & ados – CDC` | `Orthodontie pour enfants et adolescents à Meknès` |
| Implants | `Implant dentaire à Meknès \| All-on-4, devis écrit – CDC` | `Implants dentaires à Meknès : unitaire, All-on-4, greffe` |
| Chirurgie orale | `Chirurgie orale à Meknès \| Dents de sagesse – CDC` | `Chirurgie orale à Meknès : extractions et dents de sagesse` |
| Parodontie | `Parodontie à Meknès \| Gencives & déchaussement – CDC` | `Parodontie à Meknès : soigner gencives et déchaussement` |
| Prothèse | `Prothèse dentaire à Meknès \| Couronnes & bridges – CDC` | `Prothèses dentaires à Meknès : couronnes, bridges, stellites` |
| Pédodontie | `Dentiste enfant à Meknès \| Pédodontie – CDC` | `Pédodontie à Meknès : des soins doux pour les enfants` |
| Urgences | `Urgence dentaire à Meknès \| 05 35 51 69 24 – CDC` | `Urgence dentaire à Meknès : on vous répond vite` |

Meta description type (accueil, ~150 car.) :
`Centre Dentaire Chifaa, dentiste à Meknès (Av. des FAR) : implants, orthodontie, parodontie, pédodontie. Noté 5,0/5 sur Google. Devis écrit avant tout soin. ☎ 05 35 51 69 24`

Chaque page soin : réutiliser le motif `[Spécialité] à Meknès + bénéfice + preuve (5,0★) + appel (tél / rendez-vous)`.

## 3. Contenu des pages money (1 000+ mots, le seuil observé chez les gagnants)

Gabarit par spécialité :
1. H1 avec spécialité + ville, intro qui nomme le Dr et le quartier (Av. des FAR, centre de Meknès).
2. H2 « Qu'est-ce que … » (définition simple), H2 « Pour qui / quand », H2 « Déroulement au cabinet » (cone beam, empreinte numérique, chirurgie guidée = vos vrais différenciateurs), H2 « Tarifs et devis » (devis écrit avant engagement — sans prix inventés), H2 FAQ (3-5 questions réelles reprises du site clair), H2 « Prendre rendez-vous à Meknès ».
3. Variantes sémantiques dans les H2/H3 comme dr-benabdelkrim (ex. page implants : « implantologie Meknès », « All-on-4 », « greffe osseuse ») — sans bourrage.
4. Photos du cabinet réelles avec `alt` descriptif (« pose d'implant au Centre Dentaire Chifaa Meknès »).
5. Maillage : l'accueil lie les 6 pages (le méga-menu le fait déjà) ; chaque page soin lie 2 soins associés + la page urgences + le Dr.

## 4. Schéma JSON-LD (à mettre sur toutes les pages)

Étendre le bloc `Dentist` existant du site clair avec les données réelles :
- `address` complète : Bureau N1, Imm Bureaux El Menzah N5, Av des FAR, Meknès 50000
- `geo` (33.8947626, -5.5497537 — relevé sur votre fiche Maps), `hasMap` (lien maps.app.goo.gl existant)
- `openingHoursSpecification` : Lu–Ve 08:30–18:30, Sa 09:00–14:30
- `telephone` +212 5 35 51 69 24, `aggregateRating` **5.0 / 43** (réel, vérifiable — l'afficher est légitime)
- `availableService` : les 6 spécialités
- Sur chaque page soin : `MedicalProcedure` + `BreadcrumbList`. (Pas de `FAQPage` en attente de résultat enrichi : restreint pour les sites commerciaux depuis 2023 — la FAQ reste utile en contenu.)

## 5. Local d'abord (probablement plus décisif que l'on-page à Meknès)

- **Fiche Google Business** : catégorie principale « Dentiste », services = les 6 spécialités, mêmes NAP (nom/adresse/téléphone) **au caractère près** que le site et Instagram ; photos du cabinet (vous les avez) ; posts réguliers ; continuer à collecter les avis en citant la spécialité (« implant », « orthodontie ») dans les réponses.
- **Citations locales** : Dentisto (déjà), annuaires marocains (Kelio/Pagesjaunes.ma, illicomed, doctori.ma…), toujours le même NAP.
- Le lien « Réserver sur Dentisto » et le wa.me restent — signaux de prise de RDV réels.

## 6. Blog longue traîne (1 article/mois suffit au début)

Sujets calqués sur ce qui marche à Rabat, localisés Meknès :
1. « Implant dentaire à Meknès : prix, étapes, durée » (la requête prix est massive)
2. « Aligneurs ou bagues : que choisir à Meknès ? »
3. « Mon enfant a peur du dentiste : la pédodontie en douceur »
4. « Dents de sagesse : quand faut-il les enlever ? »
5. « Déchaussement des dents : les signes qui doivent alerter »
6. « Hygiène bucco-dentaire pendant le Ramadan » (le sujet local qui performe chez le n°5 de Rabat)
7. « Urgence dentaire à Meknès : que faire en attendant le rendez-vous ? »

## 7. Corrections immédiates sur le site actuel (dark/)

| Priorité | Action |
|---|---|
| 🔴 | Title accueil → `Dentiste à Meknès \| Centre Dentaire Chifaa – Dr Boukadous` (mot-clé exact en tête, comme 4 concurrents sur 5) |
| 🔴 | H1 actuel (« Retrouvez une dentition fixe et durable. ») : garder l'accroche mais ajouter la requête, ex. `Votre dentiste à Meknès, pour une dentition fixe et durable.` |
| 🔴 | Cartes en anglais (« Cosmetic Dentistry », « Restorative Dentistry »…) → passer les H3 en français (Orthodontie, Implants dentaires, Chirurgie orale, Parodontie, Prothèse dentaire, Pédodontie) : Google FR ne classe pas des H3 anglais sur ces requêtes |
| 🔴 | Réintégrer le JSON-LD `Dentist` (présent sur le site clair, absent de dark/) enrichi §4 |
| ⚠️ | Créer `sitemap.xml` + `robots.txt` au déploiement, ajouter `<html lang="fr">` ✅ (déjà), canonical, OG/Twitter tags |
| ⚠️ | `alt` des images : décrire soin + ville ; nommer les fichiers en français si possible |
| ⚠️ | Ajouter un bloc FAQ sur l'accueil (contenu déjà écrit sur le site clair) + section urgences avec le numéro |
| ℹ️ | Le domaine : un `centredentairechifaa.ma` (ou variante avec « meknes ») + GBP fort suffisent — l'EMD aide (2 concurrents) mais n'est pas indispensable |

## 8. Ordre d'exécution conseillé

1. Semaine 1 : title/meta/H1 accueil + cartes en français + JSON-LD + sitemap/robots (§7).
2. Semaines 2–4 : les 6 pages spécialité + urgences (§1–3), une par jour de travail.
3. En continu : GBP + avis (§5), 1 article/mois (§6).
4. Mesure : Search Console dès la mise en ligne ; suivre « dentiste meknes », « implant dentaire meknes », « orthodontiste meknes », « dentiste enfant meknes », « urgence dentaire meknes ».
