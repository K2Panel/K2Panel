#!/bin/bash
#coding: utf-8
# +-------------------------------------------------------------------
# | K2Panel - Blue-Green Traffic Switch Script
# +-------------------------------------------------------------------
# | Switches traffic between Blue and Green environments
# +-------------------------------------------------------------------

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# المتغيرات
TARGET_ENV="${1:-blue}"
TARGET_PORT="${2:-5001}"
NGINX_CONFIG="/etc/nginx/sites-available/k2panel"
NGINX_ENABLED="/etc/nginx/sites-enabled/k2panel"
ACTIVE_ENV_FILE=".active_environment"

# دوال المساعدة
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "$1"
    echo "═══════════════════════════════════════════════════════════"
}

# التحقق من المعاملات
if [ -z "$TARGET_ENV" ]; then
    print_error "Usage: $0 <blue|green> [port]"
    exit 1
fi

if [ "$TARGET_ENV" != "blue" ] && [ "$TARGET_ENV" != "green" ]; then
    print_error "Invalid environment. Must be 'blue' or 'green'"
    exit 1
fi

# تحديد المنفذ بناءً على البيئة
if [ "$TARGET_ENV" == "blue" ]; then
    TARGET_PORT=5001
else
    TARGET_PORT=5002
fi

print_header "🔄 Traffic Switch Script"
print_info "Switching traffic to: ${TARGET_ENV^^}"
print_info "Target port: ${TARGET_PORT}"

# 1. فحص صحة البيئة المستهدفة قبل التبديل
print_info "Verifying target environment health..."
if curl -f -s "http://localhost:${TARGET_PORT}/health" > /dev/null 2>&1 || \
   curl -f -s "http://localhost:${TARGET_PORT}/" > /dev/null 2>&1; then
    print_success "Target environment is healthy"
else
    print_error "Target environment is not responding! Aborting switch."
    exit 1
fi

# 2. تحديث nginx configuration
BACKUP_CONFIG=""
if [ -f "$NGINX_CONFIG" ]; then
    print_info "Updating nginx configuration..."
    
    # نسخة احتياطية من الـ config الحالي
    BACKUP_CONFIG="${NGINX_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
    sudo cp "$NGINX_CONFIG" "$BACKUP_CONFIG"
    print_info "Backup created: $BACKUP_CONFIG"
    
    # تحديث proxy_pass للمنفذ الجديد
    sudo sed -i "s|proxy_pass http://localhost:[0-9]\+;|proxy_pass http://localhost:${TARGET_PORT};|g" "$NGINX_CONFIG"
    
    print_success "Nginx configuration updated"
    
    # اختبار الـ configuration
    print_info "Testing nginx configuration..."
    if sudo nginx -t; then
        print_success "Nginx configuration is valid"
        
        # إعادة تحميل nginx
        print_info "Reloading nginx..."
        if sudo systemctl reload nginx; then
            print_success "Nginx reloaded successfully"
        else
            print_error "Failed to reload nginx"
            
            # استعادة الـ config السابق
            print_info "Restoring previous nginx configuration..."
            if sudo cp "$BACKUP_CONFIG" "$NGINX_CONFIG"; then
                print_success "Configuration restored from backup"
                sudo systemctl reload nginx
            else
                print_error "Failed to restore configuration from backup!"
            fi
            exit 1
        fi
    else
        print_error "Nginx configuration test failed"
        
        # استعادة الـ config السابق
        print_info "Restoring previous nginx configuration..."
        if sudo cp "$BACKUP_CONFIG" "$NGINX_CONFIG"; then
            print_success "Configuration restored from backup"
        else
            print_error "Failed to restore configuration from backup!"
        fi
        exit 1
    fi
else
    print_warning "Nginx config not found at ${NGINX_CONFIG}"
    print_info "Manual nginx configuration required"
    print_info "Please update your nginx/load balancer to point to http://localhost:${TARGET_PORT}"
fi

# 3. تحديث ملف البيئة النشطة
echo "$TARGET_ENV" > "$ACTIVE_ENV_FILE"
print_success "Active environment updated to: ${TARGET_ENV}"

# 4. التحقق من أن الخدمة تعمل بعد التبديل
print_info "Verifying service after switch..."
sleep 3

# محاولة الوصول عبر nginx (إن وُجد)
if command -v nginx &> /dev/null; then
    if curl -f -s "http://localhost/health" > /dev/null 2>&1 || \
       curl -f -s "http://localhost/" > /dev/null 2>&1; then
        print_success "Service is accessible via nginx"
    else
        print_warning "Service may not be accessible via nginx yet"
    fi
fi

# 5. ملخص التبديل
print_header "📊 Switch Summary"
echo ""
echo "✅ Traffic successfully switched to ${TARGET_ENV^^}!"
echo ""
echo "Active Environment: ${TARGET_ENV^^}"
echo "Active Port: ${TARGET_PORT}"
echo "Nginx Status: $(systemctl is-active nginx 2>/dev/null || echo 'not configured')"
echo ""
print_success "Traffic switch completed! 🎉"
