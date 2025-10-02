#!/bin/bash
#coding: utf-8
# +-------------------------------------------------------------------
# | K2Panel - VPS Deployment Script
# +-------------------------------------------------------------------
# | Automated deployment with health checks and rollback support
# +-------------------------------------------------------------------

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المتغيرات
REGISTRY="${REGISTRY:-ghcr.io}"
IMAGE_NAME="${IMAGE_NAME:-owner/k2panel}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
BACKUP_SUFFIX=".backup.yml"
MAX_HEALTH_RETRIES=15
HEALTH_CHECK_INTERVAL=5

# دوال المساعدة
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "$1"
    echo "═══════════════════════════════════════════════════════════"
}

# 1. التحقق من المتطلبات
check_requirements() {
    print_header "🔍 Checking Requirements"
    
    # التحقق من Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker: $(docker --version)"
    
    # التحقق من Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose: $(docker-compose --version)"
    
    # التحقق من ملف .env
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            print_warning ".env not found, copying from .env.example"
            cp .env.example .env
            print_warning "⚠️  Please update .env with your actual values!"
        else
            print_error ".env file not found"
            exit 1
        fi
    fi
    print_success ".env file exists"
}

# 2. نسخة احتياطية من الإعدادات الحالية
backup_current() {
    print_header "💾 Backing Up Current Configuration"
    
    if [ -f docker-compose.yml ]; then
        cp docker-compose.yml "docker-compose${BACKUP_SUFFIX}"
        print_success "Backed up docker-compose.yml"
    fi
    
    # حفظ الحالة الحالية للحاويات
    docker-compose ps > containers.backup.txt 2>/dev/null || true
    print_success "Backed up container state"
}

# 3. Pull الصورة الجديدة
pull_image() {
    print_header "📦 Pulling New Docker Image"
    
    print_info "Pulling ${FULL_IMAGE}..."
    
    if docker pull "${FULL_IMAGE}"; then
        print_success "Successfully pulled ${FULL_IMAGE}"
    else
        print_error "Failed to pull image"
        exit 1
    fi
    
    # عرض معلومات الصورة
    IMAGE_ID=$(docker images --format "{{.ID}}" "${FULL_IMAGE}" | head -1)
    IMAGE_SIZE=$(docker images --format "{{.Size}}" "${FULL_IMAGE}" | head -1)
    print_info "Image ID: ${IMAGE_ID}"
    print_info "Image Size: ${IMAGE_SIZE}"
}

# 4. إيقاف الخدمات الحالية
stop_services() {
    print_header "⏹️  Stopping Current Services"
    
    if docker-compose ps | grep -q "Up"; then
        print_info "Stopping running containers..."
        docker-compose down
        print_success "Services stopped"
    else
        print_info "No running services to stop"
    fi
}

# 5. تنظيف الموارد غير المستخدمة
cleanup_resources() {
    print_header "🧹 Cleaning Up Unused Resources"
    
    # حذف الصور القديمة (احتفظ بآخر 3 إصدارات)
    print_info "Removing old images..."
    docker images "${REGISTRY}/${IMAGE_NAME}" --format "{{.ID}}" | tail -n +4 | xargs -r docker rmi -f || true
    
    # حذف volumes اليتيمة
    print_info "Removing orphan volumes..."
    docker volume prune -f || true
    
    # حذف شبكات غير مستخدمة
    print_info "Removing unused networks..."
    docker network prune -f || true
    
    print_success "Cleanup completed"
}

# 6. بدء الخدمات الجديدة
start_services() {
    print_header "🚀 Starting New Services"
    
    print_info "Starting containers with new image..."
    
    # بدء الخدمات
    if docker-compose up -d --force-recreate; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        return 1
    fi
    
    # عرض حالة الحاويات
    print_info "Container status:"
    docker-compose ps
}

# 7. Health Check
health_check() {
    print_header "🏥 Health Check"
    
    RETRY_COUNT=0
    APP_URL="http://localhost:5000"
    
    print_info "Waiting for application to be ready..."
    sleep 10
    
    while [ $RETRY_COUNT -lt $MAX_HEALTH_RETRIES ]; do
        # محاولة health endpoint
        if curl -f -s "${APP_URL}/health" > /dev/null 2>&1; then
            print_success "Health check passed! (${APP_URL}/health)"
            return 0
        fi
        
        # محاولة الصفحة الرئيسية
        if curl -f -s "${APP_URL}/" > /dev/null 2>&1; then
            print_success "Health check passed! (${APP_URL}/)"
            return 0
        fi
        
        RETRY_COUNT=$((RETRY_COUNT + 1))
        print_warning "Health check attempt ${RETRY_COUNT}/${MAX_HEALTH_RETRIES} failed, retrying in ${HEALTH_CHECK_INTERVAL}s..."
        sleep $HEALTH_CHECK_INTERVAL
    done
    
    print_error "Health check failed after ${MAX_HEALTH_RETRIES} attempts"
    
    # عرض logs للمساعدة في التشخيص
    print_info "Application logs:"
    docker-compose logs --tail=50 app
    
    return 1
}

# 8. Rollback عند الفشل
rollback() {
    print_header "⚠️  Rolling Back to Previous Version"
    
    print_warning "Deployment failed, initiating rollback..."
    
    # إيقاف الخدمات الفاشلة
    docker-compose down
    
    # استعادة التكوين السابق
    if [ -f "docker-compose${BACKUP_SUFFIX}" ]; then
        mv "docker-compose${BACKUP_SUFFIX}" docker-compose.yml
        print_success "Restored previous docker-compose.yml"
        
        # بدء الخدمات السابقة
        if docker-compose up -d; then
            print_success "Rollback completed successfully"
            
            # فحص صحة الخدمات المستعادة
            if health_check; then
                print_success "Previous version is healthy"
            else
                print_error "Previous version also has health issues!"
            fi
        else
            print_error "Failed to start previous version"
        fi
    else
        print_error "No backup found for rollback"
    fi
}

# 9. تنظيف الملفات المؤقتة
cleanup_temp_files() {
    print_header "🗑️  Cleanup Temporary Files"
    
    # حذف ملفات النسخ الاحتياطي القديمة (احتفظ بآخر 5)
    ls -t docker-compose.backup.*.yml 2>/dev/null | tail -n +6 | xargs -r rm -f
    ls -t containers.backup.*.txt 2>/dev/null | tail -n +6 | xargs -r rm -f
    
    print_success "Temporary files cleaned"
}

# 10. عرض ملخص النشر
deployment_summary() {
    print_header "📊 Deployment Summary"
    
    echo ""
    echo "✅ Deployment completed successfully!"
    echo ""
    echo "Image: ${FULL_IMAGE}"
    echo "Container Status:"
    docker-compose ps
    echo ""
    echo "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" $(docker-compose ps -q)
    echo ""
    print_success "Application is now live! 🎉"
}

# ==================== التنفيذ الرئيسي ====================
main() {
    print_header "🚀 K2Panel Deployment Script"
    echo "Image: ${FULL_IMAGE}"
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 1. التحقق من المتطلبات
    check_requirements
    
    # 2. نسخة احتياطية
    backup_current
    
    # 3. Pull الصورة الجديدة
    pull_image
    
    # 4. إيقاف الخدمات الحالية
    stop_services
    
    # 5. تنظيف الموارد
    cleanup_resources
    
    # 6. بدء الخدمات الجديدة
    if ! start_services; then
        rollback
        exit 1
    fi
    
    # 7. Health Check
    if ! health_check; then
        rollback
        exit 1
    fi
    
    # 8. تنظيف الملفات المؤقتة
    cleanup_temp_files
    
    # 9. ملخص النشر
    deployment_summary
    
    print_success "Deployment completed successfully! ✅"
    exit 0
}

# تشغيل السكريبت
main "$@"
