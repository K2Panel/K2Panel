
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPR Monitoring Cron Job
مهمة مجدولة لمراقبة حقوق الملكية الفكرية
"""

import sys
import os

# إضافة مسار الـ panel
sys.path.insert(0, '/www/server/panel')
os.chdir('/www/server/panel')

def run_ipr_check():
    """تشغيل فحص حقوق الملكية الفكرية"""
    try:
        # استيراد نظام الفحص
        from class_v2.safe_warning_v2 import sw_ipr_protection
        
        # تشغيل الفحص
        status, message = sw_ipr_protection.check_run()
        
        # طباعة النتيجة
        if not status:
            print(f"⚠️ IPR VIOLATION: {message}")
            return 1
        else:
            print(f"✅ {message}")
            return 0
            
    except Exception as e:
        print(f"❌ Error running IPR check: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = run_ipr_check()
    sys.exit(exit_code)
