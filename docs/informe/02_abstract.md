# 2. Abstract

## Abstract

This paper presents an academic enterprise resource planning (ERP) system for D'Onofrio, a fictitious company of ice cream, chocolates and panettone with a seasonal business, a wide network of street vendors and perishable products. All company data are invented. The case starts from four problems: the vendors' daily settlement is done on paper or in Excel, lots expire without anyone noticing in time, quality and cold-chain checks leave no record tied to the lot, and management decides late and without consolidated data.

The solution is a web ERP built on Odoo 19 Community and PostgreSQL 16, running in Docker and without Enterprise licenses. It was developed with Scrum in two phases. The first one configures standard Odoo through code in the `donofrio_base` module: sales, logistics with lots and first-expired-first-out picking (FEFO), production, management, purchasing, invoicing, human resources and a service desk, with a PostgreSQL replica, backups and a hardened deployment with Nginx and TLS. The second one adds four custom modules: quality inspection with a certificate (`donofrio_calidad`), daily settlement of street vendors (`donofrio_heladeros`), the cold chain with temperature alerts and a management dashboard built with OWL (`donofrio_tablero`).

We completed 115 of the 121 user-story points (95 %), versions `v1.0.0` to `v1.4.0` are published and all 218 automated tests pass in continuous integration. Restoring a backup took 31 seconds (target: two hours); with 20 virtual users, the 95th percentile was 11.6 ms for lists; there were no high-risk security alerts; and the web performance score of the sales dashboard rose from 45 to 80 points. The back end (59) and the custom dashboard (76) stay below the target of 80, a limit explained by Odoo's JavaScript. Measurements come from a single machine with demonstration data.

**Keywords:** Odoo 19; ERP; PostgreSQL; Scrum; Docker.
