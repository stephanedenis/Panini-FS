#!/usr/bin/env bash
set -euo pipefail

# PR Auto-Doctor: diagnose -> fix docs FR/EN sync -> push -> wait checks -> merge
# Requires: gh, jq, git
# Usage examples:
#  - ./scripts/devops/pr_auto_doctor.sh diagnose --pr 39
#  - ./scripts/devops/pr_auto_doctor.sh fix-docs-sync --pr 39
#  - ./scripts/devops/pr_auto_doctor.sh wait-checks --pr 39 --check "Docs Governance"
#  - ./scripts/devops/pr_auto_doctor.sh merge --pr 39 --method squash --auto
#  - ./scripts/devops/pr_auto_doctor.sh full --pr 39 -y   # end-to-end without prompts

confirm() {
  if [[ "${ASSUME_YES:-0}" == "1" ]]; then
    return 0
  fi
  read -r -p "$1 [y/N]: " resp
  [[ "$resp" =~ ^[Yy]$ ]]
}

usage() {
  cat <<'EOF'
PR Auto-Doctor

Commands:
  diagnose                 Affiche l'état des checks et le diff ciblé docs/
  fix-docs-sync            Corrige la synchro FR/EN (placeholders, nettoyage EN mal nommés)
  wait-checks              Attend un check donné (ou l'ensemble) et renvoie l'état
  merge                    Fait la fusion du PR si vert (squash par défaut)
  full                     Enchaîne: diagnose -> fix-docs-sync -> push -> wait -> merge

Common flags:
  --pr <num>               Numéro du PR à traiter
  -y                       Sans confirmation (non-interactif)
  --check <name>           Nom du workflow à attendre (par défaut: Docs Governance)
  --method <m>             merge | squash | rebase (par défaut: squash)
EOF
}

require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 2; }; }

get_pr_info() {
  local pr="$1"
  gh pr view "$pr" --json number,headRefName,baseRefName,author,title --jq '{number, head: .headRefName, base: .baseRefName, author: .author.login, title}'
}

list_changed_docs() {
  local base_ref="$1"; local head_ref="$2"
  git --no-pager diff --name-only "origin/${base_ref}...origin/${head_ref}" | grep '^docs/' || true
}

# Compute FR<->EN peer path
peer_path() {
  local f="$1"
  if [[ "$f" == docs/en/* ]]; then
    echo "${f/docs\/en\//docs/}"
  else
    local base=${f#docs/}
    echo "docs/en/${base}"
  fi
}

is_markdown() { [[ "$1" == *.md ]]; }

fix_docs_sync() {
  local base_ref="$1"; local head_ref="$2"; local interactive="$3"
  local changed; changed="$(list_changed_docs "$base_ref" "$head_ref")"
  local actions=()

  # 1) Créer les pairs manquants (placeholders minimalistes)
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    is_markdown "$f" || continue
    local peer; peer="$(peer_path "$f")"
    if [[ ! -f "$peer" ]]; then
      actions+=("create:$peer")
    fi
  done <<<"$changed"

  # 2) Nettoyer EN mal nommés (FR slugs dans /en/)
  local en_bad=(
    "docs/en/research/compression-semantique.md"
    "docs/en/research/inventaire-dhatu-v0-1.md"
    "docs/en/research/langage-humain-developpement.md"
    "docs/en/research/universaux-semantique.md"
  )
  for f in "${en_bad[@]}"; do
    if [[ -f "$f" ]]; then actions+=("delete:$f"); fi
  done

  # Exécuter
  for act in "${actions[@]}"; do
    IFS=":" read -r kind path <<<"$act"
    case "$kind" in
      create)
        if confirm "Créer placeholder: $path ?"; then
          mkdir -p "$(dirname "$path")"
          printf '# Placeholder\n\nPeer for `%s`.\n' "${path/docs\/en\//docs/}" > "$path"
          git add "$path"
        fi
        ;;
      delete)
        if confirm "Supprimer EN mal nommé: $path ?"; then
          git rm -f "$path"
        fi
        ;;
    esac
  done

  if git diff --cached --quiet; then
    echo "Aucune modification à valider."
  else
    if confirm "Valider les changements ?"; then
      git commit -m "docs(auto-doctor): fix FR/EN sync placeholders and EN cleanup"
    fi
  fi
}

wait_workflow() {
  local head_ref="$1"; local name="${2:-Docs Governance}"
  require_cmd jq
  local run_id
  run_id=$(gh run list --json databaseId,name,headBranch,status,conclusion \
    --jq ".[] | select(.name==\"${name}\" and .headBranch==\"${head_ref}\") | .databaseId" | head -n1)
  if [[ -z "$run_id" ]]; then
    echo "Aucun run trouvé pour ${name} sur ${head_ref}"; return 1
  fi
  echo "Attente du run #$run_id (${name})..."
  # Poll simple
  while true; do
    local state
    state=$(gh run view "$run_id" --json status,conclusion --jq '{status,conclusion}') || true
    local st; st=$(echo "$state" | jq -r .status)
    local co; co=$(echo "$state" | jq -r .conclusion)
    echo "status=$st conclusion=$co"
    if [[ "$st" == "completed" || "$st" == "COMPLETED" ]]; then
      if [[ "$co" == "success" || "$co" == "SUCCESS" ]]; then return 0; else return 1; fi
    fi
    sleep 5
  done
}

merge_pr() {
  local pr="$1"; local method="${2:-squash}"; local auto_flag="${3:-0}"
  local args=("--${method}" "--delete-branch")
  if [[ "$auto_flag" == "1" ]]; then args+=("--auto"); fi
  gh pr merge "$pr" "${args[@]}"
}

main() {
  [[ $# -lt 1 ]] && usage && exit 1
  local cmd="$1"; shift
  local pr=""; local check_name="Docs Governance"; local method="squash"; ASSUME_YES=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --pr) pr="$2"; shift 2;;
      --check) check_name="$2"; shift 2;;
      --method) method="$2"; shift 2;;
      -y|--yes) ASSUME_YES=1; shift;;
      *) echo "Arg inconnu: $1"; usage; exit 1;;
    esac
  done

  require_cmd gh; require_cmd git
  [[ -z "$pr" ]] && { echo "--pr est requis"; exit 1; }
  local info; info="$(get_pr_info "$pr")"
  local head; head=$(echo "$info" | jq -r .head)
  local base; base=$(echo "$info" | jq -r .base)

  case "$cmd" in
    diagnose)
      echo "PR $pr -> head=$head base=$base"
      echo "Fichiers docs modifiés:"; list_changed_docs "$base" "$head" || true
      gh pr view "$pr" --json statusCheckRollup --jq '.statusCheckRollup[] | {name:.name,status:.status,conclusion:.conclusion}' || true
      ;;
    fix-docs-sync)
      git fetch origin "$base" "$head" --quiet
      fix_docs_sync "$base" "$head" 1
      if ! git diff --quiet; then echo "Untracked changes présents (non staged)."; fi
      if confirm "Pousser sur $head ?"; then
        git push origin HEAD:"$head"
      fi
      ;;
    wait-checks)
      wait_workflow "$head" "$check_name"
      ;;
    merge)
      merge_pr "$pr" "$method" 1
      ;;
    full)
      echo "[1/4] Diagnose"; $0 diagnose --pr "$pr"
      echo "[2/4] Fix docs sync"; git fetch origin "$base" "$head" --quiet; fix_docs_sync "$base" "$head" 1
      if confirm "Push corrections sur $head ?"; then git push origin HEAD:"$head"; fi
      echo "[3/4] Wait checks (${check_name})"; wait_workflow "$head" "$check_name" || { echo "Checks en échec"; exit 1; }
      echo "[4/4] Merge"; merge_pr "$pr" "$method" 1
      ;;
    *) usage; exit 1;;
  esac
}

main "$@"
