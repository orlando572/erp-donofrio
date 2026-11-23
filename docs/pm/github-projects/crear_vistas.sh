#!/usr/bin/env bash
# Crea las 3 VISTAS del GitHub Project "Scrum ERP D'Onofrio" (docs/plan/04 §4.11) con GraphQL (la CLI gh no las soporta).
# Uso: docs/pm/github-projects/crear_vistas.sh <numero_del_project>   (owner: orlando572). Es idempotente por nombre.
# La API no permite configurar la agrupación ni el orden de las vistas: ver README ("Pasos manuales").
set -euo pipefail
OWNER=orlando572
N=${1:?uso: crear_vistas.sh <numero_del_project>}

PID=$(gh project view "$N" --owner "$OWNER" --format json --jq .id)
campo() { gh project field-list "$N" --owner "$OWNER" --format json --jq ".fields[] | select(.name==\"$1\") | .id"; }
existentes() { gh api graphql -f query="{ user(login:\"$OWNER\"){ projectV2(number:$N){ views(first:30){ nodes{ id name } } } } }" --jq '.data.user.projectV2.views.nodes[] | "\(.id)\t\(.name)"'; }

vista() {  # nombre, layout, filtro
  local nombre=$1 layout=$2 filtro=$3 id
  id=$(existentes | awk -F'\t' -v n="$nombre" '$2==n{print $1}')
  if [ -z "$id" ]; then   # reutiliza la vista por defecto "View 1" si aún existe
    id=$(existentes | awk -F'\t' '$2=="View 1"{print $1}')
  fi
  if [ -z "$id" ]; then
    id=$(gh api graphql -f query='mutation($p:ID!,$n:String!,$l:ProjectV2ViewLayout!){ createProjectV2View(input:{projectId:$p,name:$n,layout:$l}){ projectV2View{ id } } }' \
         -f p="$PID" -f n="$nombre" -f l="$layout" --jq .data.createProjectV2View.projectV2View.id)
  fi
  gh api graphql -f query='mutation($v:ID!,$n:String!,$l:ProjectV2ViewLayout!,$f:String){ updateProjectV2View(input:{viewId:$v,name:$n,layout:$l,filter:$f}){ projectV2View{ id } } }' \
     -f v="$id" -f n="$nombre" -f l="$layout" -f f="$filtro" >/dev/null
  echo "vista: $nombre ($layout) filtro='$filtro'"
}

vista "Product Backlog"          TABLE_LAYOUT   "tipo:Épica"
vista "Sprint actual"            BOARD_LAYOUT   "sprint:@current"
vista "Roadmap"                  ROADMAP_LAYOUT ""

# Elimina las vistas de la versión anterior del plan (v1.3), si existen
for v in "Riesgos" "Entregables del informe"; do
  id=$(existentes | awk -F'\t' -v n="$v" '$2==n{print $1}')
  if [ -n "$id" ]; then
    gh api graphql -f query='mutation($v:ID!){ deleteProjectV2View(input:{viewId:$v}){ clientMutationId } }' -f v="$id" >/dev/null
    echo "vista eliminada: $v"
  fi
done
