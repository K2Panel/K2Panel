#!/bin/bash

# ================================================================
# Fail2Ban Testing Script for K2Panel
# ================================================================
# هذا السكريبت يختبر إعدادات Fail2Ban بشكل شامل
#
# الاستخدام:
#   sudo ./test_fail2ban.sh
#
# الاختبارات:
#   1. ✅ Service status
#   2. ✅ Configuration validation
#   3. ✅ Jails status
#   4. ✅ Filters testing
#   5. ✅ Ban/Unban functionality
#   6. ✅ Logs verification
# ================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# ================================================================
# Helper Functions
# ================================================================

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

test_start() {
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo -e "${CYAN}🧪 اختبار $TESTS_TOTAL: $1${NC}"
}

test_pass() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}   ✅ نجح: $1${NC}"
}

test_fail() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}   ❌ فشل: $1${NC}"
}

test_info() {
    echo -e "${BLUE}   ℹ️  $1${NC}"
}

test_warning() {
    echo -e "${YELLOW}   ⚠️  $1${NC}"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}❌ هذا السكريبت يجب تشغيله بصلاحيات root${NC}"
        echo -e "${BLUE}ℹ️  استخدم: sudo $0${NC}"
        exit 1
    fi
}

# ================================================================
# Tests
# ================================================================

check_root

print_header "🛡️  اختبار Fail2Ban لـ K2Panel"

# Test 1: Check if Fail2Ban is installed
test_start "التحقق من تثبيت Fail2Ban"
if command -v fail2ban-server &> /dev/null; then
    VERSION=$(fail2ban-server --version 2>&1 | head -n1)
    test_pass "Fail2Ban مثبت - $VERSION"
else
    test_fail "Fail2Ban غير مثبت"
    echo ""
    echo -e "${RED}الرجاء تشغيل setup_fail2ban.sh أولاً${NC}"
    exit 1
fi

# Test 2: Check if service is running
test_start "التحقق من حالة الخدمة"
if systemctl is-active --quiet fail2ban; then
    test_pass "خدمة Fail2Ban تعمل"
    
    # Check uptime
    UPTIME=$(systemctl show fail2ban --property=ActiveEnterTimestamp --value 2>/dev/null)
    if [ -n "$UPTIME" ]; then
        test_info "Uptime: $UPTIME"
    fi
else
    test_fail "خدمة Fail2Ban لا تعمل"
    test_info "حاول: systemctl start fail2ban"
fi

# Test 3: Check if service is enabled
test_start "التحقق من التفعيل التلقائي"
if systemctl is-enabled --quiet fail2ban 2>/dev/null; then
    test_pass "الخدمة مفعلة للتشغيل التلقائي"
else
    test_warning "الخدمة غير مفعلة للتشغيل التلقائي"
    test_info "حاول: systemctl enable fail2ban"
fi

# Test 4: Validate configuration
test_start "التحقق من صحة jail.local"
if fail2ban-client -t >/dev/null 2>&1; then
    test_pass "jail.local صالح"
else
    test_fail "خطأ في jail.local"
    fail2ban-client -t 2>&1 | head -10
fi

# Test 5: Check jail.local exists
test_start "التحقق من وجود jail.local"
if [ -f /etc/fail2ban/jail.local ]; then
    test_pass "jail.local موجود"
    SIZE=$(stat -c%s /etc/fail2ban/jail.local 2>/dev/null || stat -f%z /etc/fail2ban/jail.local 2>/dev/null)
    test_info "الحجم: $SIZE bytes"
else
    test_fail "jail.local غير موجود"
fi

# Test 6: Check custom filter
test_start "التحقق من custom filter لـ K2Panel"
if [ -f /etc/fail2ban/filter.d/k2panel.conf ]; then
    test_pass "k2panel.conf موجود"
    
    # Test filter with sample log
    SAMPLE_LOG="2025-01-01 12:00:00 [error] Login failed for user 'admin' from IP: 192.168.1.100"
    if echo "$SAMPLE_LOG" | fail2ban-regex - /etc/fail2ban/filter.d/k2panel.conf --print-all-matched >/dev/null 2>&1; then
        test_pass "filter يعمل بشكل صحيح"
    else
        test_warning "filter قد يحتاج مراجعة"
    fi
else
    test_warning "k2panel.conf غير موجود"
fi

# Test 6.1: Test filter accuracy (True Positives) - REAL K2Panel log formats
test_start "اختبار filter - True Positives (يجب أن يطابق)"
if [ -f /etc/fail2ban/filter.d/k2panel.conf ]; then
    TRUE_POSITIVE_COUNT=0
    TRUE_POSITIVE_TOTAL=17
    
    # REAL K2Panel log formats that SHOULD match (actual login failures)
    TP_SAMPLES=(
        # Standard formats
        "2025-01-01 12:00:00 [error] Login failed for user 'admin' from IP: 192.168.1.100"
        "2025-01-01 12:00:00 [notice] Authentication failed from 192.168.1.100"
        "2025-01-01 12:00:00 [error] Failed password for admin from 192.168.1.100 port 12345"
        "2025-01-01 12:00:00 [error] Invalid user test from 192.168.1.50"
        "2025-01-01 12:00:00 [error] Unauthorized access attempt from 10.0.0.5"
        
        # K2Panel-specific formats (username:, ip:, ip())
        "2025-01-01 12:00:00 [error] Login failed, username: admin, ip: 192.168.1.100"
        "2025-01-01 12:00:00 [error] Login failed, username: admin, ip(192.168.1.100)"
        "2025-01-01 12:00:00 Error: login failed; client: 192.168.1.100"
        "2025-01-01 12:00:00 [error] Authentication failed, client: 192.168.1.101"
        "2025-01-01 12:00:00 [error] Failed password for admin, client: 192.168.1.102"
        
        # CRITICAL: Multi-IP scenarios (must match correct IP)
        "2025-01-01 12:00:00 [error] Login failed, username: admin, last login IP: 10.0.0.5, IP: 192.168.1.100"
        "2025-01-01 12:00:00 [error] Login failed from 192.168.1.100, previous login was from 10.0.0.5"
        
        # Variations
        "2025-01-01 12:00:00 [error] login failed from IP: 10.20.30.40"
        "2025-01-01 12:00:00 [error] Auth failed from 172.16.0.1"
        "2025-01-01 12:00:00 [error] Auth failed, client: 172.16.0.2"
        "2025-01-01 12:00:00 [error] Access denied for 192.168.1.99"
        "2025-01-01 12:00:00 [error] Access denied, client: 192.168.1.98"
    )
    
    for sample in "${TP_SAMPLES[@]}"; do
        if echo "$sample" | fail2ban-regex - /etc/fail2ban/filter.d/k2panel.conf --print-all-matched >/dev/null 2>&1; then
            TRUE_POSITIVE_COUNT=$((TRUE_POSITIVE_COUNT + 1))
        fi
    done
    
    if [ $TRUE_POSITIVE_COUNT -eq $TRUE_POSITIVE_TOTAL ]; then
        test_pass "جميع login failures تم اكتشافها ($TRUE_POSITIVE_COUNT/$TRUE_POSITIVE_TOTAL)"
    else
        test_fail "بعض login failures لم يتم اكتشافها ($TRUE_POSITIVE_COUNT/$TRUE_POSITIVE_TOTAL)"
        test_info "  تم اكتشاف $TRUE_POSITIVE_COUNT من أصل $TRUE_POSITIVE_TOTAL"
    fi
else
    test_warning "k2panel.conf غير موجود - تخطي الاختبار"
fi

# Test 6.1.5: CRITICAL - Verify EXACT IP extraction in multi-IP scenarios
test_start "اختبار استخراج IP الصحيح (CRITICAL Multi-IP)"
if [ -f /etc/fail2ban/filter.d/k2panel.conf ]; then
    MULTI_IP_PASS=0
    MULTI_IP_TOTAL=5
    
    # Helper function to extract IP from fail2ban-regex output
    extract_ip() {
        local log_line="$1"
        local output=$(echo "$log_line" | fail2ban-regex - /etc/fail2ban/filter.d/k2panel.conf 2>/dev/null)
        # Extract IP from "Addresses found:" section
        echo "$output" | grep -A 20 "Addresses found:" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1
    }
    
    # Test Case 1: "last login IP: X, IP: Y" - should extract Y
    EXTRACTED=$(extract_ip "2025-01-01 12:00:00 [error] Login failed, username: admin, last login IP: 10.0.0.5, IP: 192.168.1.100")
    if [ "$EXTRACTED" = "192.168.1.100" ]; then
        test_pass "  ✓ Multi-IP case 1: extracted 192.168.1.100 (correct, not 10.0.0.5)"
        MULTI_IP_PASS=$((MULTI_IP_PASS + 1))
    else
        test_fail "  ✗ Multi-IP case 1: extracted '$EXTRACTED' (expected 192.168.1.100)"
    fi
    
    # Test Case 2: "from X, previous login was from Y" - should extract X
    EXTRACTED=$(extract_ip "2025-01-01 12:00:00 [error] Login failed from 192.168.1.100, previous login was from 10.0.0.5")
    if [ "$EXTRACTED" = "192.168.1.100" ]; then
        test_pass "  ✓ Multi-IP case 2: extracted 192.168.1.100 (correct, not 10.0.0.5)"
        MULTI_IP_PASS=$((MULTI_IP_PASS + 1))
    else
        test_fail "  ✗ Multi-IP case 2: extracted '$EXTRACTED' (expected 192.168.1.100)"
    fi
    
    # Test Case 3: "username: X, ip: Y" - should extract Y
    EXTRACTED=$(extract_ip "2025-01-01 12:00:00 [error] Login failed, username: admin, ip: 192.168.1.100")
    if [ "$EXTRACTED" = "192.168.1.100" ]; then
        test_pass "  ✓ Standard case: extracted 192.168.1.100"
        MULTI_IP_PASS=$((MULTI_IP_PASS + 1))
    else
        test_fail "  ✗ Standard case: extracted '$EXTRACTED' (expected 192.168.1.100)"
    fi
    
    # Test Case 4: "client: X" - should extract X
    EXTRACTED=$(extract_ip "2025-01-01 12:00:00 Error: login failed; client: 172.16.0.1")
    if [ "$EXTRACTED" = "172.16.0.1" ]; then
        test_pass "  ✓ Client format: extracted 172.16.0.1"
        MULTI_IP_PASS=$((MULTI_IP_PASS + 1))
    else
        test_fail "  ✗ Client format: extracted '$EXTRACTED' (expected 172.16.0.1)"
    fi
    
    # Test Case 5: "from IP: X" - should extract X
    EXTRACTED=$(extract_ip "2025-01-01 12:00:00 [error] login failed from IP: 10.20.30.40")
    if [ "$EXTRACTED" = "10.20.30.40" ]; then
        test_pass "  ✓ From IP format: extracted 10.20.30.40"
        MULTI_IP_PASS=$((MULTI_IP_PASS + 1))
    else
        test_fail "  ✗ From IP format: extracted '$EXTRACTED' (expected 10.20.30.40)"
    fi
    
    if [ $MULTI_IP_PASS -eq $MULTI_IP_TOTAL ]; then
        test_pass "🎯 CRITICAL: جميع multi-IP scenarios تستخرج IP الصحيح ($MULTI_IP_PASS/$MULTI_IP_TOTAL)"
    else
        test_fail "🚨 CRITICAL: بعض multi-IP scenarios تستخرج IP خاطئ! ($MULTI_IP_PASS/$MULTI_IP_TOTAL)"
        test_warning "⚠️  خطر: قد يتم حظر مستخدمين شرعيين!"
    fi
else
    test_warning "k2panel.conf غير موجود - تخطي الاختبار"
fi

# Test 6.2: Test filter accuracy (False Positives)
test_start "اختبار filter - False Positives (لا يجب أن يطابق)"
if [ -f /etc/fail2ban/filter.d/k2panel.conf ]; then
    FALSE_POSITIVE_COUNT=0
    FALSE_POSITIVE_TOTAL=10
    
    # Test samples that SHOULD NOT match (normal errors + multi-IP lines)
    FP_SAMPLES=(
        # Normal errors
        "2025-01-01 12:00:00 [error] 404 Not Found: /api/users from 192.168.1.200"
        "2025-01-01 12:00:00 [error] 500 Internal Server Error from 192.168.1.201"
        "2025-01-01 12:00:00 [notice] 10.0.0.10 \"GET /api/data\" 404"
        "2025-01-01 12:00:00 [notice] 10.0.0.11 \"POST /api/submit\" 500"
        "2025-01-01 12:00:00 [error] client: 192.168.1.202 - Database connection failed"
        "2025-01-01 12:00:00 [error] client: 192.168.1.203 - File not found: /tmp/data.txt"
        
        # CRITICAL: Multi-IP scenarios that should NOT match
        "2025-01-01 12:00:00 [info] Login succeeded from 192.168.1.10, last failed IP: 10.0.0.5"
        "2025-01-01 12:00:00 [notice] User logged in from 192.168.1.20, previous login 192.168.1.21"
        "2025-01-01 12:00:00 [info] Session established for 192.168.1.30, referred by 192.168.1.31"
        "2025-01-01 12:00:00 [notice] Connection from 192.168.1.40 successful (last IP: 192.168.1.41)"
    )
    
    for sample in "${FP_SAMPLES[@]}"; do
        if ! echo "$sample" | fail2ban-regex - /etc/fail2ban/filter.d/k2panel.conf --print-all-matched >/dev/null 2>&1; then
            FALSE_POSITIVE_COUNT=$((FALSE_POSITIVE_COUNT + 1))
        fi
    done
    
    if [ $FALSE_POSITIVE_COUNT -eq $FALSE_POSITIVE_TOTAL ]; then
        test_pass "لا توجد false positives - جميع الأخطاء العادية تم تجاهلها ($FALSE_POSITIVE_COUNT/$FALSE_POSITIVE_TOTAL)"
    else
        test_fail "توجد false positives! بعض الأخطاء العادية تم اكتشافها بالخطأ ($((FALSE_POSITIVE_TOTAL - FALSE_POSITIVE_COUNT))/$FALSE_POSITIVE_TOTAL)"
        test_warning "⚠️  خطر: المستخدمون الشرعيون قد يتم حظرهم!"
    fi
else
    test_warning "k2panel.conf غير موجود - تخطي الاختبار"
fi

# Test 7: List active jails
test_start "التحقق من الـ jails النشطة"
JAILS_OUTPUT=$(fail2ban-client status 2>/dev/null)
if [ -n "$JAILS_OUTPUT" ]; then
    JAILS_LIST=$(echo "$JAILS_OUTPUT" | grep "Jail list:" | sed 's/.*://; s/,/ /g' | xargs)
    
    if [ -n "$JAILS_LIST" ]; then
        test_pass "Jails نشطة: $JAILS_LIST"
        
        # Count jails
        JAIL_COUNT=$(echo "$JAILS_LIST" | wc -w)
        test_info "عدد الـ jails: $JAIL_COUNT"
    else
        test_warning "لا توجد jails نشطة"
    fi
else
    test_fail "لا يمكن الحصول على حالة الـ jails"
fi

# Test 8: Check each jail status
test_start "التحقق من حالة كل jail"
if [ -n "$JAILS_LIST" ]; then
    for jail in $JAILS_LIST; do
        JAIL_STATUS=$(fail2ban-client status "$jail" 2>/dev/null)
        
        if [ -n "$JAIL_STATUS" ]; then
            BANNED=$(echo "$JAIL_STATUS" | grep "Currently banned:" | awk '{print $4}')
            TOTAL=$(echo "$JAIL_STATUS" | grep "Total banned:" | awk '{print $4}')
            
            if [ "$BANNED" -gt 0 ]; then
                test_info "  $jail: $BANNED banned حالياً (إجمالي: $TOTAL)"
            else
                test_pass "  $jail: يعمل (banned: 0, total: $TOTAL)"
            fi
        else
            test_warning "  $jail: لا يمكن الحصول على الحالة"
        fi
    done
else
    test_warning "لا توجد jails للفحص"
fi

# Test 9: Check log files
test_start "التحقق من ملفات السجلات"

# SSH logs
SSH_LOGS_FOUND=false
for log in /var/log/auth.log /var/log/secure; do
    if [ -f "$log" ] && [ -r "$log" ]; then
        test_pass "  $log موجود وقابل للقراءة"
        SSH_LOGS_FOUND=true
        break
    fi
done

if [ "$SSH_LOGS_FOUND" = false ]; then
    test_warning "  لم يتم العثور على سجلات SSH"
fi

# Nginx logs
if [ -f /var/log/nginx/error.log ]; then
    test_pass "  /var/log/nginx/error.log موجود"
elif [ -f /var/log/nginx/access.log ]; then
    test_pass "  /var/log/nginx/access.log موجود"
else
    test_warning "  سجلات Nginx غير موجودة"
fi

# K2Panel logs
if [ -f /www/server/panel/logs/error.log ]; then
    test_pass "  /www/server/panel/logs/error.log موجود"
else
    test_warning "  سجلات K2Panel غير موجودة"
fi

# Test 10: Check Fail2Ban logs
test_start "التحقق من سجلات Fail2Ban"
if journalctl -u fail2ban -n 1 --no-pager >/dev/null 2>&1; then
    test_pass "سجلات Fail2Ban متاحة (journalctl)"
    
    # Check for recent activity
    RECENT_LOGS=$(journalctl -u fail2ban --since "5 minutes ago" --no-pager 2>/dev/null | wc -l)
    test_info "  سجلات آخر 5 دقائق: $RECENT_LOGS سطر"
elif [ -f /var/log/fail2ban.log ]; then
    test_pass "سجلات Fail2Ban متاحة (/var/log/fail2ban.log)"
else
    test_warning "لا يمكن الوصول إلى سجلات Fail2Ban"
fi

# Test 11: Test ban/unban functionality (safe test)
test_start "اختبار وظيفة Ban/Unban"
TEST_IP="192.0.2.1"  # TEST-NET-1 (RFC 5737 - safe to use)

# Try to ban test IP
if fail2ban-client set sshd banip "$TEST_IP" >/dev/null 2>&1; then
    test_pass "  تم حظر IP اختباري: $TEST_IP"
    
    # Verify ban
    if fail2ban-client status sshd 2>/dev/null | grep -q "$TEST_IP"; then
        test_pass "  تأكيد: IP موجود في قائمة الحظر"
        
        # Unban
        if fail2ban-client set sshd unbanip "$TEST_IP" >/dev/null 2>&1; then
            test_pass "  تم إلغاء الحظر بنجاح"
        else
            test_warning "  فشل إلغاء الحظر"
        fi
    else
        test_warning "  IP غير موجود في قائمة الحظر"
    fi
else
    test_warning "  فشل حظر IP اختباري (قد يكون jail sshd غير نشط)"
fi

# Test 12: Check iptables rules
test_start "التحقق من قواعد iptables"
if command -v iptables &> /dev/null; then
    F2B_CHAINS=$(iptables -L -n 2>/dev/null | grep -c "f2b-" || echo "0")
    
    if [ "$F2B_CHAINS" -gt 0 ]; then
        test_pass "قواعد Fail2Ban موجودة في iptables ($F2B_CHAINS chain)"
    else
        test_warning "لا توجد قواعد Fail2Ban في iptables"
    fi
else
    test_warning "iptables غير متاح"
fi

# Test 13: Check database
test_start "التحقق من قاعدة بيانات Fail2Ban"
if [ -f /var/lib/fail2ban/fail2ban.sqlite3 ]; then
    test_pass "قاعدة البيانات موجودة"
    SIZE=$(stat -c%s /var/lib/fail2ban/fail2ban.sqlite3 2>/dev/null || stat -f%z /var/lib/fail2ban/fail2ban.sqlite3 2>/dev/null)
    test_info "  الحجم: $SIZE bytes"
else
    test_warning "قاعدة البيانات غير موجودة"
fi

# Test 14: Check management script
test_start "التحقق من سكريبت الإدارة"
if [ -f /usr/local/bin/fail2ban-check ] && [ -x /usr/local/bin/fail2ban-check ]; then
    test_pass "fail2ban-check موجود وقابل للتنفيذ"
else
    test_warning "fail2ban-check غير موجود"
fi

# ================================================================
# Summary
# ================================================================

print_header "📊 ملخص الاختبارات"

echo ""
echo -e "${CYAN}النتائج:${NC}"
echo -e "  ${GREEN}✅ نجح: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "  ${RED}❌ فشل: $TESTS_FAILED${NC}"
fi
TESTS_WARNING=$((TESTS_TOTAL - TESTS_PASSED - TESTS_FAILED))
if [ $TESTS_WARNING -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️  تحذير: $TESTS_WARNING${NC}"
fi
echo -e "  ${BLUE}📝 الإجمالي: $TESTS_TOTAL${NC}"
echo ""

# Calculate success rate
SUCCESS_RATE=$((TESTS_PASSED * 100 / TESTS_TOTAL))

if [ $SUCCESS_RATE -ge 90 ]; then
    echo -e "${GREEN}🎉 ممتاز! Fail2Ban يعمل بشكل مثالي (نسبة النجاح: $SUCCESS_RATE%)${NC}"
elif [ $SUCCESS_RATE -ge 70 ]; then
    echo -e "${YELLOW}⚠️  جيد، لكن هناك بعض المشاكل البسيطة (نسبة النجاح: $SUCCESS_RATE%)${NC}"
else
    echo -e "${RED}❌ يحتاج إلى إصلاح (نسبة النجاح: $SUCCESS_RATE%)${NC}"
fi

echo ""
echo -e "${CYAN}الأوامر المفيدة:${NC}"
echo "  • fail2ban-check                    - فحص سريع"
echo "  • fail2ban-client status            - حالة جميع الـ jails"
echo "  • fail2ban-client status <jail>     - حالة jail معين"
echo "  • journalctl -u fail2ban -f         - متابعة السجلات"
echo "  • fail2ban-client unban <IP>        - إلغاء حظر IP"
echo ""

# Exit with appropriate code
if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
