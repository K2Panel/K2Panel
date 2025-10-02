<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="image/logo2.png">
  <source media="(prefers-color-scheme: light)" srcset="image/logo2.png">
  <img src="image/logo2.png" alt="K2Panel - Manage Servers Like A Pro" width="500">
</picture>

<h1>K2Panel</h1>
<h3>🚀 MANAGE SERVERS LIKE A PRO</h3>

<p>
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="#"><img src="https://img.shields.io/badge/Security-Enhanced-28a745?style=for-the-badge&logo=security&logoColor=white" alt="Security"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
</p>

<p><strong>Powerful server management panel with automated deployment, monitoring, and enterprise-grade security</strong></p>

<p>
  <a href="#-quick-start"><strong>Quick Start</strong></a> •
  <a href="#-documentation"><strong>Documentation</strong></a> •
  <a href="#-features"><strong>Features</strong></a> •
  <a href="#-deployment"><strong>Deployment</strong></a>
</p>

<hr>

</div>

---

## 🌟 Overview

**K2Panel** is a comprehensive server management solution designed for professional server administration with enterprise-grade features.

<table>
<tr>
<td width="50%">

### 🔧 Development
- Fast testing and iteration
- Replit environment support
- Quick prototyping
- Debug-friendly setup

</td>
<td width="50%">

### 🚀 Production
- High availability deployment
- VPS/Cloud infrastructure
- Auto-scaling ready
- 99.9%+ uptime target

</td>
</tr>
</table>

### ✨ Key Features

<table>
<tr>
<td width="33%">

#### 🔄 **CI/CD Pipeline**
- Automated deployments
- GitHub Actions workflows
- Pre-deployment validation
- Rollback mechanisms

</td>
<td width="33%">

#### 🔐 **Security First**
- MITM attack prevention
- SSH fingerprint verification
- Secrets management
- Security hardening guides

</td>
<td width="33%">

#### 📊 **Monitoring**
- Real-time metrics
- Prometheus & Grafana
- Centralized logging
- Smart alerts

</td>
</tr>
<tr>
<td width="33%">

#### 🎯 **Zero Downtime**
- Blue-Green deployment
- Health checks
- Automatic rollback
- Traffic switching

</td>
<td width="33%">

#### 💾 **Backup & Recovery**
- Automated backups
- Integrity verification
- Point-in-time recovery
- Disaster recovery

</td>
<td width="33%">

#### 🚢 **Docker Ready**
- Containerized deployment
- Docker Compose support
- Image optimization
- Multi-stage builds

</td>
</tr>
</table>

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

## 🎯 Why K2Panel?

| Feature | Traditional Setup | K2Panel |
|---------|------------------|---------|
| **Deployment Time** | Hours to days | Minutes ⚡ |
| **Security Setup** | Manual, error-prone | Automated ✅ |
| **Monitoring** | Separate tools | Built-in 📊 |
| **Zero Downtime** | Complex setup | One command 🚀 |
| **Rollback** | Manual, risky | Automatic 🔄 |
| **Documentation** | Scattered | Comprehensive 📚 |

---

<div align="center">

### 🌟 **K2Panel** - Professional Server Management Made Simple

<p>Built with ❤️ for developers who value automation, security, and reliability</p>

<p>
  <a href="https://github.com/YOUR_USERNAME/k2panel"><strong>⭐ Star this repo</strong></a> if you find it useful!
</p>

<br>

**Made with Python 🐍 | Powered by Docker 🐳 | Secured by Design 🔐**

</div>
