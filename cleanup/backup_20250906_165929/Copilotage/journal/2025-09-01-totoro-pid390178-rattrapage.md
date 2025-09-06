# Journal de rattrapage — Copilotage

- Date: 2025-09-01T22:20:56-04:00
- Hôte: totoro
- PID: 390178
- Branche: docs/research-bootstrap
- Portée: conversations et décisions non consignées entre 2025-08-30 et 2025-09-01

## Résumé exécutif

- Publications: pipeline stabilisé (MkDocs strict, i18n, Kroki, Leanpub). Génération PDF via Pandoc/Playwright, fallback wkhtmltopdf et HTML.
- reMarkable: automatisation build+push locale (openSUSE); création/gestion collection "Panini"; rafraîchissement par HUP et restart app; scripts SSH non-interactifs.
- Problème persistant: la collection "Panini" s’affiche vide sur l’UI malgré documents présents et parent=collection; essais de réparation/migration effectués; décision de pause.

## Décisions clés

1) Remplacer redémarrage appareil par refresh doux (SIGHUP) ou restart xochitl uniquement.
2) Forcer métadonnées modifiées (modified/metadatamodified=true, lastModified ms).
3) Créer/assurer .content pour les collections.
4) Ajouter outils de réparation: re-parenting, attach par nom, migration clone vers collection (+option delete-old).
5) Mettre la piste tablette en pause pour éviter pertes de temps; journaliser et pivoter.

## Actions réalisées

- Ajout `tools/build_and_push_remarkable.sh` (pipeline local openSUSE). 
- Amélioration `tools/setup_remarkable_ssh.sh` (clé ed25519, alias, BatchMode).
- Renforcement `tools/remarkable_push.py` (collection, refresh hup/restart, diagnostics, repair/migrate, ensure .content, timestamps).
- CI publications: artifacts incluent PDFs/HTML et manuscrits; logs plus verbeux.

## Commandes/flows principaux

- publications: `python publications/build_pdfs.py` (pandoc→pdf | pandoc→html→playwright | html fallback | python-markdown)
- push: `python tools/remarkable_push.py --refresh hup --collection Panini publications/out/*.pdf`
- repair: `--repair-panini`, `--attach-local-out`, `--migrate-root-to-collection [--delete-old]`
- refresh: HUP (soft) ou `systemctl restart xochitl`

## État restant / blocants

- UI reMarkable n’affiche pas le contenu de "Panini" malgré: parent correct, .content présent, refresh app; hypothèse cache/index.
- Prochaine passe: inspection sur-device des .metadata concernés, flush thumbnails/cache minimal, cycle stop/start contrôlé.

## Références internes

- `Copilotage/COPILOTAGE_WORKFLOW.md`
- `Copilotage/AGENT_CONVENTION.md`
- Journaux du 2025-08-30 (anciennes références docs_new désormais sous docs/)

## Checklist Copilotage

- [x] Rattrapage consigné
- [x] Décisions clés listées
- [x] Commandes/flows notés
- [ ] Issue/PR de suivi (optionnel)
