
#!/usr/bin/python
# coding: utf-8
# -------------------------------------------------------------------
# IPR Protection Alert System
# نظام التنبيه لحماية حقوق الملكية الفكرية
# -------------------------------------------------------------------

import sys, os
os.chdir('/www/server/panel')
sys.path.append("class/")
import os, sys, re, public, json, hashlib
from datetime import datetime

_title = 'IPR Protection Alert System'
_version = 1.0
_ps = "Monitors and alerts on intellectual property rights violations"
_level = 3  # 风险级别： 3.危险(高)
_date = '2025-10-03'
_ignore = os.path.exists("data/warning/ignore/sw_ipr_protection.pl")
_tips = [
    "Monitor license file modifications",
    "Track plugin integrity",
    "Alert on unauthorized access to protected files",
    "Log all IPR-related security events"
]
_help = 'This system protects intellectual property by monitoring critical files'

# الملفات المحمية (حقوق الملكية الفكرية)
PROTECTED_FILES = [
    'data/userInfo.json',           # معلومات المستخدم والترخيص
    'data/product_list.pl',         # قائمة المنتجات المرخصة
    'data/product_bay.pl',          # بيانات المنتجات المشتراة
    'class/PluginLoader.*.so',      # ملفات Plugin المشفرة
    'class/public/authorization.py', # نظام التفويض
    'class/panelAuth.py',           # نظام المصادقة
]

def calculate_file_hash(filepath):
    """حساب hash للملف لاكتشاف التعديلات"""
    if not os.path.exists(filepath):
        return None
    
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def check_license_integrity():
    """فحص سلامة ملفات الترخيص"""
    violations = []
    
    # فحص ملف معلومات المستخدم
    user_info_file = 'data/userInfo.json'
    if os.path.exists(user_info_file):
        try:
            with open(user_info_file, 'r') as f:
                data = json.load(f)
                
            # التحقق من وجود الحقول الأساسية
            required_fields = ['token', 'server_id', 'id']
            for field in required_fields:
                if field not in data:
                    violations.append(f"License file missing required field: {field}")
                    
        except Exception as e:
            violations.append(f"License file corrupted: {str(e)}")
    else:
        violations.append("License file not found - possible theft attempt")
    
    return violations

def check_plugin_integrity():
    """فحص سلامة ملفات الـ Plugins"""
    violations = []
    
    plugin_patterns = [
        'class/PluginLoader.*.so',
        'class/public/PluginLoader.py'
    ]
    
    for pattern in plugin_patterns:
        import glob
        files = glob.glob(pattern)
        for file in files:
            if os.path.exists(file):
                # التحقق من الصلاحيات
                stat_info = os.stat(file)
                mode = oct(stat_info.st_mode)[-3:]
                
                # ملفات .so يجب أن تكون 755 أو أقل
                if file.endswith('.so') and int(mode) > 755:
                    violations.append(f"Plugin file has suspicious permissions: {file} ({mode})")
    
    return violations

def check_unauthorized_access():
    """فحص محاولات الوصول غير المصرح بها"""
    violations = []
    log_file = 'logs/panel.log'
    
    if os.path.exists(log_file):
        try:
            # قراءة آخر 1000 سطر من السجل
            with open(log_file, 'r') as f:
                lines = f.readlines()[-1000:]
            
            # البحث عن أنماط مشبوهة
            suspicious_patterns = [
                r'unauthorized.*license',
                r'crack.*plugin',
                r'bypass.*auth',
                r'steal.*key',
                r'copy.*license'
            ]
            
            for line in lines:
                for pattern in suspicious_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append(f"Suspicious activity detected in logs: {line.strip()[:100]}")
                        
        except Exception as e:
            violations.append(f"Error reading security logs: {str(e)}")
    
    return violations

def log_ipr_violation(violation_type, details):
    """تسجيل انتهاك حقوق الملكية الفكرية"""
    log_dir = 'logs/ipr_violations'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"ipr_violations_{datetime.now().strftime('%Y%m%d')}.log")
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': violation_type,
        'details': details,
        'severity': 'HIGH'
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

def send_alert(violations):
    """إرسال تنبيه عن الانتهاكات"""
    if not violations:
        return
    
    # محاولة إرسال تنبيه عبر نظام Push
    try:
        import sys
        sys.path.append('/www/server/panel/mod/base/push_mod')
        from system import push_by_task_keyword
        
        message = "⚠️ IPR VIOLATION DETECTED\n\n" + "\n".join(violations)
        push_by_task_keyword('ipr_violation', message)
    except Exception as e:
        # تسجيل الخطأ
        log_ipr_violation('alert_failed', str(e))

def check_run():
    """الفحص الرئيسي"""
    all_violations = []
    
    # 1. فحص سلامة الترخيص
    license_violations = check_license_integrity()
    if license_violations:
        all_violations.extend(license_violations)
        log_ipr_violation('license_integrity', license_violations)
    
    # 2. فحص سلامة الـ Plugins
    plugin_violations = check_plugin_integrity()
    if plugin_violations:
        all_violations.extend(plugin_violations)
        log_ipr_violation('plugin_integrity', plugin_violations)
    
    # 3. فحص الوصول غير المصرح
    access_violations = check_unauthorized_access()
    if access_violations:
        all_violations.extend(access_violations)
        log_ipr_violation('unauthorized_access', access_violations)
    
    # إرسال تنبيه إذا كانت هناك انتهاكات
    if all_violations:
        send_alert(all_violations)
        return False, "🚨 IPR VIOLATIONS DETECTED:\n" + "\n".join(all_violations[:5])
    
    return True, "✅ No IPR violations detected"

# للاختبار المباشر
if __name__ == "__main__":
    status, message = check_run()
    print(f"Status: {'SAFE' if status else 'VIOLATION'}")
    print(f"Message: {message}")
