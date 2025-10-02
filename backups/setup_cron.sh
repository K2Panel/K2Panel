#!/bin/bash

###############################################################################
# setup_cron.sh - إعداد النسخ الاحتياطي التلقائي
# Automatic Backup Scheduling Setup
###############################################################################
# هذا السكريبت يقوم بإعداد cron job للنسخ الاحتياطي اليومي
# This script sets up a daily cron job for automatic backups
###############################################################################

set -e

# الألوان للإخراج
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المسار الأساسي للمشروع
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_SCRIPT="$PROJECT_DIR/backups/backup_manager.py"
LOG_FILE="$PROJECT_DIR/logs/backup_cron.log"

# التحقق من وجود السكريبت
if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo -e "${RED}❌ خطأ: ملف backup_manager.py غير موجود${NC}"
    echo -e "${RED}Error: backup_manager.py not found${NC}"
    exit 1
fi

# إنشاء مجلد logs إذا لم يكن موجوداً
mkdir -p "$PROJECT_DIR/logs"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}         إعداد النسخ الاحتياطي التلقائي - Cron Setup${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# عرض الخيارات
echo -e "${YELLOW}اختر طريقة الجدولة:${NC}"
echo -e "${YELLOW}Choose scheduling method:${NC}"
echo ""
echo "1) Cron (التقليدي - Classic)"
echo "2) Systemd Timer (حديث - Modern, للخوادم الإنتاجية)"
echo "3) عرض الجدولة الحالية فقط (Show current schedule)"
echo "4) إلغاء الجدولة (Remove schedule)"
echo ""
read -p "الاختيار (1-4): " choice

case $choice in
    1)
        # ==================== CRON SETUP ====================
        echo ""
        echo -e "${GREEN}⚙️  إعداد Cron Job...${NC}"
        
        # اختيار وقت التنفيذ
        echo ""
        echo -e "${YELLOW}متى تريد تشغيل النسخ الاحتياطي؟${NC}"
        echo -e "${YELLOW}When to run backups?${NC}"
        echo ""
        echo "1) يومياً الساعة 3:00 صباحاً (Daily at 3:00 AM)"
        echo "2) يومياً الساعة 2:00 صباحاً (Daily at 2:00 AM)"
        echo "3) كل 6 ساعات (Every 6 hours)"
        echo "4) كل 12 ساعة (Every 12 hours)"
        echo "5) يدوي (أدخل وقتاً مخصصاً - Custom cron expression)"
        echo ""
        read -p "الاختيار (1-5): " time_choice
        
        case $time_choice in
            1) CRON_TIME="0 3 * * *" ;;
            2) CRON_TIME="0 2 * * *" ;;
            3) CRON_TIME="0 */6 * * *" ;;
            4) CRON_TIME="0 */12 * * *" ;;
            5)
                echo ""
                echo -e "${YELLOW}أدخل تعبير cron (مثال: 0 3 * * * للساعة 3 صباحاً):${NC}"
                read -p "Cron expression: " CRON_TIME
                ;;
            *)
                echo -e "${RED}❌ اختيار غير صحيح${NC}"
                exit 1
                ;;
        esac
        
        # الأمر الكامل
        CRON_CMD="cd $PROJECT_DIR && /usr/bin/python3 $BACKUP_SCRIPT >> $LOG_FILE 2>&1"
        CRON_ENTRY="$CRON_TIME $CRON_CMD"
        
        # التحقق من وجود cron job سابق
        if crontab -l 2>/dev/null | grep -q "backup_manager.py"; then
            echo ""
            echo -e "${YELLOW}⚠️  يوجد cron job سابق للنسخ الاحتياطي${NC}"
            echo -e "${YELLOW}Previous backup cron job exists${NC}"
            read -p "هل تريد استبداله؟ (y/n): " replace
            if [ "$replace" != "y" ]; then
                echo -e "${BLUE}ℹ️  تم الإلغاء${NC}"
                exit 0
            fi
            # حذف السطر القديم
            (crontab -l 2>/dev/null | grep -v "backup_manager.py") | crontab -
        fi
        
        # إضافة cron job جديد
        (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
        
        echo ""
        echo -e "${GREEN}======================================================================${NC}"
        echo -e "${GREEN}✅ تم إعداد النسخ الاحتياطي التلقائي بنجاح!${NC}"
        echo -e "${GREEN}Automatic backup scheduled successfully!${NC}"
        echo -e "${GREEN}======================================================================${NC}"
        echo ""
        echo -e "${BLUE}📅 الجدولة:${NC} $CRON_TIME"
        echo -e "${BLUE}📁 السكريبت:${NC} $BACKUP_SCRIPT"
        echo -e "${BLUE}📝 السجل:${NC} $LOG_FILE"
        echo ""
        echo -e "${YELLOW}💡 نصائح:${NC}"
        echo -e "  • عرض cron jobs الحالية: ${BLUE}crontab -l${NC}"
        echo -e "  • مراقبة السجل: ${BLUE}tail -f $LOG_FILE${NC}"
        echo -e "  • إزالة الجدولة: ${BLUE}./setup_cron.sh${NC} واختر الخيار 4"
        echo ""
        ;;
        
    2)
        # ==================== SYSTEMD TIMER SETUP ====================
        echo ""
        echo -e "${GREEN}⚙️  إعداد Systemd Timer...${NC}"
        
        # ملفات systemd
        SERVICE_FILE="/etc/systemd/system/k2panel-backup.service"
        TIMER_FILE="/etc/systemd/system/k2panel-backup.timer"
        
        # التحقق من صلاحيات root
        if [ "$EUID" -ne 0 ]; then
            echo -e "${RED}❌ خطأ: يجب تشغيل هذا الخيار كـ root${NC}"
            echo -e "${RED}Error: Systemd setup requires root privileges${NC}"
            echo ""
            echo -e "${YELLOW}استخدم: sudo ./setup_cron.sh${NC}"
            exit 1
        fi
        
        # إنشاء service file
        cat > "$SERVICE_FILE" << EOF
[Unit]
Description=K2Panel Automatic Backup Service
After=network.target

[Service]
Type=oneshot
User=$SUDO_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $BACKUP_SCRIPT
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF
        
        # إنشاء timer file
        cat > "$TIMER_FILE" << EOF
[Unit]
Description=K2Panel Automatic Backup Timer
Requires=k2panel-backup.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
        
        # إعادة تحميل systemd
        systemctl daemon-reload
        
        # تفعيل وتشغيل timer
        systemctl enable k2panel-backup.timer
        systemctl start k2panel-backup.timer
        
        echo ""
        echo -e "${GREEN}======================================================================${NC}"
        echo -e "${GREEN}✅ تم إعداد Systemd Timer بنجاح!${NC}"
        echo -e "${GREEN}Systemd Timer configured successfully!${NC}"
        echo -e "${GREEN}======================================================================${NC}"
        echo ""
        echo -e "${BLUE}📅 الجدولة:${NC} يومياً الساعة 3:00 صباحاً (Daily at 3:00 AM)"
        echo -e "${BLUE}🔧 Service:${NC} k2panel-backup.service"
        echo -e "${BLUE}⏲️  Timer:${NC} k2panel-backup.timer"
        echo ""
        echo -e "${YELLOW}💡 أوامر مفيدة:${NC}"
        echo -e "  • حالة Timer: ${BLUE}systemctl status k2panel-backup.timer${NC}"
        echo -e "  • عرض الجدولة: ${BLUE}systemctl list-timers${NC}"
        echo -e "  • تشغيل يدوي: ${BLUE}systemctl start k2panel-backup.service${NC}"
        echo -e "  • مراقبة السجل: ${BLUE}journalctl -u k2panel-backup.service -f${NC}"
        echo ""
        ;;
        
    3)
        # ==================== عرض الجدولة الحالية ====================
        echo ""
        echo -e "${BLUE}📋 الجدولة الحالية - Current Schedule:${NC}"
        echo ""
        
        # التحقق من cron
        if crontab -l 2>/dev/null | grep -q "backup_manager.py"; then
            echo -e "${GREEN}✓ Cron Job موجود:${NC}"
            crontab -l 2>/dev/null | grep "backup_manager.py"
        else
            echo -e "${YELLOW}ℹ️  لا يوجد Cron Job للنسخ الاحتياطي${NC}"
        fi
        
        echo ""
        
        # التحقق من systemd timer
        if systemctl list-timers 2>/dev/null | grep -q "k2panel-backup.timer"; then
            echo -e "${GREEN}✓ Systemd Timer موجود:${NC}"
            systemctl status k2panel-backup.timer --no-pager
        else
            echo -e "${YELLOW}ℹ️  لا يوجد Systemd Timer للنسخ الاحتياطي${NC}"
        fi
        echo ""
        ;;
        
    4)
        # ==================== إلغاء الجدولة ====================
        echo ""
        echo -e "${YELLOW}⚠️  إزالة الجدولة التلقائية...${NC}"
        
        # حذف cron job
        if crontab -l 2>/dev/null | grep -q "backup_manager.py"; then
            (crontab -l 2>/dev/null | grep -v "backup_manager.py") | crontab -
            echo -e "${GREEN}✓ تم حذف Cron Job${NC}"
        fi
        
        # حذف systemd timer
        if systemctl list-timers 2>/dev/null | grep -q "k2panel-backup.timer"; then
            if [ "$EUID" -ne 0 ]; then
                echo -e "${YELLOW}⚠️  يجب تشغيل كـ root لحذف Systemd Timer${NC}"
            else
                systemctl stop k2panel-backup.timer
                systemctl disable k2panel-backup.timer
                rm -f /etc/systemd/system/k2panel-backup.service
                rm -f /etc/systemd/system/k2panel-backup.timer
                systemctl daemon-reload
                echo -e "${GREEN}✓ تم حذف Systemd Timer${NC}"
            fi
        fi
        
        echo ""
        echo -e "${GREEN}✅ تم إلغاء الجدولة${NC}"
        echo ""
        ;;
        
    *)
        echo -e "${RED}❌ اختيار غير صحيح${NC}"
        exit 1
        ;;
esac

echo -e "${BLUE}======================================================================${NC}"
echo ""
