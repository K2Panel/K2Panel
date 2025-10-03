<div align="center">
  <img src="@assets/Screenshot_٢٠٢٥١٠٠٢_٢٠٢٣٢٧_Chrome_1759429602919.jpg" alt="K2Panel - Manage Servers Like A Pro" width="400"/>
</div>
<br/>

<div align="center">

[![K2Panel](https://img.shields.io/badge/K2Panel-Server_Management-orange)](https://github.com/K2Panel/K2Panel)
[![social](https://img.shields.io/github/stars/K2Panel/K2Panel?style=social)](https://github.com/K2Panel/K2Panel)

</div>
<p align="center">
  <a href="https://k2panel.online">Official Website</a> | 
  <a href="https://github.com/K2Panel/K2Panel">GitHub Repository</a> |
  <a href="https://k2panel.online/demo">Demo</a>
</p>

## About K2Panel

**K2Panel is a simple but powerful hosting control panel**, it can manage the web server through web-based GUI(Graphical User Interface).

* **one-click function:** such as one-click install LNMP/LAMP developing environment and software.
* **save the time:** Our main goal is helping users to save the time of deploying, thus users just focus on their own project that is fine.

## Demo

Demo：https://k2panel.online/demo<br/>
username: k2panel<br/>
password: k2panel

## What can I do

K2Panel is a server management software that supports the Linux system.

It can easily manage the server through the Web terminal, improving the operation and maintenance efficiency.

## Installation

> Make sure it is a clean operating system, and have not installed Apache /Nginx/php/MySQL from other environments
> K2Panel is developed based on Ubuntu 22+, it is strongly recommended to use Ubuntu 22+ linux distribution

 Note, please execute the installation command with root authority

* Memory: 512M or more, 768M or more is recommended (Pure panel for about 60M of system memory)

* Hard disk: More than 100M available hard disk space (Pure panel for about 20M disk space)

* System: Ubuntu 22.04 24.04, Debian 11 12, CentOS 9, Rocky/AlmaLinux 8 9, to ensure that it is a clean operating system, there is no other environment with Apache/Nginx/php/MySQL installed (the existing environment can not be installed)

**K2Panel Installation Command**

`git clone https://github.com/K2Panel/K2Panel.git && cd K2Panel && bash install.sh`

**K2Panel Docker Deployment**

> The docker image is officially released by K2Panel

Maintained by: [K2Panel](https://binarjoinanalyticnl.nl)



How to use

`$docker run -d -p 8886:8888 -p 22:21 -p 443:443 -p 80:80 -p 889:888 -v ~/website_data:/www/wwwroot -v ~/mysql_data:/www/server/data -v ~/vhost:/www/server/panel/vhost ghcr.io/k2panel/k2panel:latest`

Now you can access K2Panel at http://youripaddress:8886/ from your host system.

* Default username:`k2panel`
* Default password:`k2panel123`

Port usage analysis
* Control Panel   : 8888
* Phpmyadmin      : 888

Dir usage analysis
* Website data    : /www/wwwroot
* Mysql data      : /www/server/data
* Vhost file      : /www/server/panel/vhost 

**Note: after the deployment is complete, please immediately modify the user name and password in the panel settings and add the installation entry**

## 🔧 Advanced Features

### 🔐 Backup System (SHA-256 + HMAC)
Secure backup and restore system with advanced protection:
- **SHA-256 + HMAC** for integrity and authenticity verification
- **Backward Compatible** with legacy MD5 backups (restore-only)
- **Path Traversal Protection** against Zip Slip attacks
- **Resource Limits** to prevent Zip Bomb
- **Automatic Scheduling** with cron/systemd

```bash
# Create backup (v2 format with SHA-256 + HMAC)
python backups/backup_manager.py

# List backups
python backups/backup_manager.py --list

# Restore backup
python backups/backup_manager.py --restore backup_file.tar.gz

# Restore legacy MD5 backup (v1 format)
python backups/backup_manager.py --restore legacy_backup.tar.gz --skip-md5
```

📖 Full documentation: 
- [Backup System Guide](backups/README.md)
- [Deployment Secrets & SECRET_KEY](DEPLOYMENT_SECRETS.md)

### 🔵🟢 Blue-Green Deployment
Zero-downtime deployment strategy:
- **Instant Rollback** in seconds
- **Safe Testing** before switching
- **Automated CI/CD** with GitHub Actions

📖 Full documentation: [BLUE_GREEN_DEPLOYMENT.md](BLUE_GREEN_DEPLOYMENT.md)

### 🚀 Quick Links
- [Deployment Secrets Guide](DEPLOYMENT_SECRETS.md)
- [Nginx Setup Guide](NGINX_SETUP.md)
- [Systemd Setup Guide](SYSTEMD_SETUP.md)
- [Migrations Guide](MIGRATIONS_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)


