#!/usr/bin/env python3
# coding: utf-8
"""
سكريبت تنظيف ملفات .info القديمة
Legacy Info Files Cleanup Script

يصلح ملفات .info ذات التسمية الخاطئة (.tar.tar.gz.info → .tar.gz.info)
Fixes incorrectly named .info files
"""

import os
import sys
from pathlib import Path


def main():
    """إصلاح ملفات .info القديمة"""

    backups_dir = Path(__file__).parent

    print("\n" + "=" * 70)
    print("🔧 تنظيف ملفات .info القديمة | Legacy Info Files Cleanup")
    print("=" * 70 + "\n")

    # البحث عن ملفات .tar.tar.gz.info
    legacy_files = list(backups_dir.glob("*.tar.tar.gz.info"))

    if not legacy_files:
        print("✅ لا توجد ملفات .info قديمة تحتاج إصلاح")
        print("   No legacy .info files found\n")
        return 0

    print(f"🔍 تم العثور على {len(legacy_files)} ملف .info قديم:\n")

    fixed_count = 0
    error_count = 0

    for old_file in legacy_files:
        # الاسم الصحيح: إزالة .tar الزائد
        correct_name = str(old_file).replace(".tar.tar.gz.info", ".tar.gz.info")
        new_file = Path(correct_name)

        try:
            # التحقق من عدم وجود الملف الجديد
            if new_file.exists():
                print(f"⚠️  تخطي {old_file.name} - الملف الصحيح موجود بالفعل")
                # حذف الملف القديم
                old_file.unlink()
                print(f"   ✓ تم حذف الملف القديم")
            else:
                # إعادة التسمية
                old_file.rename(new_file)
                print(f"✅ {old_file.name}")
                print(f"   → {new_file.name}")

            fixed_count += 1

        except Exception as e:
            print(f"❌ خطأ في معالجة {old_file.name}: {e}")
            error_count += 1

    print("\n" + "=" * 70)
    print(f"📊 الملخص | Summary:")
    print(f"   • تم الإصلاح: {fixed_count}")
    print(f"   • أخطاء: {error_count}")
    print("=" * 70 + "\n")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
