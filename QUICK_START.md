
# 🚀 دليل البدء السريع - K2Panel

## البيئة 1️⃣: Replit (التطوير)

### الخطوات:
1. **Fork** المشروع على Replit
2. انقر **Run** ▶️
3. افتح **Preview** 🌐

### المميزات:
- ✅ لا يتطلب إعداد
- ✅ يكتشف البيئة تلقائياً
- ✅ مثالي للتطوير والاختبار
- ✅ يدعم Hot Reload

### URL التطبيق:
```
https://your-repl-name.your-username.repl.co
```

---

## البيئة 2️⃣: VPS (الإنتاج)

### التثبيت السريع (10 دقائق):

```bash
# 1. تثبيت Docker
curl -fsSL https://get.docker.com | sh

# 2. Clone المشروع
git clone https://github.com/K2Panel/K2Panel.git
cd K2Panel

# 3. إعداد البيئة
cp .env.example .env
nano .env  # عدّل SECRET_KEY و DATABASE_URL

# 4. تشغيل
docker-compose up -d
```

### التثبيت القياسي (30 دقيقة):

```bash
# 1. تثبيت Python و Dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx certbot -y

# 2. Clone المشروع
git clone https://github.com/K2Panel/K2Panel.git
cd K2Panel

# 3. إعداد systemd
sudo ./setup_systemd.sh

# 4. إعداد Nginx + SSL
sudo ./setup_nginx.sh
```

---

## التحقق من الجاهزية

```bash
# تشغيل سكريبت الفحص
python3 check_readiness.py
```

**النتيجة المتوقعة:**
```
✅ التطبيق جاهز للنشر على البيئتين!
```

---

## المسارات المهمة

| المسار | الوصف |
|--------|--------|
| `/` | الصفحة الرئيسية |
| `/health` | فحص الصحة |
| `/health/ready` | جاهزية التطبيق |
| `/api/docs` | توثيق API |

---

## التطوير والنشر

### سير العمل الموصى به:

```
Replit (Dev) → Git Push → GitHub → VPS (Production)
```

1. **طور في Replit** 💻
2. **ادفع للـ Git** 📤
3. **اسحب في VPS** 📥
4. **أعد التشغيل** 🔄

```bash
# في VPS
cd /opt/k2panel
git pull origin main
sudo systemctl restart k2panel
```

---

## استكشاف الأخطاء

### Replit:
```bash
# فحص السجلات
cat logs/app.log
```

### VPS:
```bash
# فحص خدمة systemd
sudo systemctl status k2panel
sudo journalctl -u k2panel -f

# فحص Nginx
sudo nginx -t
sudo systemctl status nginx
```

---

## الأوامر المفيدة

### Replit:
```bash
python3 runserver.py          # تشغيل
python3 check_readiness.py    # فحص
python3 backups/backup_manager.py  # نسخ احتياطي
```

### VPS:
```bash
sudo systemctl restart k2panel  # إعادة تشغيل
sudo systemctl reload nginx     # إعادة تحميل Nginx
docker-compose restart          # إعادة تشغيل Docker
```

---

## الدعم والتوثيق

📚 **أدلة شاملة:**
- [VPS_DEPLOYMENT_GUIDE.md](./VPS_DEPLOYMENT_GUIDE.md)
- [DOCKER_USAGE.md](./DOCKER_USAGE.md)
- [SYSTEMD_SETUP.md](./SYSTEMD_SETUP.md)
- [NGINX_SETUP.md](./NGINX_SETUP.md)

🐛 **المشاكل؟** راجع [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

✅ **التطبيق جاهز للعمل على البيئتين!**
