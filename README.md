<div align="center">

<img src="attached_assets/a7444a760ad4ea7_file_0000000038f46230b90e1aa8798aaf7d_wm_1759442589561.png" alt="K2Panel Logo" width="400">

# K2Panel
### MANAGE SERVERS LIKE A PRO

[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Security](https://img.shields.io/badge/Security-Enhanced-success?logo=shield&logoColor=white)](#)

**Powerful server management panel with automated deployment, monitoring, and security**

[Quick Start](#-quick-start) • [Documentation](#-documentation) • [Features](#-features) • [Deployment](#-deployment)

</div>

---

## 🌟 Overview

**K2Panel** is a comprehensive server management solution designed for:

- 🔧 **Development** (Replit) - Fast testing and development
- 🚀 **Production** (VPS) - Reliable deployment with high uptime

### Key Features

- ✅ **Unified Codebase** - Single source for all environments
- ✅ **Automated CI/CD** - Secure deployment pipeline
- ✅ **Comprehensive Monitoring** - Real-time metrics and alerts
- ✅ **Automated Backups** - Scheduled with integrity verification
- ✅ **Enterprise Security** - MITM protection, SSH fingerprint verification
- ✅ **Zero-Downtime Deployment** - Blue-Green deployment strategy

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Python 3.8+
- Docker & Docker Compose
- VPS with Ubuntu 20.04+ (for production)

# Optional (for development)
- Replit account
```

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/k2panel.git
cd k2panel

# 2. Setup environment
cp .env.example .env
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python run.py
```

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment guide.

---

## 📚 Documentation

| Document | Description | When to Use |
|----------|-------------|-------------|
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Complete deployment guide | Production setup |
| [DEPLOYMENT_SECRETS.md](./DEPLOYMENT_SECRETS.md) | GitHub Secrets setup | CI/CD configuration |
| [BLUE_GREEN_DEPLOYMENT.md](./BLUE_GREEN_DEPLOYMENT.md) | Zero-downtime deployment | Advanced deployment |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues & solutions | When problems occur |
| [SECURITY_HARDENING_GUIDE.md](./SECURITY_HARDENING_GUIDE.md) | Security best practices | Production security |

---

## 🔐 Security Features

### SSH Host Fingerprint Verification (NEW)
- **MITM Attack Protection** - Mandatory host fingerprint verification
- **StrictHostKeyChecking** - Enforced on all SSH connections
- **Automated Testing** - Pre-deployment connection validation

### Required GitHub Secrets (4)
```yaml
VPS_HOST              # VPS IP address
VPS_USER              # SSH username
VPS_SSH_KEY           # SSH private key
VPS_HOST_FINGERPRINT  # 🔐 SSH fingerprint (REQUIRED for MITM protection)
```

**Get fingerprint:**
```bash
ssh-keyscan -H YOUR_VPS_IP 2>/dev/null | ssh-keygen -lf - | awk '{print $2}'
```

---

## 🧪 Testing & CI/CD

### Test VPS Connection
```bash
# In GitHub Repository:
Actions → Test VPS Connection → Run workflow

# Validates:
✅ All GitHub Secrets are configured
✅ SSH connection works
✅ Host fingerprint verified (MITM protection)
✅ Docker installed
✅ Deployment path exists
```

### Automated Deployment
- **Trigger**: Push to `main` branch
- **Workflow**: Build → Test → Deploy (Blue-Green)
- **Rollback**: Automatic on failure

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           K2Panel Architecture              │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐         ┌──────────────┐  │
│  │   Frontend  │ ◄─────► │   Backend    │  │
│  │   (Vite)    │         │   (Python)   │  │
│  └─────────────┘         └──────────────┘  │
│         │                        │          │
│         ▼                        ▼          │
│  ┌─────────────────────────────────────┐   │
│  │         Nginx (Reverse Proxy)       │   │
│  └─────────────────────────────────────┘   │
│                     │                       │
│         ┌───────────┴───────────┐          │
│         ▼                       ▼          │
│  ┌─────────────┐         ┌──────────────┐  │
│  │ PostgreSQL  │         │    Redis     │  │
│  │  Database   │         │    Cache     │  │
│  └─────────────┘         └──────────────┘  │
│                                             │
│  Monitoring: Prometheus + Grafana + Loki   │
└─────────────────────────────────────────────┘
```

---

## 📊 Deployment Strategies

### 1. Basic Deployment (VPS + Docker)
- Simple setup for small projects
- Direct deployment to VPS
- Manual rollback if needed

### 2. Blue-Green Deployment (Recommended)
- Zero-downtime deployment
- Automatic health checks
- Instant rollback capability
- Traffic switching with Nginx

### 3. CI/CD Pipeline (Advanced)
- Automated testing
- Multi-environment support
- Slack/Email notifications
- Automated backups

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: Vite, Modern JavaScript
- **Database**: PostgreSQL, Redis
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana, Loki
- **Reverse Proxy**: Nginx
- **SSL/TLS**: Let's Encrypt

---

## 📈 Monitoring & Alerts

- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Loki** - Centralized logging
- **Alertmanager** - Smart notifications
- **Integrations**: Slack, Email, PagerDuty

---

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

---

## 📄 License

This project is proprietary. See LICENSE file for details.

---

## 📞 Support

- 📚 [Documentation](./DEPLOYMENT.md)
- 🐛 [Issues](https://github.com/YOUR_USERNAME/k2panel/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/k2panel/discussions)

---

<div align="center">

**K2Panel** - Professional Server Management Made Simple

**[⭐ Star this repo](https://github.com/YOUR_USERNAME/k2panel)** if you find it useful!

</div>
