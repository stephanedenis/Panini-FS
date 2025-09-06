# Empreintes de patterns et pièges de récursion — PaniniFS

But: décrire un système d’empreintes (fingerprints) pour détecter motifs sémantiques, éviter récursions pathologiques, et outiller la déduplication intelligente.

Empreintes (idées)
- Hash sémantique: basé sur signatures dhātu + structure relationnelle, pas sur bytes bruts.
- Locality-sensitive hashing (LSH) pour proximité conceptuelle.
- Fingerprint multi-couches: contenu, provenance, vue (contexte), opération.

Pièges de récursion
- Self-reference cycles dans hypergraphes (ex: citation circulaire).
- Re-écritures infinies (transformations non contractantes).
- Détection: graphe de dérivations acyclique exigé par types d’arcs, seuils de profondeur.

Applications
- Déduplication de concepts/documents à niveau sémantique.
- Alerte boucles (pipeline de publication/ETL).
- Sécurité: éviter amplification involontaire de biais.

À faire
- Prototyper un fingerprint dhātu sur petits exemples.
- Règles anti-récursion (types d’arcs, depth limit, tarjan SCC).
