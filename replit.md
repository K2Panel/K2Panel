# aaPanel - لوحة تحكم الخادم

## Overview
aaPanel is a powerful server management control panel built with Python/Flask. It provides a graphical web interface for easy server administration, aiming to be a robust, multi-environment solution for both development (Replit) and production (VPS). Key capabilities include multi-database support (SQLite, MySQL, PostgreSQL), advanced security features, and a scalable architecture. The project's vision is to simplify server management for a wide range of users, from developers to system administrators, leveraging its flexibility and open-source nature to capture a significant market share.

## User Preferences
### متطلبات التوثيق
- يجب تحديث حالة كل مهمة فور إنجازها
- توثيق واضح لما تم إنجازه وما تبقى
- تمكين الفريق من معرفة نقطة التوقف ونقطة الاستكمال
- 🔴 **إلزامي:** مراجعة `تقارير_مراجعة_ارشكتر.md` قبل البدء بأي مهمة

### التواصل
- **اللغة المفضلة**: العربية فقط في جميع الردود
- التوثيق يجب أن يكون واضح ومفصل

### 🔴 ملف تقارير Architect (إلزامي)
**جميع الوكلاء يجب أن:**
1. ✅ يقرأوا `تقارير_مراجعة_ارشكتر.md` قبل البدء
2. ✅ يحدثوا الملف عند حل أي مشكلة
3. ✅ يضيفوا مشاكل جديدة يكتشفها Architect
4. ✅ يوثقوا طريقة الحل والسبب

**الملف يحتوي على:**
- 10 مشاكل مكتشفة من مراجعة Architect الشاملة
- 1 محلولة (10%)، 9 تحتاج حل (90%)
- خطة عمل مفصلة لحل المشاكل المتبقية

## System Architecture
The project uses Python 3.12 and the Flask framework, served with Gunicorn in production. Core architectural decisions include a Factory Pattern for configuration management, an environment detector for runtime identification (Replit or VPS), and a validator for configuration.

**Key Architectural Features:**
-   **Multi-Environment Support:** Distinct configurations for Development (Replit, SQLite) and Production (VPS, external MySQL/PostgreSQL, Nginx, systemd).
-   **Configuration Management:** Dynamic settings loading via `BaseConfig`, `DevelopmentConfig`, and `ProductionConfig`.
-   **Environment Detection:** Automatic detection of Replit vs. VPS environments.
-   **Containerization:** Multi-stage `Dockerfile` with Gunicorn and `GeventWebSocketWorker`. Docker Compose for orchestration with PostgreSQL and Redis. Blue-Green deployment strategy for zero-downtime deployments.
-   **UI/UX:** Graphical web interface for server management.
-   **Security:** Enforces `SECRET_KEY`, supports SSL/TLS, and uses `.dockerignore`. Includes system hardening, firewall setup, and Fail2Ban integration.
-   **Nginx Configuration:** Comprehensive Nginx setup for HTTPS, WebSocket proxying, security headers, rate limiting, and performance optimizations. A+ SSL rating with Let's Encrypt integration.
-   **systemd Integration:** Advanced `systemd` unit file (`aapanel.service`) for managing Gunicorn in production as a non-root user, with robust restart policies and security hardening.
-   **CI/CD Pipeline:** GitHub Actions for automated testing (pytest, coverage, security scanning), linting/formatting, multi-platform Docker image builds, and automated Blue-Green deployments to VPS, including rollback and health checks.
-   **Database Migrations:** Alembic and Flask-Migrate for managing database schema changes with validation.
-   **Database Backup Strategy:** Comprehensive backup system for SQLite, PostgreSQL, and MySQL, featuring automatic scheduling, integrity verification, and security measures (SHA-256 + HMAC).
-   **Monitoring & Alerting:** Health & Readiness Endpoints (`/health/live`, `/health/ready`, `/health/metrics`) for probes and Prometheus metrics. Integrated with Prometheus and Grafana for visualization. Alerting system via Prometheus Alertmanager with 11 alert rules, notifications via Slack and Email.
-   **Centralized Logging:** Grafana Loki and Promtail for centralized log aggregation. Features structured JSON logging, 7-day retention, and a comprehensive Grafana dashboard.
-   **Developer Documentation:** `CONTRIBUTING.md` and `DEVELOPER_GUIDE.md` for clear bilingual guidance on coding standards, Git workflow, and project setup.
-   **Database Connection Pooling:** Integration of DatabaseConnectionPool with retry logic and pool statistics.

## External Dependencies
-   **Web Server:** Gunicorn
-   **Databases:** SQLite, MySQL, PostgreSQL
-   **Database Drivers:** `PyMySQL`, `psycopg2`
-   **Reverse Proxy/Web Server:** Nginx
-   **Process Management:** systemd
-   **Containerization:** Docker
-   **Caching/Message Broker:** Redis
-   **SSL Certificate Management:** Certbot (Let's Encrypt), OpenSSL
-   **CI/CD Platform:** GitHub Actions
-   **Container Registry:** GitHub Container Registry (ghcr.io)
-   **Security Scanners:** Bandit, Safety, Anchore Grype
-   **Monitoring & Alerting:** Prometheus, Grafana, Alertmanager
-   **Notification Channels:** Slack, Email (SMTP)
-   **Centralized Logging:** Grafana Loki, Promtail
-   **Database Migration:** Alembic, Flask-Migrate