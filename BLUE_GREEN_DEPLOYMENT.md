# 🔵🟢 Blue-Green Deployment Guide - K2Panel

## 📋 جدول المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [كيف يعمل Blue-Green](#-كيف-يعمل-blue-green)
- [البنية التحتية](#-البنية-التحتية)
- [الملفات المطلوبة](#-الملفات-المطلوبة)
- [دليل الإعداد](#-دليل-الإعداد)
- [دليل الاستخدام](#-دليل-الاستخدام)
- [استكشاف الأخطاء](#-استكشاف-الأخطاء)
- [أفضل الممارسات](#-أفضل-الممارسات)
- [الأسئلة الشائعة](#-الأسئلة-الشائعة)

---

## 🌟 نظرة عامة

**Blue-Green Deployment** هي استراتيجية نشر متقدمة تضمن **zero-downtime** (عدم توقف الخدمة) عند نشر إصدارات جديدة من التطبيق.

### المزايا الرئيسية

✅ **Zero Downtime** - المستخدمون لا يشعرون بأي توقف  
✅ **Rollback فوري** - العودة للإصدار السابق في ثوانٍ  
✅ **اختبار آمن** - اختبار الإصدار الجديد قبل التبديل  
✅ **تقليل المخاطر** - البيئة القديمة تبقى جاهزة للاستخدام  
✅ **CI/CD متقدم** - نشر تلقائي بدون تدخل يدوي  
✅ **عزل كامل** - بيانات منفصلة لكل بيئة (Blue/Green)  

### متى تستخدم Blue-Green؟

- ✅ تطبيقات الإنتاج ذات الأهمية الحرجة
- ✅ عندما يكون downtime غير مقبول
- ✅ عند الحاجة لاختبار الإصدار الجديد في بيئة الإنتاج
- ✅ عندما تريد rollback فوري وآمن

---

## 🔄 كيف يعمل Blue-Green

### المفهوم الأساسي

```
┌─────────────────────────────────────────────────────────┐
│  لديك بيئتان متطابقتان تماماً:                         │
│  • Blue Environment (الأزرق)                            │
│  • Green Environment (الأخضر)                           │
│                                                          │
│  في أي لحظة، واحدة فقط تخدم المستخدمين (النشطة)          │
│  والأخرى جاهزة للنشر (غير نشطة)                         │
└─────────────────────────────────────────────────────────┘
```

### دورة النشر

```
الحالة الحالية:
┌──────────────┐
│ Blue (نشط)   │ ◄─── المستخدمون
│ Port 5001    │
└──────────────┘
┌──────────────┐
│ Green (معطل) │
│ Port 5002    │
└──────────────┘

↓ (1) نشر الإصدار الجديد على Green

┌──────────────┐
│ Blue (نشط)   │ ◄─── المستخدمون
│ Port 5001    │
└──────────────┘
┌──────────────┐
│ Green (نشط)  │ ← الإصدار الجديد
│ Port 5002    │
└──────────────┘

↓ (2) Health Check للتأكد من سلامة Green

┌──────────────┐
│ Blue (نشط)   │ ◄─── المستخدمون
│ Port 5001    │
└──────────────┘
┌──────────────┐
│ Green (✅)    │ ← Health check نجح
│ Port 5002    │
└──────────────┘

↓ (3) تبديل Traffic من Blue إلى Green

┌──────────────┐
│ Blue (معطل)  │
│ Port 5001    │
└──────────────┘
┌──────────────┐
│ Green (نشط)  │ ◄─── المستخدمون (تحويل فوري)
│ Port 5002    │
└──────────────┘

↓ (4) إيقاف Blue (بعد فترة أمان)

الحالة النهائية:
┌──────────────┐
│ Blue (معطل)  │ ← جاهز للنشر التالي
│ Port 5001    │
└──────────────┘
┌──────────────┐
│ Green (نشط)  │ ◄─── المستخدمون
│ Port 5002    │
└──────────────┘
```

---

## 🏗️ البنية التحتية

### المكونات الرئيسية

```
┌─────────────────────────────────────────────────────────┐
│                      Load Balancer                       │
│                  (Nginx / HAProxy)                       │
│                                                          │
│  يُوجّه الطلبات إلى البيئة النشطة:                       │
│  • Blue: http://localhost:5001                           │
│  • Green: http://localhost:5002                          │
└────────────┬──────────────────────┬─────────────────────┘
             │                      │
   ┌─────────▼────────┐   ┌────────▼────────┐
   │ Blue Environment │   │ Green Environment│
   │ ================ │   │ ================│
   │ • app-blue       │   │ • app-green     │
   │   (Port 5001)    │   │   (Port 5002)   │
   └──────────────────┘   └─────────────────┘
             │                      │
             └──────────┬───────────┘
                        │
         ┌──────────────▼─────────────────┐
         │    Shared Infrastructure       │
         │    ===================         │
         │    • PostgreSQL (postgres-     │
         │      shared)                   │
         │    • Redis (redis-shared)      │
         │    • Persistent Volumes        │
         └────────────────────────────────┘
```

### الموارد المشتركة vs المنفصلة

| المورد | نوعه | السبب |
|--------|------|-------|
| **PostgreSQL** | مشترك | بيانات موحدة بين البيئتين |
| **Redis** | مشترك | cache مشترك |
| **App Container** | منفصل | كل بيئة لها تطبيق مستقل |
| **App Data** | منفصل | عزل كامل - تجنب تضارب البيانات |
| **Logs** | منفصل | logs منفصلة لكل بيئة |

> ⚠️ **مهم**: كل بيئة لها `app_data` منفصل تماماً (`app_data_blue`, `app_data_green`) لضمان عزل كامل وتجنب تضارب البيانات عند تشغيل البيئتين معاً.

---

## 📁 الملفات المطلوبة

### 1. Docker Compose Files

```bash
docker-compose.blue.yml    # تكوين البيئة الزرقاء
docker-compose.green.yml   # تكوين البيئة الخضراء
```

**الاختلافات الرئيسية:**
- **Container name**: `k2panel_app_blue` vs `k2panel_app_green`
- **Port mapping**: `5001:5000` vs `5002:5000`
- **Environment**: `APP_COLOR=blue` vs `APP_COLOR=green`
- **Data volume**: `app_data_blue` vs `app_data_green` (عزل كامل)
- **Logs volume**: `app_logs_blue` vs `app_logs_green`

### 0. Shared Services (جديد!)

```bash
docker-compose.shared.yml   # الخدمات المشتركة (PostgreSQL + Redis)
```

**يجب تشغيله أولاً** قبل أي من البيئتين Blue أو Green.

### 2. Deployment Scripts

```bash
blue-green-deploy.sh       # سكريبت النشر الرئيسي
switch.sh                  # سكريبت تبديل Traffic
```

### 3. Configuration Files

```bash
nginx-blue-green.conf.template   # تكوين nginx للـ Blue-Green
.active_environment              # ملف تتبع البيئة النشطة
```

### 4. GitHub Actions

```bash
.github/workflows/blue-green-deploy.yml   # Workflow للنشر التلقائي
```

---

## 🛠️ دليل الإعداد

### المتطلبات الأساسية

```bash
# 1. Docker & Docker Compose
docker --version          # >= 20.10
docker-compose --version  # >= 1.29

# 2. Nginx (للـ traffic routing)
nginx -v                  # >= 1.18

# 3. curl (للـ health checks)
curl --version
```

### الخطوة 1: إعداد الملفات على VPS

```bash
# الاتصال بالـ VPS
ssh user@your-vps-ip

# إنشاء مجلد النشر
sudo mkdir -p /opt/k2panel
cd /opt/k2panel

# نسخ الملفات المطلوبة (من GitHub أو محلياً)
# سيتم نسخها تلقائياً عبر GitHub Actions
```

### الخطوة 2: إعداد ملف .env

```bash
# نسخ من المثال
cp .env.example .env

# تحرير المتغيرات
nano .env
```

**المتغيرات المطلوبة:**

```bash
# Docker Registry
REGISTRY=ghcr.io
IMAGE_NAME=owner/k2panel
IMAGE_TAG=latest

# Database
POSTGRES_USER=k2panel_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=production_db

# Application
ENVIRONMENT=production
SECRET_KEY=your_secret_key_here
```

### الخطوة 3: إعداد Nginx

```bash
# نسخ template
sudo cp nginx-blue-green.conf.template /etc/nginx/sites-available/k2panel

# استبدال المتغيرات
sudo sed -i 's/${DOMAIN}/your-domain.com/g' /etc/nginx/sites-available/k2panel
sudo sed -i 's/${ACTIVE_PORT}/5001/g' /etc/nginx/sites-available/k2panel

# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/k2panel /etc/nginx/sites-enabled/

# اختبار التكوين
sudo nginx -t

# إعادة تحميل nginx
sudo systemctl reload nginx
```

### الخطوة 4: إضافة Rate Limiting Zones

```bash
# تحرير nginx.conf الرئيسي
sudo nano /etc/nginx/nginx.conf
```

**أضف داخل http block:**

```nginx
http {
    # ... existing config ...
    
    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
}
```

### الخطوة 5: إعداد GitHub Secrets

في repository settings → Secrets and variables → Actions، أضف:

```yaml
VPS_HOST: your.vps.ip.address
VPS_USER: deployment_user
VPS_SSH_KEY: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  ... your SSH private key ...
  -----END OPENSSH PRIVATE KEY-----
VPS_HOST_FINGERPRINT: SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # 🔐 جديد وإلزامي
VPS_DOMAIN: your-domain.com
```

**🔐 للحصول على VPS_HOST_FINGERPRINT:**
```bash
ssh-keyscan -H YOUR_VPS_IP 2>/dev/null | ssh-keygen -lf - | awk '{print $2}'
```

**📋 اختبار الاتصال قبل النشر:**
```bash
# في GitHub: Actions → Test VPS Connection → Run workflow
# تأكد من نجاح جميع الفحوصات قبل النشر
```

---

## 🚀 دليل الاستخدام

### النشر التلقائي (عبر GitHub Actions)

#### التشغيل التلقائي

```yaml
# يتم تشغيله تلقائياً عند:
# 1. Push إلى main branch بعد build ناجح
# 2. إنشاء tag بصيغة v*.*.* (مثل v1.0.0)
```

#### التشغيل اليدوي

```bash
# 1. اذهب إلى GitHub Actions tab
# 2. اختر "Blue-Green Deployment"
# 3. اضغط "Run workflow"
# 4. اختر البيئة (production/staging)
# 5. اختياري: اختر اللون المحدد (blue/green) أو اتركه فارغاً للاكتشاف التلقائي
```

### النشر اليدوي (على VPS مباشرة)

```bash
# الاتصال بالـ VPS
ssh user@your-vps-ip
cd /opt/k2panel

# الخطوة 1: بدء Shared Services (PostgreSQL + Redis)
docker-compose -f docker-compose.shared.yml up -d

# الخطوة 2: تصدير المتغيرات
export REGISTRY=ghcr.io
export IMAGE_NAME=owner/k2panel
export IMAGE_TAG=latest

# تشغيل Blue-Green deployment
./blue-green-deploy.sh
```

**ماذا يفعل السكريبت؟**

```
✓ يكتشف البيئة النشطة الحالية
✓ يُنزّل الصورة الجديدة من Registry
✓ ينشر على البيئة غير النشطة
✓ يفحص صحة البيئة الجديدة (Health Check)
✓ يبدل Traffic للبيئة الجديدة
✓ يوقف البيئة القديمة (بعد 30 ثانية)
✓ ينظف الموارد غير المستخدمة
```

### التبديل اليدوي بين البيئات

```bash
# التبديل إلى Blue
./switch.sh blue

# التبديل إلى Green
./switch.sh green
```

### فحص الحالة الحالية

```bash
# معرفة البيئة النشطة
cat .active_environment

# معرفة الحاويات الجارية
docker ps | grep k2panel

# فحص logs
docker-compose -f docker-compose.blue.yml logs --tail=50 app-blue
docker-compose -f docker-compose.green.yml logs --tail=50 app-green
```

### Rollback السريع

#### Rollback تلقائي
```bash
# يحدث تلقائياً عند فشل:
# • Health check
# • بدء الحاويات
# • أي خطأ في النشر
```

#### Rollback يدوي

```bash
# 1. معرفة البيئة النشطة السابقة
cat .active_environment.backup

# 2. التبديل للبيئة السابقة
./switch.sh <previous_environment>

# مثال:
./switch.sh blue   # إذا كانت blue هي السابقة
```

---

## 🔍 استكشاف الأخطاء

### المشكلة 1: فشل Health Check

**الأعراض:**
```
❌ Health check failed after 15 attempts
```

**الحلول:**

```bash
# 1. فحص logs
docker-compose -f docker-compose.<color>.yml logs app-<color>

# 2. فحص المنفذ مباشرة
curl http://localhost:5001/   # Blue
curl http://localhost:5002/   # Green

# 3. فحص حالة الحاويات
docker-compose -f docker-compose.<color>.yml ps

# 4. فحص متغيرات البيئة
docker-compose -f docker-compose.<color>.yml config
```

### المشكلة 2: البيئتان تعملان معاً

**الأعراض:**
```
Both blue and green containers are running
```

**الحل:**

```bash
# إيقاف البيئة القديمة يدوياً
docker-compose -f docker-compose.<old_color>.yml down
```

### المشكلة 3: فشل تبديل nginx

**الأعراض:**
```
⚠️  Failed to reload nginx
```

**الحلول:**

```bash
# 1. فحص تكوين nginx
sudo nginx -t

# 2. فحص logs
sudo tail -50 /var/log/nginx/error.log

# 3. التحقق من الصلاحيات
ls -l /etc/nginx/sites-available/k2panel
ls -l /etc/nginx/sites-enabled/k2panel

# 4. إعادة تحميل nginx يدوياً
sudo systemctl reload nginx
```

### المشكلة 4: Database connection errors

**الأعراض:**
```
could not connect to server: Connection refused
```

**الحلول:**

```bash
# 1. التحقق من postgres container
docker ps | grep postgres

# 2. فحص logs
docker logs k2panel_postgres_shared

# 3. التحقق من المتغيرات في .env
cat .env | grep POSTGRES

# 4. إعادة تشغيل postgres
docker-compose -f docker-compose.blue.yml restart postgres-shared
```

### المشكلة 5: Port already in use

**الأعراض:**
```
Error: bind: address already in use
```

**الحلول:**

```bash
# 1. معرفة العملية التي تستخدم المنفذ
sudo lsof -i :5001   # Blue
sudo lsof -i :5002   # Green

# 2. إيقاف العملية
sudo kill -9 <PID>

# أو إيقاف الحاوية القديمة
docker-compose -f docker-compose.<color>.yml down
```

---

## ✅ أفضل الممارسات

### 1. قبل النشر

```bash
# ✅ افحص الإصدار الجديد محلياً
docker pull ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
docker run --rm ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} --version

# ✅ راجع الـ logs من build الحالي
# في GitHub Actions

# ✅ أخطر الفريق بالنشر القادم
```

### 2. أثناء النشر

```bash
# ✅ راقب logs في الوقت الفعلي
tail -f /var/log/nginx/k2panel_access.log

# ✅ راقب metrics (CPU, Memory)
docker stats

# ✅ راقب GitHub Actions workflow
```

### 3. بعد النشر

```bash
# ✅ فحص شامل للوظائف الأساسية
# (Login, Dashboard, API endpoints)

# ✅ مراقبة لمدة 15-30 دقيقة

# ✅ الاحتفاظ بالبيئة القديمة لمدة ساعة على الأقل

# ✅ تحديث التوثيق إن لزم
```

### 4. أمان

```bash
# ✅ استخدم HTTPS فقط
# ✅ حدّث الأسرار بانتظام
# ✅ فحص الصور للثغرات قبل النشر
# ✅ احتفظ بنسخ احتياطية من قاعدة البيانات (SHA-256 + HMAC)

# نسخ احتياطي قبل النشر
python backups/backup_manager.py
```

> **ℹ️ ملاحظة:** النسخ الاحتياطية الجديدة تستخدم SHA-256 + HMAC للأمان. النسخ القديمة (MD5) مدعومة للاستعادة فقط.  
> لمزيد من التفاصيل حول SECRET_KEY والنسخ الاحتياطية، راجع [DEPLOYMENT_SECRETS.md](./DEPLOYMENT_SECRETS.md)

### 5. الأداء

```bash
# ✅ استخدم layer caching في Docker
# ✅ احتفظ بآخر 3 إصدارات فقط من الصور
# ✅ نظّف volumes اليتيمة بانتظام
# ✅ راقب استخدام الموارد
```

---

## ❓ الأسئلة الشائعة

### س: كم من الوقت يستغرق النشر؟

**ج:** عادة 2-5 دقائق:
- Pull الصورة: 30-60 ثانية
- بدء البيئة الجديدة: 30-60 ثانية  
- Health checks: 30-90 ثانية
- تبديل Traffic: فوري (< 1 ثانية)

### س: هل البيانات آمنة أثناء النشر؟

**ج:** نعم! قاعدة البيانات مشتركة بين البيئتين ولا يتم إيقافها أبداً.

### س: ماذا لو فشل النشر؟

**ج:** يتم Rollback تلقائي للبيئة السابقة. المستخدمون لا يتأثرون.

### س: هل يمكن تشغيل البيئتين معاً؟

**ج:** تقنياً نعم، لكن للاختبار فقط. في الإنتاج، واحدة فقط تخدم المستخدمين.

### س: كيف أختبر الإصدار الجديد قبل التبديل؟

**ج:** بعد النشر وقبل التبديل، يمكنك الوصول مباشرة:
```bash
# Blue
curl http://your-vps:5001/

# Green
curl http://your-vps:5002/
```

### س: ما هو الفرق عن Rolling Deployment؟

**ج:** 
| Blue-Green | Rolling |
|------------|---------|
| بيئتان كاملتان | حاوية بحاوية |
| Rollback فوري | Rollback بطيء |
| يحتاج موارد أكثر | يحتاج موارد أقل |
| مناسب للتطبيقات الحرجة | مناسب للتطبيقات العادية |

### س: كيف أضيف بيئة ثالثة (مثل Canary)؟

**ج:** Blue-Green يدعم بيئتان فقط. للـ Canary deployment، تحتاج استراتيجية مختلفة.

---

## 📊 مخطط التدفق الكامل

```
┌─────────────────────────────────────────────────────────┐
│           بدء النشر (Trigger)                            │
│   • GitHub Actions (Auto)                                │
│   • Manual Script                                        │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  1. اكتشاف البيئة النشطة                                 │
│     • قراءة .active_environment                          │
│     • اكتشاف تلقائي من Docker containers                 │
│     • تحديد البيئة المستهدفة                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  2. Pull الصورة الجديدة                                 │
│     • من ghcr.io                                         │
│     • التحقق من integrity                                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  3. نشر على البيئة المستهدفة                            │
│     • docker-compose up البيئة الجديدة                   │
│     • انتظار بدء الحاويات                                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  4. Health Check شامل                                    │
│     • فحص /health endpoint                               │
│     • فحص الصفحة الرئيسية                                │
│     • 15 محاولة × 5 ثوانٍ                               │
└──────────────┬──────────────────┬───────────────────────┘
               │                  │
         [نجح] │                  │ [فشل]
               │                  │
               ▼                  ▼
     ┌─────────────────┐  ┌──────────────────┐
     │ 5. تبديل        │  │ ROLLBACK          │
     │    Traffic      │  │ • إيقاف الجديدة   │
     │                 │  │ • استعادة القديمة │
     └────────┬────────┘  └──────────────────┘
              │
              ▼
     ┌─────────────────┐
     │ 6. إيقاف        │
     │    البيئة       │
     │    القديمة      │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ 7. تنظيف        │
     │    الموارد      │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ ✅ اكتمال       │
     │    النشر        │
     └─────────────────┘
```

---

## 📞 الدعم والمساعدة

### المشاكل الشائعة

راجع قسم [استكشاف الأخطاء](#-استكشاف-الأخطاء) أعلاه.

### للمساعدة الإضافية

1. **راجع logs:**
   ```bash
   # Application logs
   docker-compose -f docker-compose.<color>.yml logs

   # Nginx logs
   sudo tail -100 /var/log/nginx/k2panel_error.log

   # System logs
   sudo journalctl -u docker -n 100
   ```

2. **فحص الحالة:**
   ```bash
   # Docker containers
   docker ps -a | grep k2panel

   # Nginx status
   sudo systemctl status nginx

   # Resource usage
   docker stats --no-stream
   ```

3. **اتصل بالفريق الفني**

---

## 📚 مراجع إضافية

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Blue-Green Deployment Pattern](https://martinfowler.com/bliki/BlueGreenDeployment.html)

---

**آخر تحديث:** 30 سبتمبر 2025  
**الإصدار:** 1.0.0  
**المسؤول:** الوكيل رقم 9
