# Calibre Clarity : présentation facultative

Ce module est indépendant du thème d'icônes. Il propose un fond blanc uniforme,
une hiérarchie typographique et des pictogrammes dans les détails des livres.
Il ne change ni les livres, ni les métadonnées, ni les réglages de conversion.
Ce n'est ni un plugin ni un installateur. Aucun script n'est à exécuter.

## Ce qui est inclus

- `book_details.css` : la feuille de style, avec ses SVG intégrés.
- Ce guide et sa version anglaise.
- Les licences MIT (CSS) et CC BY 4.0 (dessins de Loic Gridaine).

Les réglages de disposition ci-dessous sont facultatifs et se font dans calibre.
La copie du CSS n'applique pas ces réglages. Le thème d'icônes reste sélectionné
indépendamment dans Apparence et présentation.

## Installer la présentation

1. Décompressez `calibre-clarity-ux.zip`.
2. Dans calibre, ouvrez **Préférences > Avancé > Divers > Ouvrir le répertoire de configuration de calibre**.
3. Gardez ce dossier ouvert, puis quittez complètement calibre.
4. Dans ce dossier de configuration, ouvrez `resources`, puis `templates`.
   Créez ces deux dossiers s'ils n'existent pas.
5. Si `templates` contient déjà `book_details.css`, sauvegardez ce fichier
   ailleurs ou renommez-le `book_details.avant-clarity.css` avant de continuer.
6. Copiez le fichier `book_details.css` du module dans `resources/templates`.
7. Relancez calibre et sélectionnez un livre pour voir sa fiche.

Utilisez le dossier ouvert par calibre, pas celui de l'application ni celui
contenant vos livres. Aucun chemin personnel n'est à modifier dans le CSS.
Il ne faut pas charger ce ZIP dans **Extensions** ou **Changer le thème d'icônes**.

## Régler la disposition, à votre rythme

Avant de changer une valeur, notez sa valeur actuelle ou prenez une capture des
préférences. Modifiez un réglage à la fois. Les libellés peuvent varier selon la
version de calibre et la traduction.

| Élément | Réglage conseillé |
| --- | --- |
| Couleurs | Choisissez une interface claire : cette feuille CSS utilise un fond blanc. |
| Taille du texte | Conservez d'abord la police et la taille du système. Augmentez-les si la lecture reste difficile. |
| Barre d'outils | Dans Apparence et présentation, choisissez des icônes moyennes et gardez leurs libellés visibles au début. |
| Actions fréquentes | Dans Préférences > Barres d'outils et menus, gardez Ajouter, Modifier les métadonnées, Lire, Convertir et Préférences accessibles. Gardez Envoyer vers le périphérique si vous utilisez une liseuse. |
| Tri et recherche | Conservez le champ de recherche et la commande Trier. |
| Panneau de gauche | Ajustez son séparateur pour lire les catégories sans troncature ; environ 230 à 280 pixels est un point de départ, pas une obligation. |
| Grille de couvertures | Activez la grille, affichez les titres, augmentez les couvertures et réduisez l'espacement dans ses préférences. Le nombre de colonnes dépend de votre écran et des panneaux ouverts. |
| Catégories | Dans les options du navigateur d'étiquettes, regroupez les longues listes par lettre initiale si cette option est proposée. |
| Détails des livres | Utilisez la commande de configuration du panneau pour choisir les champs et leur ordre. |

Ordre de départ conseillé pour les détails : titre, auteurs, série, note,
étiquettes, formats, publication, langues, commentaires. Ajoutez les pages si
votre bibliothèque possède déjà ce champ. Ce module ne crée aucune colonne.
Dans la fenêtre Informations, conservez les libellés et champs techniques dont
vous avez besoin ; le CSS ne remplace pas la configuration des champs.

## Revenir en arrière

1. Quittez calibre.
2. Déplacez le `book_details.css` de Clarity hors de `resources/templates`.
3. Si vous aviez un CSS personnel, remettez votre sauvegarde avec le nom exact
   `book_details.css`. Sinon, calibre retrouvera sa présentation intégrée.
4. Relancez calibre.
5. Pour les réglages de disposition modifiés manuellement, rétablissez les
   valeurs que vous aviez notées. Retirer le CSS ne les annule pas.

Les préférences et ressources personnelles sont communes aux bibliothèques
utilisant cette configuration calibre. Le CSS concerne également la fenêtre
d'informations complète, mais pas le lecteur de livres ni le serveur de contenu.
Les styles déjà présents dans certains résumés peuvent influencer le rendu.

Test de référence : calibre 9.13 sur macOS. Windows et Linux ne sont pas encore
validés visuellement. Les mises à jour conservent habituellement ces ressources
personnelles, mais une évolution du HTML ou de Qt peut demander un ajustement.

Documentation officielle :
https://manual.calibre-ebook.com/fr/customize.html#overriding-icons-templates-et-cetera

Projet et assistance : https://github.com/gridaine/calibre-clarity
