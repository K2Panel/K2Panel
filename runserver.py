#coding: utf-8
# +-------------------------------------------------------------------
# | K2Panel
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 K2Panel(binarjoinanalyticnl.nl) All rights reserved.
# +-------------------------------------------------------------------
# | Author: hwliang <hwl@binarjoinanalyticnl.nl>
# +-------------------------------------------------------------------
import sys
import os
from os import environ

# Add required paths to sys.path before importing BTPanel
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if os.path.join(current_dir, 'class') not in sys.path:
    sys.path.insert(0, os.path.join(current_dir, 'class'))
if os.path.join(current_dir, 'class_v2') not in sys.path:
    sys.path.insert(0, os.path.join(current_dir, 'class_v2'))

from BTPanel import app
from config_factory import get_config
from environment_detector import detect_environment

if __name__ == '__main__':
    # كشف البيئة وتحميل الإعدادات المناسبة
    env_info = detect_environment()
    config = get_config()
    
    # استخدام HOST و PORT من الإعدادات
    HOST = config.HOST
    PORT = config.PORT
    
    # طباعة معلومات التشغيل
    print(f"=" * 60)
    print(f"🚀 بدء تشغيل K2Panel")
    print(f"=" * 60)
    print(f"البيئة المكتشفة: {env_info['platform']}")
    print(f"البيئة المعدة: {config.ENVIRONMENT}")
    print(f"المضيف: {HOST}")
    print(f"المنفذ: {PORT}")
    print(f"وضع التصحيح: {config.DEBUG if hasattr(config, 'DEBUG') else False}")
    
    if env_info['is_replit']:
        print(f"✅ تشغيل على Replit")
        print(f"   URL: https://{os.getenv('REPL_SLUG', 'app')}.{os.getenv('REPL_OWNER', 'user')}.repl.co")
    elif env_info['is_vps']:
        print(f"✅ تشغيل على VPS")
        if config.ENVIRONMENT == 'production':
            print(f"   ⚠️  تذكير: استخدم Nginx كـ reverse proxy في الإنتاج")
    
    print(f"=" * 60)
    
    # تشغيل التطبيق
    try:
        app.run(host=HOST, port=PORT, debug=config.DEBUG if hasattr(config, 'DEBUG') else False)
    except Exception as e:
        print(f"❌ فشل تشغيل التطبيق: {e}")
        sys.exit(1)
