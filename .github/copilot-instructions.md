# Instructions Copilot - Panini-FS

📍 **CONTEXTE LOCAL :** Tu te trouves actuellement dans le sous-module `modules/core/filesystem`.
**Mission stricte :** Moteur de décomposition sémantique FUSE3 (Rust/Python).

⚠️ **RÈGLES D'ANTI-DÉBORDEMENT :**
- Gère le stockage FUSE3 et la décomposition sémantique bas niveau.
- Ne recrée jamais une logique qui appartient à un autre module de l'écosystème.
- Ce module interagit avec le reste de l'écosystème via des interfaces claires.

🗺️ **CARTOGRAPHIE DE L'ÉCOSYSTÈME PANINI :**
1. **Hub/Orchestrateur** (Racine) : Lien entre les modules. Ne contient que l'orchestration (`src/panini_colabmcp`).
2. **Panini-FS** (`modules/core/filesystem`) : Stockage FUSE3.
3. **Panini-SemanticCore** (`modules/core/semantic`) : Extraction dhātu.
4. **OntoWave** (`modules/ontowave`) : UX et UI.
5. **Panini-AttributionRegistry** (`modules/data/attribution`) : Traçabilité et provenance.
6. **Panini-AutonomousMissions** (`modules/missions/autonomous`) : Workflows IA.
7. **Panini-PublicationEngine** (`modules/publication/engine`) : Formatage/Export.
8. **Panini-UltraReactive** (`modules/reactive/ultra-reactive`) : Streaming temps réel.
9. **Panini-CloudOrchestrator** (`modules/orchestration/cloud`) : Infra et Déploiement.
10. **Panini-Research** (`research`): Laboratoire de recherche fondamentale — noyau iso (moteur) + NIPADA (couche descriptive et produit).

🔗 **RÈGLES GLOBALES :**
Le submodule `copilotage/` est présent dans ce dépôt et contient les directives partagées de l'écosystème Panini.
- **Journal de bord :** ce dépôt tient son propre journal dans `docs/journal-de-bord/YYYY-MM-DD.md`. Consulter `copilotage/regles/REGLES_JOURNAL_v1.md` pour les règles complètes.
- **Règles d'autonomie et de copilotage :** `copilotage/regles/REGLES_COPILOTAGE_v0.0.2.md`
- **Avant tout commit :** créer/mettre à jour `docs/journal-de-bord/$(date +%Y-%m-%d).md` puis stager le fichier.
- **Anti-ASCII :** Interdiction absolue de l'ASCII art. Utiliser diagram-as-code (Mermaid, Kroki) ou SVG externalisé (fichier `.svg` séparé, référencé via `![description](path.svg)`). Pas de SVG inline/embeddé.

## Règles spécifiques à ce module

### Base Dolt = cache calculé

La base de données Dolt (`panini-unified-db`, `panini-concepts-db`) est un
**cache calculé**, pas du capital accumulé. Elle est entièrement reconstructible
via le pipeline déterministe. Ne pas traiter les fichiers `.dolt/` comme précieux.

### Ontologie à 4 catégories

Le système d'atomes couvre 4 catégories ontologiques :
- **ENT** (entités) — objets, substances
- **PROC** (processus) — actions, événements, émotions
- **QUAL** (qualités) — propriétés, attributs
- **ABS** (abstraits) — relations, structures, mesures

Tout nouvel atome doit être mappé dans les 6 dictionnaires de
`import_panlang_v2.py` : ATOM_DIMENSIONS, ATOM_NSM, ATOM_JACKENDOFF,
ATOM_PUSTEJOVSKY, ATOM_DHATU, et ATOM_KEYWORDS dans
`gutenberg_multilingual_validator.py`.



---

## 🧭 Architecture sémantique Panini — deux niveaux, jamais confondus

- **Noyau (iso)** = moteur rigide / mathématique : 14 atomes V14 (encodage leibnizien), 9 dhātus, logique trinaire Ł3 (exacte — pas du flou), TrinarySAT, DTP, graphe = tissu computationnel. Il **infère** (directement ou par réalités émergentes), il est déterministe ; il **ne décrit jamais** aucun corpus.
- **NIPADA — couche descriptive** = encyclopédie en logique floue (Zadeh, poids [0,1]) : graphe encyclopédique de métadonnées, graphe de transmission généalogico-culturel, corpus. Elle **décrit la réalité observable** et fournit les paramètres que le noyau n'infère pas (régime descriptif R4 : fiction, oral, presse…).
- **NIPADA — produit** = instanciation complète du noyau dans le langage naturel : **noyau + couche descriptive** (le produit contient les deux niveaux).
- **Principe de séparation** : *le noyau ne décrit jamais — il infère ; NIPADA décrit ce que le noyau ne peut inférer.* Mêmes atomes et opérateurs aux deux niveaux ; seule la **source des paramètres** diffère (inférence vs description).
- **Versionnement couplé** : un noyau n'est testable qu'à travers sa NIPADA — on teste le couple **Kᵢ + NIPADAᵢ**, jamais un noyau seul (les corpus signés v271, v272… sont des versions de la couche descriptive).
- Vocabulaire figé : « NIPADA en logique floue » désigne **uniquement la couche descriptive** (niveau 2) ; Ł3 ≠ flou ; trois usages du flou (Zadeh pragmatique / Ł3 moteur / poids du graphe) = **un seul système** à décrire comme tel.
- Référence canonique : `PaniniResearch/Panini-Research` → `docs/ARCHITECTURE_NOYAU_NIPADA_v1.0.md` (dérivée de `philosophy-theory/DOCUMENT_DE_CONTEXTE_v2.0.md` §2.1).
