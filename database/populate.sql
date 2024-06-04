INSERT INTO bvbv (name) VALUES 
('bien vivre, bien vieillir'), 
('bien vivre'), 
('bien vieillir'),
('Aucune information');



INSERT INTO branches (name) VALUES 
('indépendence'),
('environnement'),
('informations générales'),
('Aucune information');



INSERT INTO sub_branches (name) VALUES 
('mobilité'),
('capacité de travail / éducation et comprétences'),
('sécurité'),
('environnement domestique'),
('resources financières'),
('soins de santé et soins sociaux'),
('environnement physique'),
('infrastructure'),
('niveau d''urbanisme'),
('adresse'),
('population'),
('Aucune information');

INSERT INTO branches_sub_branches (id_branches, id_sub_branches) VALUES 
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(3, 10),
(3, 11);


INSERT INTO precision (name) VALUES
('aspect précis'),
('mobilité professionnel'),
('programmes et ressources'),
('pollution'),
('bruit'),
('espaces extérieurs'),
('transport'),
('eau potable'),
('gaz'),
('reseaux d''assainissement'),
('météo'),
('Aucune information');



INSERT INTO region (name) VALUES
('Landes'),
('France'),
('Nouvelle-Aquitaine'),
('Brocas'),
('Toulouse'),
('Dax'),
('Garein'),
('Aucune information');



INSERT INTO urls (url) VALUES
('https://www.pigma.org/fr/dataset/datasets/4600/resource/10225/download/'),
('https://www.pigma.org/fr/dataset/datasets/7421/resource/15101/download/'),
('https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/logements-et-logements-sociaux-dans-les-departements/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B'),
('https://www.data.gouv.fr/fr/datasets/repertoire-des-logements-locatifs-des-bailleurs-sociaux/'),
('https://www.insee.fr/fr/recherche/recherche-statistiques?q=parc+locatif+social&debut=0&categorie=5'),
('https://www.data.gouv.fr/fr/datasets/etablissements-ehpad-esld-residences-autonomie-accueils-de-jour/#/resources'),
('https://www.data.gouv.fr/fr/datasets/laccessibilite-potentielle-localisee-apl/#/resources'),
('https://opendata.atmo-na.org/geoserver/alrt_nouvelle_aquitaine/wfs?request=GetFeature&service=WFS&version=1.1.0&typeName=alrt_nouvelle_aquitaine:alrt_nouvelle_aquitaine&outputFormat=csv'),
('https://www.data.gouv.fr/fr/datasets/accessibilite-des-traversees-pietonnes-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/niveau-daccessibilite-des-cheminements-pietons-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/cheminements-retrecis-pour-pietons-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/obstacles-lineaires-sur-les-cheminements-pietons-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/accessibilite-des-grilles-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/accessibilite-des-cheminements-non-lineaire-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/accessibilite-autour-des-etablissements-recevant-du-public-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/dispositif-dinformation-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/ressauts-non-conforme-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/qualite-du-revetement-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://www.data.gouv.fr/fr/datasets/escaliers-accessible-ou-non-accessible-diagnostique-accessibilite-2014-toulouse-metropole/'),
('https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/sanisettes/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B'),
('https://www.pigma.org/public/opendata/nouvelle_aquitaine_mobilites/publication/landes-aggregated-gtfs.zip'),
('https://www.pigma.org/public/opendata/nouvelle_aquitaine_mobilites/publication/naq-aggregated-gtfs.zip'),
('https://catalogue.sigena.fr:443/geonetwork/srv/api/records/a3791ce8-a36e-431b-b832-48e3fd18587f/attachments/gisements_fonciers_40.zip'),
('https://beta.pigma.org/fr/dataset/datasets/76/resource/280/download/'),
('https://www.insee.fr/fr/statistiques/fichier/3698339/base-pop-historiques-1876-2021.xlsx');



INSERT INTO sources (name) VALUES
('ADACL'),
('landes.gouv.fr'),
('SDIS DES LANDES'),
('pigma'),
('DDTM DES LANDES'),
('opendata.caissedesdepots.fr'),
('Ministère de la Transition écologique'),
('Insee'),
('Lou Dupont'),
('ARS NOUVELLE AQUITAINE'),
('Ministère des Solidarités et de la Santé'),
('Open data Atmo'),
('UNIVERSITE BORDEAUX 3'),
('Atmo'),
('catalogue.geo-ide.developpement-durable.gouv.fr'),
('toilettespubliques.net'),
('Toulouse métropole'),
('Département de Landes'),
('Open Data Commons (ODbL)'),
('GIP ATGERI'),
('DREAL NOUVELLE-AQUITAINE'),
('Aucune information');


INSERT INTO datasets (id_bvbv, id_branches, id_sub_branches, id_precision, name, id_sources, id_region, id_urls)
VALUES
    (1, 2, 3, NULL, 'Landes : SAIP (implantation sirènes)', 2, 1, 1),
    (1, 2, 3, NULL, 'landes - Postes d''appel d''urgence', 4, 1, 2),
    (1, 2, 4, NULL, 'Logements et logements sociaux dans les départements', 6, 2, 3),
    (1, 2, 4, NULL, 'Répertoire des logements locatifs des bailleurs sociaux', 7, 2, 4),
    (1, 2, 4, NULL, 'Répertoire du parc locatif social (RPLS)', 8, 2, 5),
    (3, 2, 4, 3, 'Etablissements EHPAD, ESLD, résidences autonomie, accueils de jour', 9, 2, 6),
    (1, 2, 6, NULL, 'landes - Postes d''appel d''urgence', 4, 1, 2),
    (1, 2, 6, NULL, 'L''accessibilité potentielle localisée (APL)', 11, 2, 7),
    (1, 2, 7, 4, 'Episodes de pollution pour les départements de Nouvelle-Aquitaine pour l''année dernière et jusqu''à la veille', 12, 3, 8),
    (3, 2, 7, 6, 'Accessibilité des Traversées Piétonnes - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 9),
    (3, 2, 7, 6, 'Niveau d''accessibilité des cheminements piétons - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 10),
    (3, 2, 7, 6, 'Cheminements rétrécis pour piétons - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 11),
    (3, 2, 7, 6, 'Obstacles linéaires sur les cheminements piétons - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 12),
    (3, 2, 7, 6, 'Accessibilité des grilles - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 13),
    (3, 2, 7, 6, 'Accessibilité des cheminements non linéaire - Diagnostique accessibilité 2014 Toulouse Métropole7', 17, 5, 14),
    (3, 2, 7, 6, 'Accessibilité autour des établissements recevant du public - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 15),
    (3, 2, 7, 6, 'Dispositif d''information - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 16),
    (3, 2, 7, 6, 'Ressauts non conforme - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 17),
    (3, 2, 7, 6, 'Qualité du revêtement - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 18),
    (3, 2, 7, 6, 'Escaliers accessible ou non accessible - Diagnostique accessibilité 2014 Toulouse Métropole', 17, 5, 19),
    (3, 2, 7, 6, 'Sanisettes - Toulouse', 17, 5, 20),
    (1, 2, 8, 7, 'Offre de transport - Landes', 4, 1, 21),
    (1, 2, 8, 7, 'Arrêts, horaires et parcours théoriques des réseaux de transport public des membres du syndicat Nouvelle-Aquitaine Mobilités', 19, 3, 22),
    (2, 2, 9, NULL, 'Landes : foncier potentiellement disponible dans les zones déjà urbanisées des communes', 21, 1, 23),
    (1, 3, 10, NULL, 'Base adresse locale de la commune de Garein', 1, 7, 24),
    (1, 3, 11, NULL, 'Historique des populations communales', 8, 2, 25);