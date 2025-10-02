# 🌐 دليل إعداد Nginx لـ K2Panel

## 📋 نظرة عامة

هذا الدليل يشرح كيفية إعداد Nginx كـ reverse proxy لتطبيق K2Panel في بيئة الإنتاج (VPS). التهيئة تتضمن:

- ✅ Reverse proxy للتطبيق
- ✅ دعم SSL/TLS (HTTPS)
- ✅ دعم WebSocket
- ✅ تحسينات الأداء (gzip, caching)
- ✅ رؤوس الأمان (Security Headers)
- ✅ Rate limiting للحماية من الهجمات
- ✅ صفحات أخطاء مخصصة

---

## 📁 الملفات المُنشأة

### 1. `nginx.conf.template`
ملف تهيئة Nginx الرئيسي (template يحتوي على متغيرات):
- Server blocks للـ HTTP و HTTPS
- إعدادات SSL/TLS محسّنة
- دعم WebSocket لـ `/ws/`
- Rate limiting للـ API و Login
- Caching للملفات الثابتة

### 2. `proxy_params`
ملف يحتوي على معاملات الـ proxy القياسية:
- رؤوس HTTP المطلوبة
- إعدادات timeout
- تعطيل buffering

### 3. `setup_nginx.sh`
سكريبت إعداد تلقائي:
- تثبيت nginx و certbot
- إعداد SSL من Let's Encrypt
- استبدال المتغيرات في template
- إنشاء المجلدات المطلوبة
- اختبار وإعادة تحميل nginx

---

## 🚀 طريقة الإعداد

### الطريقة الأولى: الإعداد التلقائي (موصى به)

#### 1. تحميل الملفات إلى VPS
```bash
# نسخ الملفات إلى الخادم
scp nginx.conf.template nginx_http_only.conf.template proxy_params setup_nginx.sh user@your-vps:/home/user/k2panel/
```

#### 2. تشغيل السكريبت
```bash
cd /home/user/k2panel
sudo ./setup_nginx.sh
```

#### 3. إدخال المعلومات المطلوبة
سيطلب منك السكريبت:
- اسم النطاق (مثال: `example.com`)
- البريد الإلكتروني لـ Let's Encrypt
- تأكيد إعداد SSL

#### 4. مراحل الإعداد ⚡

**⚠️ مهم:** إذا طلبت SSL، سيعمل السكريبت على مرحلتين:

**المرحلة 1 - HTTP فقط:**
- نشر تهيئة HTTP بسيطة (بدون HTTPS)
- الموقع سيعمل مؤقتاً على `http://` فقط
- هذا ضروري حتى يتمكن Let's Encrypt من التحقق من النطاق

**المرحلة 2 - تفعيل HTTPS:**
- الحصول على شهادة SSL من Let's Encrypt
- تحديث التهيئة لتفعيل HTTPS
- إعادة توجيه تلقائي من HTTP إلى HTTPS

**المدة الإجمالية:** 2-3 دقائق

#### 5. انتهى! ✅
السكريبت سيقوم بـ:
- تثبيت nginx و certbot
- نشر HTTP → الحصول على SSL → تفعيل HTTPS
- إعداد التجديد التلقائي للشهادة
- اختبار وتشغيل nginx

---

### الطريقة الثانية: الإعداد اليدوي

#### 1. تثبيت المتطلبات
```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
```

#### 2. إنشاء المجلدات
```bash
sudo mkdir -p /var/www/k2panel/errors
sudo mkdir -p /var/www/certbot
```

#### 3. الحصول على شهادة SSL
```bash
sudo certbot certonly --webroot -w /var/www/certbot \
  -d your-domain.com -d www.your-domain.com \
  --email your-email@example.com \
  --agree-tos
```

#### 4. تطبيق التهيئة
```bash
# نسخ proxy_params
sudo cp proxy_params /etc/nginx/proxy_params

# استبدال المتغيرات في template
DOMAIN="your-domain.com"
APP_PORT="5000"
SSL_CERT="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
SSL_KEY="/etc/letsencrypt/live/$DOMAIN/privkey.pem"

sed -e "s/\${DOMAIN}/$DOMAIN/g" \
    -e "s/\${APP_PORT}/$APP_PORT/g" \
    -e "s|\${SSL_CERT}|$SSL_CERT|g" \
    -e "s|\${SSL_KEY}|$SSL_KEY|g" \
    nginx.conf.template | sudo tee /etc/nginx/sites-available/k2panel
```

#### 5. تفعيل الموقع
```bash
# إنشاء symlink
sudo ln -sf /etc/nginx/sites-available/k2panel /etc/nginx/sites-enabled/

# إزالة الموقع الافتراضي
sudo rm -f /etc/nginx/sites-enabled/default

# اختبار التهيئة
sudo nginx -t

# إعادة تحميل nginx
sudo systemctl reload nginx

# تفعيل البدء التلقائي
sudo systemctl enable nginx
```

---

## 🔧 المتغيرات المستخدمة

يمكن تحديد المتغيرات عبر:
1. ملف `.env` في المجلد الحالي
2. متغيرات البيئة
3. الإدخال التفاعلي

| المتغير | الوصف | القيمة الافتراضية |
|---------|--------|-------------------|
| `DOMAIN` | اسم النطاق | - (إلزامي) |
| `APP_PORT` | منفذ التطبيق | 5000 |
| `SSL_CERT` | مسار شهادة SSL | `/etc/letsencrypt/live/$DOMAIN/fullchain.pem` |
| `SSL_KEY` | مسار مفتاح SSL | `/etc/letsencrypt/live/$DOMAIN/privkey.pem` |
| `USE_SSL` | تفعيل SSL | yes |

---

## 🔒 إعدادات الأمان

### SSL/TLS
- **البروتوكولات**: TLSv1.2, TLSv1.3 فقط
- **Ciphers**: Modern configuration (آمن)
- **HSTS**: مُفعّل (max-age: 2 years)
- **OCSP Stapling**: مُفعّل

### Security Headers
```nginx
Strict-Transport-Security
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy
Referrer-Policy
```

### Rate Limiting
- **API**: 10 requests/second (burst: 20)
- **Login**: 5 requests/minute (burst: 5)
- **Connections**: 10 concurrent connections per IP

---

## ⚡ تحسينات الأداء

### Gzip Compression
- مُفعّل للملفات النصية
- مستوى الضغط: 6
- الحد الأدنى: 1024 bytes

### Caching
- **Static files**: 1 year
- **Favicon**: 1 year
- **Cache-Control**: public, immutable

### Timeouts
- Client body: 12s
- Client header: 12s
- Keepalive: 65s
- Send: 10s

### WebSocket
- دعم كامل لـ `/ws/`
- Timeout: 3600s (1 hour)
- No buffering

---

## 🧪 الاختبار والتحقق

### 1. اختبار التهيئة
```bash
sudo nginx -t
```

### 2. التحقق من SSL
```bash
# عبر openssl
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# عبر موقع SSL Labs
# https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com
```

### 3. اختبار WebSocket
```bash
# استخدم أداة websocat أو wscat
wscat -c wss://your-domain.com/ws/test
```

### 4. اختبار Rate Limiting
```bash
# إرسال طلبات متعددة
for i in {1..15}; do curl -I https://your-domain.com/api/test; done
```

---

## 🔄 التشغيل والصيانة

### أوامر أساسية
```bash
# اختبار التهيئة
sudo nginx -t

# إعادة تحميل التهيئة (بدون downtime)
sudo systemctl reload nginx

# إعادة تشغيل nginx
sudo systemctl restart nginx

# إيقاف nginx
sudo systemctl stop nginx

# حالة nginx
sudo systemctl status nginx
```

### مراجعة السجلات
```bash
# سجل الوصول
sudo tail -f /var/log/nginx/k2panel_access.log

# سجل الأخطاء
sudo tail -f /var/log/nginx/k2panel_error.log

# جميع سجلات nginx
sudo journalctl -u nginx -f
```

### تجديد SSL (تلقائي)
```bash
# التحقق من التجديد التلقائي
sudo certbot renew --dry-run

# تجديد يدوي
sudo certbot renew

# مراجعة cron job
crontab -l | grep certbot
```

---

## 🐛 حل المشاكل الشائعة

### المشكلة: nginx لا يبدأ
```bash
# التحقق من الخطأ
sudo nginx -t
sudo journalctl -u nginx -n 50

# التحقق من المنافذ
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

**الحل**: تأكد من:
- عدم وجود خدمة أخرى على المنافذ 80/443
- صحة مسارات SSL
- صحة syntax الملف

### المشكلة: 502 Bad Gateway
```bash
# التحقق من التطبيق
sudo systemctl status k2panel
curl http://127.0.0.1:5000/health
```

**الحل**: تأكد من:
- التطبيق يعمل على المنفذ الصحيح (5000)
- المنفذ 5000 مفتوح داخلياً
- لا يوجد firewall يمنع الاتصال

### المشكلة: SSL Certificate Error
```bash
# التحقق من الشهادة
sudo certbot certificates
```

**الحل**: 
```bash
# إعادة الحصول على الشهادة
sudo certbot certonly --webroot -w /var/www/certbot \
  -d your-domain.com --force-renewal
```

### المشكلة: WebSocket لا يعمل
**الحل**: تأكد من:
- إعدادات WebSocket موجودة في nginx
- التطبيق يدعم WebSocket على `/ws/`
- لا يوجد buffering في nginx

---

## 📊 المراقبة والأداء

### Nginx Status (اختياري)
يمكن إضافة endpoint للـ status:
```nginx
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

### Metrics (اختياري)
للتكامل مع Prometheus:
```bash
# تثبيت nginx-prometheus-exporter
wget https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v0.11.0/nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz
tar xzf nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz
sudo mv nginx-prometheus-exporter /usr/local/bin/
```

---

## 🔐 Best Practices

### 1. الأمان
- ✅ استخدم HTTPS دائماً
- ✅ فعّل HSTS
- ✅ استخدم TLS 1.2+ فقط
- ✅ فعّل Rate Limiting
- ✅ أخفِ version nginx: `server_tokens off;`

### 2. الأداء
- ✅ فعّل gzip compression
- ✅ استخدم caching للملفات الثابتة
- ✅ استخدم HTTP/2
- ✅ استخدم keepalive connections

### 3. الصيانة
- ✅ مراجعة السجلات بانتظام
- ✅ مراقبة استخدام الموارد
- ✅ تحديث nginx بانتظام
- ✅ نسخ احتياطية للتهيئة (استخدم نظام SHA-256 + HMAC المدمج)
  - انظر [DEPLOYMENT_SECRETS.md](./DEPLOYMENT_SECRETS.md) لتفاصيل SECRET_KEY

---

## 📚 موارد إضافية

### التوثيق الرسمي
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Docs](https://letsencrypt.org/docs/)
- [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)

### أدوات مفيدة
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Security Headers Check](https://securityheaders.com/)
- [WebPageTest](https://www.webpagetest.org/)

---

## 📝 ملاحظات

### للبيئة الإنتاجية
- تأكد من تحديث DNS للنطاق
- افتح المنافذ 80 و 443 في الـ firewall
- راقب استخدام الموارد
- احتفظ بنسخ احتياطية من التهيئة (`python backups/backup_manager.py`)

### للتطوير
- استخدم Docker Compose بدلاً من nginx
- راجع `docker-compose.yml` للتطوير المحلي

---

**آخر تحديث**: 30 سبتمبر 2025  
**المسؤول**: الوكيل رقم 5  
**الحالة**: ✅ جاهز للإنتاج
