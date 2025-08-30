# Base hypernodale et treillis de vues — PaniniFS

But: décrire un modèle de données hypernodal (hypergraphes) avec vues hiérarchiques réutilisables se superposant en treillis, et ses liens avec PI/attribution.

Concepts
- Hypernœud: entité multi-dimensionnelle (contenu, métadonnées, provenance, droits).
- Hyperarcs: relations multi-nœuds, typées (inférence, dérivation, citation, versionnage).
- Vues: arbres contextuels projetés depuis l’hypergraphe; superposables → treillis.
- Treillis: jointures/suprema entre vues pour composer des perspectives.

Propriété intellectuelle & attribution
- Chaque assertion porte provenance (qui/quoi/quand/où) et licence.
- Chaîne d’attribution conservée sur transformations (hyperarcs de dérivation).
- Recherche/affichage filtrables par droits/licences.

PaniniFS: implémentation envisagée
- Schéma logique: tables (nodes, arcs, views, rights, licenses, provenance).
- Indexation par signatures dhātu pour requêtes sémantiques.
- API: CRUD hypernœuds, projections de vues, opérations de treillis (meet/join).

À faire
- Esquisser un schéma SQL minimal (ou graph DB) + exemples de requêtes.
- Définir format d’export/import avec attribution complète.
