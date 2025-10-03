
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت التحقق من جاهزية K2Panel للنشر
يتحقق من جميع المتطلبات الأساسية
"""

import os
import sys
from pathlib import Path

def check_environment_files():
    """التحقق من وجود ملفات البيئة المطلوبة"""
    print("🔍 التحقق من ملفات البيئة...")
    
    required_files = [
        '.env',
        'config/config.json',
        'environment_detector.py',
        'config_factory.py',
        'runserver.py'
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
            print(f"  ❌ غير موجود: {file}")
        else:
            print(f"  ✅ موجود: {file}")
    
    return len(missing) == 0, missing

def check_python_modules():
    """التحقق من توفر الوحدات المطلوبة"""
    print("\n🔍 التحقق من وحدات Python...")
    
    required_modules = [
        'flask',
        'gevent',
        'psycopg2',
        'redis',
        'dotenv'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"  ✅ متوفر: {module}")
        except ImportError:
            missing.append(module)
            print(f"  ❌ غير متوفر: {module}")
    
    return len(missing) == 0, missing

def check_directories():
    """التحقق من وجود المجلدات المطلوبة"""
    print("\n🔍 التحقق من المجلدات...")
    
    required_dirs = [
        'logs',
        'data',
        'backups',
        'config',
        'class',
        'class_v2'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
            print(f"  ❌ غير موجود: {dir_path}")
        else:
            print(f"  ✅ موجود: {dir_path}")
    
    return len(missing) == 0, missing

def check_deployment_files():
    """التحقق من وجود ملفات النشر"""
    print("\n🔍 التحقق من ملفات النشر...")
    
    deployment_files = {
        'Replit': ['.replit'],
        'Docker': ['Dockerfile', 'docker-compose.yml'],
        'Systemd': ['k2panel.service', 'setup_systemd.sh'],
        'Nginx': ['nginx.conf.template', 'setup_nginx.sh']
    }
    
    results = {}
    for platform, files in deployment_files.items():
        found = sum(1 for f in files if Path(f).exists())
        total = len(files)
        results[platform] = (found, total)
        
        status = "✅" if found == total else "⚠️"
        print(f"  {status} {platform}: {found}/{total} ملفات موجودة")
    
    return results

def main():
    """تشغيل جميع الفحوصات"""
    print("=" * 60)
    print("🚀 فحص جاهزية K2Panel للنشر")
    print("=" * 60)
    
    all_passed = True
    
    # فحص الملفات
    passed, missing = check_environment_files()
    if not passed:
        all_passed = False
        print(f"\n⚠️  ملفات مفقودة: {', '.join(missing)}")
    
    # فحص الوحدات
    passed, missing = check_python_modules()
    if not passed:
        all_passed = False
        print(f"\n⚠️  وحدات مفقودة: {', '.join(missing)}")
        print(f"   تثبيت: pip install {' '.join(missing)}")
    
    # فحص المجلدات
    passed, missing = check_directories()
    if not passed:
        all_passed = False
        print(f"\n⚠️  مجلدات مفقودة: {', '.join(missing)}")
    
    # فحص ملفات النشر
    deployment_results = check_deployment_files()
    
    # النتيجة النهائية
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ التطبيق جاهز للنشر على البيئتين!")
        print("\n📋 خيارات النشر المتاحة:")
        
        for platform, (found, total) in deployment_results.items():
            if found == total:
                print(f"  ✅ {platform}: جاهز ({found}/{total})")
            else:
                print(f"  ⚠️  {platform}: جزئي ({found}/{total})")
        
        print("\n🎯 للتشغيل:")
        print("  - Replit: اضغط على زر Run")
        print("  - محلياً: python3 runserver.py")
        print("  - Docker: docker-compose up -d")
        print("  - VPS: راجع VPS_DEPLOYMENT_GUIDE.md")
    else:
        print("❌ التطبيق غير جاهز بالكامل")
        print("   راجع الأخطاء أعلاه وقم بإصلاحها")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
