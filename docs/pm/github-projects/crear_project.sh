#!/usr/bin/env bash
# Crea los CAMPOS del GitHub Project "Scrum ERP D'Onofrio" (docs/plan/04 §4.11) con la CLI gh.
# Requiere el permiso `project` del token:  gh auth refresh -s project
# Uso: docs/pm/github-projects/crear_project.sh <numero_del_project>   (el owner es orlando572)
# El Project se creó con:
#   gh project create --owner orlando572 --title "Scrum ERP D'Onofrio"
#   gh project link <n> --owner orlando572 --repo orlando572/erp-donofrio
#   gh project edit <n> --owner orlando572 --visibility PUBLIC
set -euo pipefail
OWNER=orlando572
N=${1:?uso: crear_project.sh <numero_del_project>}

PID=$(gh project view "$N" --owner "$OWNER" --format json --jq .id)
STATUS_ID=$(gh project field-list "$N" --owner "$OWNER" --format json --jq '.fields[] | select(.name=="Status") | .id')

# Status: reemplaza las opciones por defecto (Todo / In Progress / Done) por las del plan
gh api graphql -f query='
mutation($f:ID!){ updateProjectV2Field(input:{fieldId:$f, singleSelectOptions:[
  {name:"Backlog",     color:GRAY,   description:"Aún sin planificar en un sprint"},
  {name:"Por hacer",   color:BLUE,   description:"Planificado en el sprint"},
  {name:"En curso",    color:YELLOW, description:"En desarrollo"},
  {name:"En revisión", color:ORANGE, description:"PR o documento esperando la revisión del otro integrante"},
  {name:"Hecho",       color:GREEN,  description:"Cumple la Definition of Done"}]}){ projectV2Field{ ... on ProjectV2SingleSelectField{ id } } } }' -f f="$STATUS_ID" >/dev/null

gh project field-create "$N" --owner "$OWNER" --name "Puntos"      --data-type NUMBER >/dev/null
gh project field-create "$N" --owner "$OWNER" --name "Responsable" --data-type SINGLE_SELECT --single-select-options "Evelyn,Orlando" >/dev/null
gh project field-create "$N" --owner "$OWNER" --name "Fase"        --data-type SINGLE_SELECT --single-select-options "F1,F2" >/dev/null
gh project field-create "$N" --owner "$OWNER" --name "Tipo"        --data-type SINGLE_SELECT --single-select-options "Épica,Gestión,Bug" >/dev/null
gh project field-create "$N" --owner "$OWNER" --name "Prioridad"   --data-type SINGLE_SELECT --single-select-options "Must,Should,Could" >/dev/null

# Sprint: campo de tipo Iteración (la CLI no lo soporta; se crea con GraphQL).
# Cada iteración dura ~1 día (timebox del plan). Las fechas son provisionales: se ajustan a las fechas reales de ejecución.
gh api graphql -f query='
mutation($p:ID!){ createProjectV2Field(input:{projectId:$p, dataType:ITERATION, name:"Sprint",
  iterationConfiguration:{startDate:"2026-11-22", duration:1, iterations:[
    {title:"S0",     startDate:"2026-11-22", duration:1},
    {title:"S1",     startDate:"2026-11-23", duration:1},
    {title:"S2",     startDate:"2026-11-24", duration:1},
    {title:"S3",     startDate:"2026-11-25", duration:1},
    {title:"S4",     startDate:"2026-11-26", duration:1},
    {title:"Cierre", startDate:"2026-11-27", duration:1}]}}){ projectV2Field{ ... on ProjectV2IterationField{ id } } } }' -f p="$PID" >/dev/null

echo "Campos creados en el Project $N"
