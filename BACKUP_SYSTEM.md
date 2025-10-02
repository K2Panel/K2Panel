# 🔐 نظام النسخ الاحتياطي - Backup System

## نظرة عامة

نظام نسخ احتياطي شامل وآمن لـ K2Panel مع تشفير SHA-256 + HMAC وحماية متقدمة ضد الهجمات.

## ✨ المزايا الرئيسية

### 🔒 الأمان المتقدم
- **SHA-256 Checksum** - تحقق من سلامة الملفات بدلاً من MD5 الضعيف
- **HMAC-SHA256** - تحقق من الأصالة باستخدام مفتاح سري
- **Format v2** - نسق محدث مع فرض HMAC إلزامي
- **Constant-time comparison** - حماية من timing attacks
- **Weak key rejection** - رفض المفاتيح الضعيفة في الإنتاج

### 🛡️ الحماية من الهجمات
- ✅ **Path Traversal / Zip Slip** - حماية كاملة
- ✅ **Symlink attacks** - منع symlinks و hardlinks
- ✅ **Zip Bomb** - حدود موارد صارمة
- ✅ **Whitelist validation** - فقط المجلدات المسموحة
- ✅ **Permission exploits** - صلاحيات آمنة (0644/0755)

### 📦 إدارة ذكية
- نسخ تلقائية مجدولة
- الاحتفاظ بعدد محدد من النسخ (افتراضي: 7)
- تنظيف تلقائي للنسخ القديمة
- معلومات شاملة عن كل نسخة

## 🚀 الاستخدام السريع

### إنشاء نسخة احتياطية

```bash
# طريقة 1: نسخة افتراضية
python backups/backup_manager.py

# طريقة 2: تحديد عدد النسخ المحفوظة
python backups/backup_manager.py --keep 10
```

**ماذا يتم نسخه؟**
- ✅ قاعدة البيانات (SQLite أو PostgreSQL dump)
- ✅ ملف `.env` (مع إخفاء القيم الحساسة)
- ✅ ملفات التكوين
- ✅ البيانات المهمة

**مخرجات النسخ:**
```
🔵 بدء النسخ الاحتياطي الشامل - Backup Started
================================================

📦 جاري نسخ قاعدة البيانات...
✓ تم نسخ قاعدة بيانات SQLite بنجاح

📋 جاري نسخ ملف البيئة .env...
✓ تم نسخ .env بشكل آمن (تم إخفاء القيم الحساسة)

📦 جاري ضغط الملفات...
✓ تم إنشاء tarball

🔐 جاري حساب checksum...
✓ SHA-256 + HMAC تم حسابهما

======================================================================
✅ تم إنشاء النسخة الاحتياطية بنجاح!
======================================================================
📁 الملف: backups/backup_20251001_164523.tar.gz
📊 الحجم: 2.45 MB
🔐 SHA-256: a3b5c8d9e1f2...
🔒 HMAC: f9e8d7c6b5a4...
======================================================================
```

### عرض قائمة النسخ

```bash
python backups/backup_manager.py --list
```

**مثال على المخرجات:**
```
====================================================================================================
📋 قائمة النسخ الاحتياطية - Backup List
====================================================================================================

1. backup_20251001_164523.tar.gz
   📅 التاريخ: 2025-10-01 16:45:23
   📊 الحجم: 2.45 MB
   🌍 البيئة: production
   💾 قاعدة البيانات: postgresql
   🔐 SHA-256: a3b5c8d9...

2. backup_20251001_120000.tar.gz
   📅 التاريخ: 2025-10-01 12:00:00
   📊 الحجم: 2.38 MB
   🌍 البيئة: production
   💾 قاعدة البيانات: postgresql

====================================================================================================
📊 إجمالي: 2 نسخة احتياطية | الحجم الكلي: 4.83 MB
====================================================================================================
```

### استرجاع نسخة احتياطية

```bash
# استرجاع مع التحقق الأمني الكامل (موصى به)
python backups/backup_manager.py --restore backups/backup_20251001_164523.tar.gz

# استرجاع مع تخطي التأكيد (للأتمتة فقط)
python backups/backup_manager.py --restore backups/backup_20251001_164523.tar.gz --force

# استرجاع مع تخطي التحقق من checksum (غير آمن - للطوارئ فقط!)
python backups/backup_manager.py --restore backups/backup_20251001_164523.tar.gz --skip-md5
```

**عملية الاسترجاع:**

```
======================================================================
⚠️  تحذير: استرجاع النسخة الاحتياطية
======================================================================

هذه العملية ستستبدل البيانات الحالية!
الملف: backup_20251001_164523.tar.gz

هل تريد المتابعة؟ (yes/no): yes

🔐 جاري التحقق من SHA-256 + HMAC (v2)...
✓ تم التحقق من SHA-256 بنجاح
✓ تم التحقق من HMAC بنجاح (الأصالة مؤكدة)

📦 جاري استخراج الملفات بأمان محسّن...

======================================================================
✅ اكتمل الاسترجاع بأمان!
======================================================================
📊 الإحصائيات:
   ✓ ملفات مقبولة: 45
   ✗ ملفات مرفوضة: 0
   ⊘ ملفات متخطاة: 0
   📦 الحجم الإجمالي: 2.45 MB
📁 الملفات المستخرجة في: restore_temp

⚠️  يجب نقل الملفات يدوياً إلى المواقع المناسبة
```

### تنظيف النسخ القديمة

```bash
python backups/backup_manager.py --cleanup
```

## 🔐 نظام التحقق من الأمان

### Format v2 (الحالي - موصى به)

**الملفات المنشأة:**
1. `backup_YYYYMMDD_HHMMSS.tar.gz` - ملف النسخة المضغوط
2. `backup_YYYYMMDD_HHMMSS.tar.gz.info` - معلومات التحقق

**محتوى ملف .info (v2):**
```
Format: v2
Backup Name: backup_20251001_164523.tar.gz
Created: 2025-10-01 16:45:23
Environment: production
Database Type: postgresql
SHA256: a3b5c8d9e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8
HMAC-SHA256: f9e8d7c6b5a4g3h2i1j0k9l8m7n6o5p4q3r2s1t0u9v8w7x6y5z4a3b2c1d0e9f8
Size: 2.45 MB
Algorithm: SHA-256
```

**عملية التحقق (v2):**
1. ✅ فحص وجود `Format: v2`
2. ✅ التحقق من SHA-256 (constant-time)
3. ✅ التحقق من HMAC باستخدام SECRET_KEY
4. ✅ رفض المفاتيح الضعيفة في الإنتاج
5. ✅ استخراج آمن مع فحص Path Traversal

### Format v1 Legacy (للتوافق الرجعي)

**النسخ القديمة بـ MD5:**
- ⚠️ يتم قبولها مع تحذير
- ⚠️ يُوصى بشدة بإعادة إنشائها بـ SHA-256
- ❌ غير آمنة - MD5 ضعيف ضد الهجمات

**عند استرجاع نسخة MD5:**
```
⚠️  تحذير: النسخة تستخدم MD5 (deprecated - v1 legacy)
   يُوصى بشدة بإعادة إنشاء النسخة بـ SHA-256 + HMAC
✓ تم التحقق من MD5 بنجاح (لكن غير آمن!)
```

## 🛡️ حدود الأمان (Restore Limits)

### الحدود المطبقة

```python
class RestoreLimits:
    MAX_FILES = 100_000           # أقصى عدد ملفات
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB لكل ملف
    MAX_TOTAL_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB إجمالي
    MAX_DEPTH = 10                # أقصى عمق للمسار
    SAFE_FILE_MODE = 0o644        # صلاحيات الملفات
    SAFE_DIR_MODE = 0o755         # صلاحيات المجلدات
    
    ALLOWED_ROOTS = [
        'data/', 'config/', 'backups/', 
        'logs/', 'migrations/', 'vhost/'
    ]
```

### الحماية من الهجمات

#### 1. Path Traversal / Zip Slip
```python
# ❌ محاولة هجوم
backup/../../../etc/passwd  → رفض
/etc/passwd                 → رفض
backup/../../root/.ssh/     → رفض

# ✅ مسموح
backup/data/file.txt        → قبول
backup/config/settings.json → قبول
```

#### 2. Whitelist Validation
```python
# ❌ مجلدات غير مسموحة
backup/malicious/evil.sh    → رفض
backup/unauthorized/key     → رفض

# ✅ مجلدات مسموحة فقط
backup/data/               → قبول
backup/config/             → قبول
```

#### 3. Resource Limits
```python
# ❌ تجاوز الحدود
ملف 150 MB                  → رفض (> 100 MB)
150,000 ملف                → رفض (> 100,000)
مسار بعمق 15 مستوى          → رفض (> 10)

# ✅ ضمن الحدود
ملف 50 MB                   → قبول
80,000 ملف                 → قبول
مسار بعمق 8 مستويات         → قبول
```

#### 4. Symlink Protection
```python
# ❌ symlinks محظورة
backup/data/link -> /etc/passwd  → رفض
parent_is_symlink/file.txt       → رفض

# ✅ ملفات عادية فقط
backup/data/real_file.txt        → قبول
```

## 📋 متطلبات SECRET_KEY

### بيئة التطوير (Development)
- ✅ يتم توليد SECRET_KEY تلقائياً إذا لم يكن موجوداً
- ✅ يمكن استخدام مفاتيح قصيرة للتجربة
- ⚠️ HMAC اختياري

### بيئة الإنتاج (Production)
- ❌ **إلزامي:** SECRET_KEY يجب أن يكون موجوداً
- ❌ **إلزامي:** طول 32 حرف على الأقل
- ❌ **محظور:** المفاتيح الافتراضية:
  - `fallback-key-for-development`
  - `dev-secret`
  - `test-key`
- ✅ **موصى به:** 64 حرف عشوائي

### توليد SECRET_KEY آمن

```bash
# طريقة 1: Python
python -c "import secrets; print(secrets.token_hex(32))"

# طريقة 2: OpenSSL
openssl rand -hex 32

# طريقة 3: /dev/urandom
head -c 32 /dev/urandom | base64

# إضافة إلى .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
```

## 🔄 النسخ الاحتياطية التلقائية

### باستخدام Cron (Linux/macOS)

```bash
# تحرير crontab
crontab -e

# نسخة احتياطية يومية عند 2 صباحاً
0 2 * * * cd /opt/k2panel && python backups/backup_manager.py >> logs/backup.log 2>&1

# نسخة احتياطية كل 6 ساعات
0 */6 * * * cd /opt/k2panel && python backups/backup_manager.py

# نسخة احتياطية أسبوعية (الأحد 3 صباحاً)
0 3 * * 0 cd /opt/k2panel && python backups/backup_manager.py --keep 30
```

### باستخدام systemd Timer

```bash
# إنشاء service
sudo nano /etc/systemd/system/k2panel-backup.service
```

```ini
[Unit]
Description=K2Panel Backup Service
After=network.target

[Service]
Type=oneshot
User=k2panel
WorkingDirectory=/opt/k2panel
ExecStart=/usr/bin/python3 /opt/k2panel/backups/backup_manager.py
StandardOutput=journal
StandardError=journal
```

```bash
# إنشاء timer
sudo nano /etc/systemd/system/k2panel-backup.timer
```

```ini
[Unit]
Description=K2Panel Backup Timer
Requires=k2panel-backup.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# تفعيل
sudo systemctl daemon-reload
sudo systemctl enable k2panel-backup.timer
sudo systemctl start k2panel-backup.timer

# التحقق من الحالة
sudo systemctl status k2panel-backup.timer
```

## 📊 الإحصائيات والمراقبة

### عرض logs النسخ

```bash
# logs النظام
tail -f logs/backup_manager.log

# logs systemd
journalctl -u k2panel-backup.service -f
```

### مراقبة المساحة

```bash
# حجم مجلد النسخ
du -sh backups/

# النسخ الأكبر
ls -lhS backups/backup_*.tar.gz | head -5

# مساحة القرص المتاحة
df -h | grep /opt/k2panel
```

## 🚨 استكشاف الأخطاء

### المشكلة: فشل التحقق من HMAC

**السبب:** SECRET_KEY مختلف عن الذي استُخدم عند إنشاء النسخة (v2)

**الحل:**
```bash
# 1. تحقق من SECRET_KEY الحالي
cat .env | grep SECRET_KEY

# 2. استرجع SECRET_KEY القديم الذي استُخدم لإنشاء النسخة (الحل الموصى به)

# 3. للنسخ القديمة (v1 - MD5) فقط: استخدم --skip-md5 (خطر!)
python backups/backup_manager.py --restore legacy_backup.tar.gz --skip-md5
```

> **⚠️ ملاحظة:** --skip-md5 يُستخدم فقط للنسخ القديمة (v1) التي تستخدم MD5. النسخ الجديدة (v2) تتطلب SECRET_KEY صحيح.

### المشكلة: رفض ملفات أثناء الاسترجاع

**السبب:** الملفات تخالف قيود الأمان

**الحل:**
```bash
# فحص تفاصيل الرفض في logs
tail -100 logs/backup_manager.log | grep "رفض"

# الأسباب الشائعة:
# - Path Traversal: backup/../etc/passwd
# - Whitelist: backup/malicious/file
# - Size: ملف > 100 MB
# - Depth: مسار بعمق > 10
```

### المشكلة: نفاذ المساحة

**الحل:**
```bash
# حذف نسخ قديمة يدوياً
python backups/backup_manager.py --cleanup

# أو حذف الأقدم
cd backups && ls -t *.tar.gz | tail -n +8 | xargs rm -f

# أو ضبط retention
python backups/backup_manager.py --keep 3
```

## ✅ أفضل الممارسات

### 🔒 الأمان
1. ✅ استخدم SECRET_KEY قوي (64 حرف)
2. ✅ خزّن النسخ في مكان آمن خارج الخادم
3. ✅ شفّر النسخ الاحتياطية الحساسة (gpg)
4. ✅ راجع logs النسخ بانتظام
5. ✅ اختبر الاسترجاع دورياً

### 💾 التخزين
1. ✅ احتفظ بـ 7-30 نسخة (حسب الأهمية)
2. ✅ استخدم مواقع تخزين متعددة (3-2-1 rule)
3. ✅ راقب المساحة المتاحة
4. ✅ نظّف النسخ القديمة تلقائياً

### ⏰ الجدولة
1. ✅ نسخ يومية للإنتاج
2. ✅ نسخ أسبوعية طويلة الأجل
3. ✅ نسخ قبل التحديثات المهمة
4. ✅ اختبار الاسترجاع شهرياً

### 📋 التوثيق
1. ✅ وثّق إجراءات الطوارئ
2. ✅ سجّل تواريخ النسخ المهمة
3. ✅ احتفظ بسجل التغييرات
4. ✅ درّب الفريق على الاسترجاع

## 🔄 ترقية من v1 إلى v2

### لماذا الترقية؟
- ❌ MD5 ضعيف أمنياً (collision attacks)
- ✅ SHA-256 + HMAC أكثر أماناً
- ✅ حماية من tampering
- ✅ تحقق من الأصالة

### خطوات الترقية

```bash
# 1. نسخ احتياطية جديدة ستكون v2 تلقائياً
python backups/backup_manager.py

# 2. النسخ القديمة (v1) ستعمل مع تحذير
python backups/backup_manager.py --restore old_backup.tar.gz
# ⚠️  تحذير: النسخة تستخدم MD5 (deprecated)

# 3. إعادة إنشاء النسخ المهمة
python backups/backup_manager.py --restore old_backup.tar.gz
python backups/backup_manager.py  # نسخة جديدة v2
```

## 📚 الوثائق الإضافية

- [BLUE_GREEN_DEPLOYMENT.md](BLUE_GREEN_DEPLOYMENT.md) - نشر بدون توقف
- [DEPLOYMENT_SECRETS.md](DEPLOYMENT_SECRETS.md) - إدارة الأسرار
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل المشاكل

---

**آخر تحديث:** 1 أكتوبر 2025  
**الإصدار:** 2.0 (SHA-256 + HMAC)  
**المسؤول:** فريق K2Panel
