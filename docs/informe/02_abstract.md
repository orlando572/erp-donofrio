# 2. Abstract

## Abstract

This paper presents an academic enterprise resource planning (ERP) system for D'Onofrio, a fictitious seasonal company of ice cream, chocolates and panettone with a wide network of street vendors. All data are invented. The case starts from four problems: vendor settlement on paper, lots that expire unnoticed, quality and cold-chain checks without a record tied to the lot, and late decisions without consolidated data.

The solution is a web ERP built on Odoo 19 Community and PostgreSQL 16, running in Docker and without Enterprise licenses. It was developed with Scrum in two phases. The first one configures standard Odoo through code in the `donofrio_base` module: sales, logistics with lots and first-expired-first-out picking (FEFO), production, purchasing, invoicing, human resources and a service desk, with a PostgreSQL replica, backups and a hardened Nginx and TLS deployment. The second one adds four custom modules: quality inspection with a certificate (`donofrio_calidad`), daily settlement of street vendors (`donofrio_heladeros`), the cold chain with temperature alerts and a management dashboard built with OWL (`donofrio_tablero`).

We completed 115 of 121 user-story points (95 %), versions `v1.0.0` to `v1.4.0` are published and all 218 automated tests pass. A backup restored in 31 seconds (target: two hours); with 20 virtual users the 95th percentile was 11.6 ms; there were no high-risk security alerts; and the sales dashboard score rose from 45 to 80. The back end (59) and the custom dashboard (76) stay below the target of 80, a limit of Odoo's JavaScript. Measurements come from a single machine with demonstration data.

**Keywords:** Odoo 19; ERP; PostgreSQL; Scrum; Docker.
