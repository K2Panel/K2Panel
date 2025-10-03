
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
from pathlib import Path
from collections import defaultdict

class ImageUsageReporter:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.bmp'}
        self.code_extensions = {'.py', '.html', '.js', '.css', '.vue', '.jsx', '.tsx', '.json'}
        self.images = []
        self.image_usage = defaultdict(list)
        
    def find_all_images(self):
        """البحث عن جميع ملفات الصور"""
        exclude_dirs = {'pyenv', 'node_modules', '.git', '__pycache__', 'venv', '.venv'}
        
        for root, dirs, files in os.walk(self.root_dir):
            # تخطي المجلدات المستبعدة
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.image_extensions:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.root_dir)
                    self.images.append({
                        'path': rel_path,
                        'name': file,
                        'size': os.path.getsize(full_path),
                        'ext': ext
                    })
    
    def search_image_usage(self):
        """البحث عن استخدام الصور في الملفات"""
        exclude_dirs = {'pyenv', 'node_modules', '.git', '__pycache__', 'venv', '.venv', 'backups'}
        
        # أنماط البحث عن الصور
        patterns = [
            r'["\']([^"\']*\.(png|jpg|jpeg|gif|svg|ico|webp|bmp))["\']',  # "image.png" or 'image.png'
            r'url\(["\']?([^"\'()]*\.(png|jpg|jpeg|gif|svg|ico|webp|bmp))["\']?\)',  # url(image.png)
            r'src=["\']([^"\']*\.(png|jpg|jpeg|gif|svg|ico|webp|bmp))["\']',  # src="image.png"
            r'background(?:-image)?:\s*url\(["\']?([^"\'()]*\.(png|jpg|jpeg|gif|svg|ico|webp|bmp))["\']?\)',
            r'<img[^>]+src=["\']([^"\']*)["\']',  # <img src="">
            r'icon\.png|logo\.png|\.svg|\.ico',  # أسماء شائعة
        ]
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.code_extensions:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            
                        for line_num, line in enumerate(lines, 1):
                            for pattern in patterns:
                                matches = re.finditer(pattern, line, re.IGNORECASE)
                                for match in matches:
                                    image_ref = match.group(1) if match.lastindex >= 1 else match.group(0)
                                    
                                    # تنظيف المسار
                                    image_ref = image_ref.strip('\'"')
                                    
                                    self.image_usage[image_ref].append({
                                        'file': rel_path,
                                        'line': line_num,
                                        'context': line.strip()[:100]
                                    })
                    except Exception as e:
                        print(f"خطأ في قراءة {rel_path}: {e}")
    
    def generate_report(self):
        """إنشاء التقرير المفصل"""
        report = {
            'summary': {
                'total_images': len(self.images),
                'total_references': sum(len(refs) for refs in self.image_usage.values()),
                'unique_image_paths': len(self.image_usage)
            },
            'images': self.images,
            'usage': {}
        }
        
        # ترتيب الاستخدامات
        for img_path, usages in sorted(self.image_usage.items()):
            report['usage'][img_path] = usages
        
        # حفظ التقرير JSON
        with open('image_usage_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # إنشاء تقرير نصي
        with open('image_usage_report.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("تقرير شامل عن استخدام الصور في التطبيق\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"إجمالي الصور المكتشفة: {report['summary']['total_images']}\n")
            f.write(f"إجمالي الإشارات للصور: {report['summary']['total_references']}\n")
            f.write(f"عدد مسارات الصور الفريدة المستخدمة: {report['summary']['unique_image_paths']}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("1. قائمة جميع الصور في المشروع\n")
            f.write("=" * 80 + "\n\n")
            
            for img in sorted(self.images, key=lambda x: x['path']):
                f.write(f"الصورة: {img['path']}\n")
                f.write(f"  - الاسم: {img['name']}\n")
                f.write(f"  - الحجم: {img['size']:,} بايت\n")
                f.write(f"  - النوع: {img['ext']}\n\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("2. استخدام الصور في الملفات\n")
            f.write("=" * 80 + "\n\n")
            
            for img_path, usages in sorted(self.image_usage.items()):
                f.write(f"\nالصورة: {img_path}\n")
                f.write(f"عدد الاستخدامات: {len(usages)}\n")
                f.write("-" * 80 + "\n")
                
                for usage in usages:
                    f.write(f"  الملف: {usage['file']}\n")
                    f.write(f"  السطر: {usage['line']}\n")
                    f.write(f"  السياق: {usage['context']}\n\n")
        
        # إنشاء تقرير HTML
        self.generate_html_report(report)
        
        print("✅ تم إنشاء التقرير بنجاح!")
        print("📄 الملفات المنشأة:")
        print("  - image_usage_report.json")
        print("  - image_usage_report.txt")
        print("  - image_usage_report.html")
    
    def generate_html_report(self, report):
        """إنشاء تقرير HTML"""
        html = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير استخدام الصور</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            color: #667eea;
        }
        .summary-card .number {
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .image-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-right: 4px solid #667eea;
        }
        .usage-item {
            background: #e9ecef;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            background: #667eea;
            color: white;
            border-radius: 3px;
            font-size: 12px;
            margin: 0 5px;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .path {
            color: #764ba2;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 تقرير شامل عن استخدام الصور في التطبيق</h1>
        <p>تم إنشاء هذا التقرير تلقائياً</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>🖼️ إجمالي الصور</h3>
            <div class="number">""" + str(report['summary']['total_images']) + """</div>
        </div>
        <div class="summary-card">
            <h3>🔗 إجمالي الإشارات</h3>
            <div class="number">""" + str(report['summary']['total_references']) + """</div>
        </div>
        <div class="summary-card">
            <h3>📁 مسارات فريدة</h3>
            <div class="number">""" + str(report['summary']['unique_image_paths']) + """</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📁 جميع الصور في المشروع</h2>
"""
        
        for img in sorted(report['images'], key=lambda x: x['path']):
            html += f"""
        <div class="image-item">
            <div class="path">{img['path']}</div>
            <div>
                <span class="badge">{img['ext']}</span>
                <span class="badge">{img['size']:,} بايت</span>
            </div>
        </div>
"""
        
        html += """
    </div>
    
    <div class="section">
        <h2>🔍 استخدام الصور في الملفات</h2>
"""
        
        for img_path, usages in sorted(report['usage'].items()):
            html += f"""
        <div class="image-item">
            <div class="path">{img_path}</div>
            <div><span class="badge">{len(usages)} استخدام</span></div>
"""
            for usage in usages:
                html += f"""
            <div class="usage-item">
                <div>📄 <strong>الملف:</strong> <code>{usage['file']}</code></div>
                <div>📍 <strong>السطر:</strong> {usage['line']}</div>
                <div>💬 <strong>السياق:</strong> <code>{usage['context']}</code></div>
            </div>
"""
            html += """
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open('image_usage_report.html', 'w', encoding='utf-8') as f:
            f.write(html)

def main():
    print("🔍 جاري البحث عن الصور...")
    reporter = ImageUsageReporter()
    
    print("📸 البحث عن ملفات الصور...")
    reporter.find_all_images()
    
    print("🔎 البحث عن استخدام الصور في الملفات...")
    reporter.search_image_usage()
    
    print("📝 إنشاء التقرير...")
    reporter.generate_report()
    
    print("\n✨ تم إكمال المهمة بنجاح!")

if __name__ == "__main__":
    main()
