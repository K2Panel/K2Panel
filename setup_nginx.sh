#!/bin/bash

# ================================================================
# Nginx Setup Script for K2Panel
# ================================================================
# هذا السكريبت يقوم بإعداد nginx للإنتاج تلقائياً
# 
# الاستخدام:
#   sudo ./setup_nginx.sh
#
# يمكن تحديد المتغيرات عبر:
#   1. ملف .env في المجلد الحالي
#   2. متغيرات البيئة
#   3. الإدخال التفاعلي
# ================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ================================================================
# Helper Functions
# ================================================================

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ================================================================
# Check Requirements
# ================================================================

print_info "فحص المتطلبات..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "يجب تشغيل هذا السكريبت بصلاحيات root"
    print_info "استخدم: sudo ./setup_nginx.sh"
    exit 1
fi

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    print_warning "nginx غير مثبت. جاري التثبيت..."
    apt-get update
    apt-get install -y nginx
    print_success "تم تثبيت nginx"
else
    print_success "nginx مثبت بالفعل"
fi

# Check if certbot is installed (for SSL)
if ! command -v certbot &> /dev/null; then
    print_warning "certbot غير مثبت (مطلوب للـ SSL)"
    print_info "جاري تثبيت certbot..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
    print_success "تم تثبيت certbot"
else
    print_success "certbot مثبت بالفعل"
fi

# ================================================================
# Load Environment Variables
# ================================================================

print_info "تحميل المتغيرات..."

# Load from .env if exists
if [ -f .env ]; then
    print_info "تحميل من .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Get configuration values (with defaults)
DOMAIN=${DOMAIN:-""}
APP_PORT=${APP_PORT:-5000}
SSL_CERT=${SSL_CERT:-"/etc/letsencrypt/live/\$DOMAIN/fullchain.pem"}
SSL_KEY=${SSL_KEY:-"/etc/letsencrypt/live/\$DOMAIN/privkey.pem"}
USE_SSL=${USE_SSL:-"yes"}

# ================================================================
# Interactive Configuration
# ================================================================

print_info "إعداد التهيئة..."

# Ask for domain if not set
if [ -z "$DOMAIN" ]; then
    echo -n "أدخل اسم النطاق (مثال: example.com): "
    read DOMAIN
fi

if [ -z "$DOMAIN" ]; then
    print_error "يجب إدخال اسم النطاق"
    exit 1
fi

print_success "النطاق: $DOMAIN"

# Ask for SSL setup
if [ "$USE_SSL" = "yes" ]; then
    echo -n "هل تريد إعداد SSL تلقائياً باستخدام Let's Encrypt؟ (y/n) [y]: "
    read SETUP_SSL
    SETUP_SSL=${SETUP_SSL:-y}
else
    SETUP_SSL="n"
fi

# ================================================================
# Store SSL email for later use
# ================================================================

SSL_REQUESTED="no"
if [ "$SETUP_SSL" = "y" ] || [ "$SETUP_SSL" = "yes" ]; then
    print_info "إعداد شهادة SSL..."
    
    # Ask for email
    echo -n "أدخل البريد الإلكتروني لـ Let's Encrypt: "
    read SSL_EMAIL
    
    if [ -z "$SSL_EMAIL" ]; then
        print_error "يجب إدخال البريد الإلكتروني"
        exit 1
    fi
    
    SSL_REQUESTED="yes"
    USE_SSL="no"  # Start with HTTP-only config
    print_info "سيتم نشر تهيئة HTTP أولاً، ثم الحصول على SSL، ثم تحديث التهيئة..."
else
    print_info "تخطي إعداد SSL"
    USE_SSL="no"
fi

# ================================================================
# Create Nginx Configuration
# ================================================================

print_info "إنشاء تهيئة nginx..."

# Choose appropriate template based on SSL setting
if [ "$USE_SSL" = "no" ]; then
    # Use HTTP-only template for initial setup
    if [ ! -f "nginx_http_only.conf.template" ]; then
        print_error "nginx_http_only.conf.template غير موجود"
        exit 1
    fi
    TEMPLATE_FILE="nginx_http_only.conf.template"
    print_info "استخدام تهيئة HTTP فقط..."
else
    # Use full template with HTTPS
    if [ ! -f "nginx.conf.template" ]; then
        print_error "nginx.conf.template غير موجود"
        exit 1
    fi
    TEMPLATE_FILE="nginx.conf.template"
    print_info "استخدام تهيئة HTTPS كاملة..."
fi

# Create temporary config file
TEMP_CONFIG="/tmp/k2panel_nginx.conf"
cp "$TEMPLATE_FILE" "$TEMP_CONFIG"

# Replace variables in template
sed -i "s/\${DOMAIN}/$DOMAIN/g" "$TEMP_CONFIG"
sed -i "s/\${APP_PORT}/$APP_PORT/g" "$TEMP_CONFIG"
sed -i "s|\${SSL_CERT}|$SSL_CERT|g" "$TEMP_CONFIG"
sed -i "s|\${SSL_KEY}|$SSL_KEY|g" "$TEMP_CONFIG"

# ================================================================
# Create Required Directories
# ================================================================

print_info "إنشاء المجلدات المطلوبة..."

mkdir -p /var/www/k2panel
mkdir -p /var/www/k2panel/errors
mkdir -p /var/www/certbot
mkdir -p /var/log/nginx

# Create simple error pages
cat > /var/www/k2panel/errors/404.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>404 - الصفحة غير موجودة</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { font-size: 48px; color: #e74c3c; }
        p { font-size: 18px; color: #555; }
    </style>
</head>
<body>
    <h1>404</h1>
    <p>عذراً، الصفحة المطلوبة غير موجودة</p>
    <p><a href="/">العودة للصفحة الرئيسية</a></p>
</body>
</html>
EOF

cat > /var/www/k2panel/errors/50x.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>خطأ في الخادم</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { font-size: 48px; color: #e67e22; }
        p { font-size: 18px; color: #555; }
    </style>
</head>
<body>
    <h1>خطأ في الخادم</h1>
    <p>عذراً، حدث خطأ أثناء معالجة طلبك</p>
    <p>يرجى المحاولة مرة أخرى لاحقاً</p>
</body>
</html>
EOF

print_success "تم إنشاء المجلدات والملفات"

# ================================================================
# Install Nginx Configuration
# ================================================================

print_info "تثبيت تهيئة nginx..."

# Backup existing config if exists
NGINX_SITE="/etc/nginx/sites-available/k2panel"
if [ -f "$NGINX_SITE" ]; then
    print_warning "توجد تهيئة سابقة، جاري عمل نسخة احتياطية..."
    cp "$NGINX_SITE" "$NGINX_SITE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy configuration
cp "$TEMP_CONFIG" "$NGINX_SITE"
print_success "تم نسخ التهيئة إلى $NGINX_SITE"

# Copy proxy_params if exists
if [ -f "proxy_params" ]; then
    cp proxy_params /etc/nginx/proxy_params
    print_success "تم نسخ proxy_params"
fi

# Enable site (create symlink)
ln -sf "$NGINX_SITE" /etc/nginx/sites-enabled/k2panel
print_success "تم تفعيل الموقع"

# Remove default site (optional)
if [ -f /etc/nginx/sites-enabled/default ]; then
    print_info "إزالة الموقع الافتراضي..."
    rm -f /etc/nginx/sites-enabled/default
fi

# ================================================================
# Test and Reload Nginx
# ================================================================

print_info "اختبار التهيئة..."

if nginx -t; then
    print_success "التهيئة صحيحة ✓"
    
    print_info "إعادة تحميل nginx..."
    systemctl reload nginx
    print_success "تم إعادة تحميل nginx"
    
    # Enable nginx on boot
    systemctl enable nginx
    print_success "nginx سيبدأ تلقائياً عند الإقلاع"
else
    print_error "خطأ في تهيئة nginx"
    print_info "راجع السجلات: sudo nginx -t"
    exit 1
fi

# ================================================================
# Setup SSL with Certbot (after nginx is configured with HTTP-only)
# ================================================================

if [ "$SSL_REQUESTED" = "yes" ]; then
    echo ""
    print_info "════════════════════════════════════════"
    print_info "  المرحلة 2: الحصول على شهادة SSL"
    print_info "════════════════════════════════════════"
    echo ""
    
    # nginx is now serving HTTP and can handle ACME challenge
    print_info "الحصول على شهادة SSL من Let's Encrypt..."
    print_info "(قد يستغرق بضع دقائق...)"
    
    # Use certbot certonly with webroot (nginx already serves the path)
    certbot certonly --webroot -w /var/www/certbot \
        -d "$DOMAIN" -d "www.$DOMAIN" \
        --email "$SSL_EMAIL" \
        --agree-tos \
        --non-interactive || {
        print_error "فشل الحصول على شهادة SSL"
        print_info "تأكد من:"
        print_info "  1. DNS للنطاق يشير إلى هذا الخادم"
        print_info "  2. المنافذ 80 و 443 مفتوحة في firewall"
        print_info "  3. nginx يعمل بشكل صحيح"
        echo ""
        print_info "يمكنك محاولة الحصول على الشهادة يدوياً عبر:"
        print_info "  sudo certbot certonly --webroot -w /var/www/certbot -d $DOMAIN"
        echo ""
        print_warning "سيبقى الموقع يعمل على HTTP فقط"
        print_success "انتهى الإعداد (بدون SSL)"
        exit 0
    }
    
    print_success "تم الحصول على شهادة SSL بنجاح!"
    
    # Now re-create configuration with SSL enabled
    print_info "تحديث التهيئة لتفعيل HTTPS..."
    
    SSL_CERT="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
    SSL_KEY="/etc/letsencrypt/live/$DOMAIN/privkey.pem"
    USE_SSL="yes"
    
    # Re-create config with SSL
    TEMP_CONFIG="/tmp/k2panel_nginx_ssl.conf"
    cp nginx.conf.template "$TEMP_CONFIG"
    
    # Replace variables
    sed -i "s/\${DOMAIN}/$DOMAIN/g" "$TEMP_CONFIG"
    sed -i "s/\${APP_PORT}/$APP_PORT/g" "$TEMP_CONFIG"
    sed -i "s|\${SSL_CERT}|$SSL_CERT|g" "$TEMP_CONFIG"
    sed -i "s|\${SSL_KEY}|$SSL_KEY|g" "$TEMP_CONFIG"
    
    # Install new config with SSL
    cp "$TEMP_CONFIG" "$NGINX_SITE"
    
    # Test new config
    print_info "اختبار التهيئة الجديدة..."
    if nginx -t; then
        print_success "التهيئة صحيحة ✓"
        
        # Reload nginx
        print_info "إعادة تحميل nginx لتفعيل HTTPS..."
        systemctl reload nginx
        print_success "تم تفعيل HTTPS بنجاح!"
        
        # Setup auto-renewal
        print_info "إعداد التجديد التلقائي للشهادة..."
        (crontab -l 2>/dev/null; echo "0 0,12 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
        print_success "تم إعداد التجديد التلقائي"
    else
        print_error "خطأ في التهيئة الجديدة"
        print_warning "الموقع لا يزال يعمل على HTTP"
        exit 1
    fi
    
    # Clean up
    rm -f "$TEMP_CONFIG"
fi

# ================================================================
# Summary
# ================================================================

echo ""
print_success "════════════════════════════════════════"
print_success "  تم إعداد nginx بنجاح!"
print_success "════════════════════════════════════════"
echo ""
print_info "معلومات الإعداد:"
echo "  • النطاق: $DOMAIN"
echo "  • منفذ التطبيق: $APP_PORT"
echo "  • SSL: $([ "$USE_SSL" = "yes" ] && echo "مُفعّل ✓" || echo "غير مُفعّل")"
echo "  • ملف التهيئة: $NGINX_SITE"
echo ""

if [ "$USE_SSL" = "yes" ]; then
    print_info "شهادة SSL:"
    echo "  • الشهادة: $SSL_CERT"
    echo "  • المفتاح: $SSL_KEY"
    echo "  • التجديد: تلقائي (cron job)"
    echo ""
fi

print_info "الأوامر المفيدة:"
echo "  • اختبار التهيئة: sudo nginx -t"
echo "  • إعادة التحميل: sudo systemctl reload nginx"
echo "  • إعادة التشغيل: sudo systemctl restart nginx"
echo "  • السجلات: sudo tail -f /var/log/nginx/k2panel_error.log"
echo ""

print_success "يمكنك الآن الوصول للتطبيق عبر:"
if [ "$USE_SSL" = "yes" ]; then
    echo "  🔒 https://$DOMAIN"
    echo "  🔒 https://www.$DOMAIN"
else
    echo "  🌐 http://$DOMAIN"
    echo "  🌐 http://www.$DOMAIN"
fi
echo ""

print_info "ملاحظة: تأكد من أن التطبيق يعمل على المنفذ $APP_PORT"
print_info "استخدم: gunicorn -b 127.0.0.1:$APP_PORT runserver:app"
echo ""

# Clean up
rm -f "$TEMP_CONFIG"

print_success "انتهى الإعداد بنجاح! 🎉"
