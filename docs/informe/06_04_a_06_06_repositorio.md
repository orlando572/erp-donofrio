# 6.4 a 6.6 Repositorio: resumen de GitHub, ramificación y estrategia de fusión

## 6.4 Resumen del GitHub

El código, la documentación y los flujos de automatización están en un único repositorio público: <https://github.com/orlando572/erp-donofrio> (licencia LGPL-3.0, rama por defecto `develop`). Las cifras son del 25/11/2026.

### Tabla 27. Cifras clave del repositorio

| Elemento | Resultado |
|---|---|
| Ramas | `develop` (integración) y `main` (entregado), ambas protegidas con `lint` y `test` obligatorios |
| Pull requests | 82, todos fusionados (80 a `develop` y 2 a `main`): 43 de Orlando y 39 de Evelyn |
| GitHub Actions | 3 flujos (`CI`, `Release` y `Pruebas no funcionales`) y 199 ejecuciones |
| Releases | 5 con su zip: `v1.0.0` (núcleo), `v1.1.0` (M1), `v1.2.0` (M2), `v1.3.0` (M3) y `v1.4.0` (M4) |
| Paquete (GHCR) | Imagen pública `ghcr.io/orlando572/erp-donofrio`, publicada con cada tag |
| GitHub Project | «Scrum ERP D'Onofrio», público, con 22 ítems (6.3) |
| Issues | 22 (15 épicas y 7 de gestión), con plantillas de épica y de bug |
| Seguridad | *Secret scanning* y *push protection* activos |
| Estructura | Cuatro módulos en `addons/`, `docker/`, `scripts/`, `docs/` y `.github/` con 3 flujos y las plantillas de issue y PR |

De las 192 ejecuciones del flujo `CI`, 165 fueron correctas, 23 se cancelaron porque las reemplazó una corrida más reciente y 4 quedaron en rojo; las 4 las corrigió el propio PR antes de fusionarse, lo que muestra que el control funciona. Las 7 del flujo `Release` fueron correctas: 2 ensayos y 5 publicaciones, una por tag. La corrida más reciente sobre `develop` terminó en verde con 218 pruebas.

## 6.5 Ramificación

El esquema usa ramas de corta vida que parten de `develop` y vuelven a ella por PR:

| Rama | Propósito | Uso real |
|---|---|---|
| `main` | Lo entregado, un tag por release | Recibió 2 PR de release: el núcleo (24/11, `v1.0.0`) y la Fase 2 completa (25/11, `v1.4.0`) |
| `develop` | Integración continua | Base de los 80 PR de trabajo |
| `feature/HU-xx-*` | Una HU | 43 ramas |
| `docs` (prefijo) | Avance del informe y de Scrum | 34 ramas |
| `fix/*`, `chore/*`, `release/*` | Corrección, mantenimiento y paso a `main` | 1, 2 y 2 ramas |

Ninguna rama vive más de unas horas: el proyecto, de la creación del repositorio al cierre de la Fase 2, ocurrió entre el 22 y el 25/11/2026. Las ramas se borran al fusionar.

### Figura 12. Flujograma de ramas

```mermaid
gitGraph
  commit id: "inicializa repo"
  branch develop
  checkout develop
  branch feature/HU-xx
  commit id: "feat HU-xx"
  checkout develop
  merge feature/HU-xx id: "PR con revisión cruzada"
  commit id: "squash de cada PR"
  checkout main
  merge develop id: "release" tag: "v1.0.0"
  checkout develop
  commit id: "M1 a M4"
  checkout main
  merge develop id: "release" tag: "v1.4.0"
```

## 6.6 Merge strategy

Cada PR sale de una rama `feature/*` hacia `develop` con la plantilla de la definición de terminado, recibe la revisión del otro integrante y se fusiona con el CI en verde; `develop` pasa a `main` con tag.

| Punto | Resultado |
|---|---|
| Método a `develop` | 63 *squash* y 17 *merge commit*; desde el PR #184 los 46 restantes son *squash*, un commit por PR |
| Revisión cruzada | 79 de 82 PR (96 %) con aprobación vigente del otro integrante; en los 82 revisó el otro |
| Quién fusiona | 48 los fusionó el otro integrante y 34 su autor, después de la aprobación |
| Aprobación al cambiar el código | Se descarta y hay que aprobar de nuevo: ocurrió en 13 revisiones de 11 PR |
| Conflictos | 10 PR integraron `develop` en su rama (sin *force push*); se concentraron en `__manifest__.py`, `tests/__init__.py`, `ci.yml` y `docs/`, y se resolvieron con cambios aditivos |
| `develop` → `main` | PR #222 (núcleo, *squash*) y PR #229 (Fase 2, *merge commit*) |

El repositorio tiene un solo administrador (Orlando) y la protección de ramas no aplica a administradores (`enforce_admins` desactivado); el equipo lo compensa cumpliendo siempre la revisión cruzada, y los casos en que se fusionó sin aprobación vigente están documentados en 4.3.1.
