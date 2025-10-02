# 🤝 دليل المساهمة - Contributing Guide

<div align="center">

[![K2Panel](https://img.shields.io/badge/K2Panel-K2Panel-blue)](https://github.com/K2Panel/K2Panel)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**مرحباً بك في مجتمع K2Panel! نحن سعداء بمساهمتك 🎉**

Welcome to the K2Panel community! We're excited to have your contribution 🎉

</div>

---

## 📋 جدول المحتويات - Table of Contents

1. [ميثاق السلوك](#-ميثاق-السلوك---code-of-conduct)
2. [كيفية المساهمة](#-كيفية-المساهمة---getting-started)
3. [سير العمل التطويري](#-سير-العمل-التطويري---development-workflow)
4. [معايير البرمجة](#-معايير-البرمجة---coding-standards)
5. [إرشادات Git Commit](#-إرشادات-git-commit)
6. [الاختبارات](#-الاختبارات---testing)
7. [عملية Pull Request](#-عملية-pull-request)
8. [عملية المراجعة](#-عملية-المراجعة---review-process)
9. [البنية التحتية](#-البنية-التحتية---infrastructure)

---

## 📜 ميثاق السلوك - Code of Conduct

### قيمنا الأساسية - Our Core Values

نحن ملتزمون بتوفير بيئة ترحيبية وشاملة للجميع. نتوقع من جميع المساهمين:

We are committed to providing a welcoming and inclusive environment for everyone. We expect all contributors to:

- ✅ **الاحترام المتبادل** - Treat everyone with respect and kindness
- ✅ **التواصل البنّاء** - Engage in constructive and professional communication
- ✅ **قبول النقد البنّاء** - Accept constructive feedback gracefully
- ✅ **التركيز على المصلحة العامة** - Focus on what's best for the community
- ✅ **إظهار التعاطف** - Show empathy towards other community members

### السلوك غير المقبول - Unacceptable Behavior

- ❌ التحرش أو التمييز بأي شكل - Harassment or discrimination of any kind
- ❌ اللغة المسيئة أو الهجومية - Offensive or abusive language
- ❌ الهجمات الشخصية - Personal attacks
- ❌ التصيد أو التعليقات الاستفزازية - Trolling or inflammatory comments
- ❌ نشر معلومات خاصة دون إذن - Publishing private information without permission

### الإبلاغ - Reporting

إذا واجهت أو شاهدت سلوكاً غير مقبول، يرجى الإبلاغ عنه عبر:

If you experience or witness unacceptable behavior, please report it via:

- 📧 Email: conduct@k2panel.com
- 📝 GitHub Issues (للمشاكل العامة)

---

## 🚀 كيفية المساهمة - Getting Started

### أنواع المساهمات المرحب بها - Types of Contributions

نرحب بجميع أنواع المساهمات:

We welcome all types of contributions:

- 🐛 **إبلاغ عن الأخطاء** - Bug reports
- ✨ **طلبات ميزات جديدة** - Feature requests
- 📝 **تحسين التوثيق** - Documentation improvements
- 🔧 **إصلاح الأخطاء** - Bug fixes
- ⚡ **تحسينات الأداء** - Performance improvements
- 🎨 **تحسينات واجهة المستخدم** - UI/UX improvements
- 🔒 **تحسينات الأمان** - Security enhancements
- 🧪 **إضافة اختبارات** - Adding tests
- 🌍 **الترجمة** - Translations

### قبل البدء - Before You Start

1. **ابحث أولاً** - تحقق من Issues و Pull Requests الموجودة
   - Search first - Check existing Issues and Pull Requests

2. **أنشئ Issue أولاً** - للميزات الكبيرة، ناقش فكرتك أولاً
   - Create an Issue first - For major features, discuss your idea first

3. **اقرأ الأدلة** - تأكد من قراءة هذا الدليل و DEVELOPER_GUIDE.md
   - Read the guides - Make sure to read this guide and DEVELOPER_GUIDE.md

4. **اطلع على الكود** - افهم بنية المشروع الحالية
   - Review the code - Understand the current project structure

---

## 🔄 سير العمل التطويري - Development Workflow

### 1️⃣ Fork المشروع - Fork the Repository

```bash
# انتقل إلى صفحة المشروع على GitHub واضغط "Fork"
# Go to the project page on GitHub and click "Fork"
https://github.com/K2Panel/K2Panel

# ثم استنسخ fork الخاص بك
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/K2Panel.git
cd K2Panel
```

### 2️⃣ أضف Remote للمشروع الأصلي - Add Upstream Remote

```bash
# أضف المشروع الأصلي كـ upstream
# Add the original repository as upstream
git remote add upstream https://github.com/K2Panel/K2Panel.git

# تحقق من الـ remotes
# Verify remotes
git remote -v
```

### 3️⃣ أنشئ فرع جديد - Create a New Branch

```bash
# حدّث فرع main من upstream
# Update your main branch from upstream
git checkout main
git pull upstream main

# أنشئ فرع جديد للميزة/الإصلاح
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# أو للإصلاح - or for a fix
git checkout -b fix/issue-description
```

**تسمية الفروع - Branch Naming Convention:**

```
feature/add-user-authentication     # ميزة جديدة - New feature
fix/database-connection-bug         # إصلاح خطأ - Bug fix
docs/update-api-documentation       # توثيق - Documentation
refactor/improve-config-factory     # إعادة هيكلة - Refactoring
test/add-unit-tests                 # اختبارات - Tests
security/fix-sql-injection          # أمان - Security
perf/optimize-database-queries      # أداء - Performance
```

### 4️⃣ قم بالتعديلات - Make Your Changes

```bash
# قم بتعديلاتك على الكود
# Make your code changes

# اتبع معايير البرمجة المذكورة أدناه
# Follow the coding standards mentioned below
```

### 5️⃣ اختبر تعديلاتك - Test Your Changes

```bash
# شغّل الاختبارات
# Run tests
pytest

# تحقق من التغطية
# Check coverage
pytest --cov=. --cov-report=html

# شغّل linting
# Run linting
flake8 .
black --check .
```

### 6️⃣ Commit التعديلات - Commit Your Changes

```bash
# أضف الملفات المعدلة
# Stage your changes
git add .

# أنشئ commit باتباع الإرشادات أدناه
# Create a commit following the guidelines below
git commit -m "feat: add user authentication feature"
```

### 7️⃣ Push إلى Fork الخاص بك - Push to Your Fork

```bash
# ادفع الفرع إلى fork الخاص بك
# Push the branch to your fork
git push origin feature/your-feature-name
```

### 8️⃣ أنشئ Pull Request - Create a Pull Request

1. انتقل إلى fork الخاص بك على GitHub
   - Go to your fork on GitHub

2. اضغط "Compare & pull request"
   - Click "Compare & pull request"

3. املأ قالب PR (انظر القسم أدناه)
   - Fill in the PR template (see section below)

4. اضغط "Create pull request"
   - Click "Create pull request"

---

## 📝 معايير البرمجة - Coding Standards

### Python Style Guide

نتبع **PEP 8** مع بعض التخصيصات:

We follow **PEP 8** with some customizations:

#### 1️⃣ تنسيق الكود - Code Formatting

```python
# استخدم Black للتنسيق التلقائي
# Use Black for automatic formatting

# تثبيت Black
# Install Black
pip install black

# تشغيل Black
# Run Black
black .

# التحقق فقط (بدون تعديل)
# Check only (without modifying)
black --check .
```

**إعدادات Black:**
```toml
# pyproject.toml أو .black.toml
[tool.black]
line-length = 120
target-version = ['py312']
include = '\.pyi?$'
```

#### 2️⃣ Linting مع Flake8

```bash
# تثبيت Flake8
# Install Flake8
pip install flake8

# تشغيل Flake8
# Run Flake8
flake8 .

# مع تقرير مفصل
# With detailed report
flake8 --statistics --show-source .
```

**إعدادات Flake8** (من `.flake8`):
```ini
[flake8]
max-line-length = 120
ignore = E203, E501, W503, W504
exclude = .git, __pycache__, pyenv/, BTPanel/, class/
max-complexity = 15
```

#### 3️⃣ Type Hints

استخدم Type hints حيثما أمكن:

Use Type hints wherever possible:

```python
# ✅ جيد - Good
def calculate_total(price: float, quantity: int) -> float:
    """
    حساب الإجمالي - Calculate total
    
    Args:
        price (float): السعر - Price
        quantity (int): الكمية - Quantity
    
    Returns:
        float: الإجمالي - Total
    """
    return price * quantity

# ❌ سيء - Bad
def calculate_total(price, quantity):
    return price * quantity
```

**Type hints متقدمة:**
```python
from typing import List, Dict, Optional, Union, Tuple, Any

def process_users(
    users: List[Dict[str, Any]], 
    filter_by: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """معالجة قائمة المستخدمين - Process users list"""
    # ...
    return filtered_users, count
```

#### 4️⃣ Docstrings

اكتب docstrings بالعربية والإنجليزية:

Write docstrings in both Arabic and English:

```python
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    مصادقة المستخدم - Authenticate User
    
    يتحقق من بيانات اعتماد المستخدم ويُرجع معلومات الجلسة
    Verifies user credentials and returns session information
    
    Args:
        username (str): اسم المستخدم - Username
        password (str): كلمة المرور - Password
    
    Returns:
        Optional[Dict[str, Any]]: 
            معلومات المستخدم إذا نجحت المصادقة، None خلاف ذلك
            User information if authentication succeeds, None otherwise
    
    Raises:
        ValueError: إذا كانت المدخلات فارغة - If inputs are empty
        DatabaseError: إذا فشل الاتصال بقاعدة البيانات - If database connection fails
    
    Example:
        >>> user = authenticate_user("admin", "secure_password")
        >>> if user:
        ...     print(f"Welcome {user['name']}")
    """
    if not username or not password:
        raise ValueError("Username and password are required")
    
    # المنطق هنا...
    # Logic here...
    pass
```

**تنسيق الـ Docstrings:**
- استخدم Google Style أو NumPy Style
- Use Google Style or NumPy Style
- أضف أمثلة عملية للدوال المعقدة
- Add practical examples for complex functions

#### 5️⃣ تسمية المتغيرات - Variable Naming

```python
# استخدم snake_case للمتغيرات والدوال
# Use snake_case for variables and functions
user_name = "admin"
total_price = 100.50

def calculate_discount(price: float) -> float:
    pass

# استخدم PascalCase للفئات
# Use PascalCase for classes
class UserAuthentication:
    pass

# استخدم UPPER_CASE للثوابت
# Use UPPER_CASE for constants
MAX_LOGIN_ATTEMPTS = 3
DATABASE_TIMEOUT = 30
```

#### 6️⃣ Imports

```python
# ترتيب الـ Imports - Import ordering:
# 1. المكتبات القياسية - Standard library
import os
import sys
from typing import Optional, List

# 2. مكتبات الطرف الثالث - Third-party libraries
import flask
from flask import request, jsonify
import pymysql

# 3. المكتبات المحلية - Local modules
from config_factory import get_config
from environment_detector import detect_environment

# استخدم isort لترتيب تلقائي
# Use isort for automatic sorting
# pip install isort
# isort .
```

#### 7️⃣ أفضل الممارسات - Best Practices

```python
# ✅ استخدم context managers
# ✅ Use context managers
with open('file.txt', 'r') as f:
    content = f.read()

# ✅ استخدم list comprehensions بحكمة
# ✅ Use list comprehensions wisely
squares = [x**2 for x in range(10)]

# ✅ تعامل مع الاستثناءات بشكل محدد
# ✅ Handle exceptions specifically
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except DatabaseError as e:
    logger.error(f"Database error: {e}")

# ❌ تجنب bare except
# ❌ Avoid bare except
try:
    result = risky_operation()
except:  # سيء - Bad!
    pass
```

### Security Guidelines - إرشادات الأمان

```python
# ✅ لا تكتب أسرار في الكود مباشرة
# ✅ Don't hardcode secrets
SECRET_KEY = os.environ.get('SECRET_KEY')

# ✅ استخدم parameterized queries
# ✅ Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✅ تحقق من المدخلات
# ✅ Validate inputs
from werkzeug.utils import secure_filename
filename = secure_filename(uploaded_file.filename)

# ✅ استخدم hashing للكلمات السرية
# ✅ Use hashing for passwords
import bcrypt
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

---

## 💬 إرشادات Git Commit

نستخدم **Conventional Commits** لرسائل الـ commit:

We use **Conventional Commits** for commit messages:

### التنسيق - Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### الأنواع - Types

| Type | العربية | الاستخدام - Usage |
|------|---------|-------------------|
| `feat` | ميزة | ميزة جديدة - New feature |
| `fix` | إصلاح | إصلاح خطأ - Bug fix |
| `docs` | توثيق | تغييرات في التوثيق - Documentation changes |
| `style` | تنسيق | تنسيق الكود (لا يؤثر على المنطق) - Code formatting |
| `refactor` | إعادة هيكلة | إعادة هيكلة الكود - Code refactoring |
| `perf` | أداء | تحسين الأداء - Performance improvement |
| `test` | اختبار | إضافة/تعديل اختبارات - Adding/modifying tests |
| `build` | بناء | تغييرات في نظام البناء - Build system changes |
| `ci` | CI/CD | تغييرات في CI/CD - CI/CD changes |
| `chore` | صيانة | مهام صيانة أخرى - Other maintenance tasks |
| `revert` | تراجع | التراجع عن commit سابق - Revert previous commit |
| `security` | أمان | إصلاحات أمنية - Security fixes |

### أمثلة - Examples

```bash
# ميزة جديدة - New feature
git commit -m "feat(auth): add two-factor authentication support"

# إصلاح خطأ - Bug fix
git commit -m "fix(database): resolve connection pool timeout issue"

# توثيق - Documentation
git commit -m "docs(api): update API endpoints documentation"

# أمان - Security
git commit -m "security(sql): prevent SQL injection in user queries"

# أداء - Performance
git commit -m "perf(cache): implement Redis caching for user sessions"

# اختبارات - Tests
git commit -m "test(auth): add unit tests for login functionality"
```

### Commit Message مفصل - Detailed Commit

```bash
git commit -m "feat(backup): add automated backup with SHA-256 verification

- إضافة نظام backup تلقائي يعمل كل 6 ساعات
- Add automated backup system running every 6 hours
- التحقق من سلامة النسخ الاحتياطية باستخدام SHA-256
- Verify backup integrity using SHA-256
- دعم التخزين السحابي (S3, GCS)
- Support cloud storage (S3, GCS)

Closes #123
Relates to #124"
```

### القواعد - Rules

1. ✅ استخدم الفعل المضارع - Use imperative mood: "add" not "added"
2. ✅ لا تنهِ بنقطة - Don't end with a period
3. ✅ حافظ على السطر الأول أقل من 72 حرف - Keep first line under 72 characters
4. ✅ أضف تفاصيل في الـ body إذا لزم - Add details in body if needed
5. ✅ اذكر رقم الـ issue ذي الصلة - Reference related issue numbers

---

## 🧪 الاختبارات - Testing

### متطلبات الاختبار - Testing Requirements

1. ✅ **اكتب اختبارات لكل feature جديد**
   - Write tests for every new feature

2. ✅ **تغطية الكود > 80%**
   - Code coverage > 80%

3. ✅ **اختبارات Unit + Integration**
   - Unit tests + Integration tests

### تشغيل الاختبارات - Running Tests

```bash
# تثبيت مكتبات الاختبار
# Install test dependencies
pip install -r requirements-dev.txt

# تشغيل جميع الاختبارات
# Run all tests
pytest

# تشغيل مع التغطية
# Run with coverage
pytest --cov=. --cov-report=html

# تشغيل اختبارات محددة
# Run specific tests
pytest tests/test_auth.py
pytest tests/test_auth.py::test_login

# تشغيل حسب markers
# Run by markers
pytest -m unit          # اختبارات unit فقط
pytest -m integration   # اختبارات integration فقط
pytest -m "not slow"    # تجاهل الاختبارات البطيئة
```

### كتابة الاختبارات - Writing Tests

```python
# tests/test_auth.py
import pytest
from BTPanel.auth import authenticate_user

class TestAuthentication:
    """اختبارات نظام المصادقة - Authentication system tests"""
    
    def test_login_success(self):
        """اختبار تسجيل دخول ناجح - Test successful login"""
        user = authenticate_user("admin", "correct_password")
        assert user is not None
        assert user['username'] == "admin"
    
    def test_login_wrong_password(self):
        """اختبار كلمة مرور خاطئة - Test wrong password"""
        user = authenticate_user("admin", "wrong_password")
        assert user is None
    
    def test_login_empty_credentials(self):
        """اختبار بيانات فارغة - Test empty credentials"""
        with pytest.raises(ValueError):
            authenticate_user("", "")
    
    @pytest.mark.slow
    def test_brute_force_protection(self):
        """اختبار الحماية من الهجمات - Test brute force protection"""
        # هذا اختبار بطيء
        # This is a slow test
        pass
```

### تقرير التغطية - Coverage Report

```bash
# إنشاء تقرير HTML
# Generate HTML report
pytest --cov=. --cov-report=html

# عرض التقرير
# View the report
open htmlcov/index.html

# تقرير في Terminal
# Terminal report
pytest --cov=. --cov-report=term-missing
```

---

## 🔀 عملية Pull Request

### قبل إنشاء PR - Before Creating a PR

- ✅ تأكد من نجاح جميع الاختبارات - Ensure all tests pass
- ✅ تأكد من عدم وجود أخطاء linting - Ensure no linting errors
- ✅ تأكد من تحديث التوثيق - Ensure documentation is updated
- ✅ تأكد من إضافة اختبارات للكود الجديد - Ensure new code has tests
- ✅ حدّث فرعك من upstream/main - Update your branch from upstream/main

```bash
# حدّث فرعك
# Update your branch
git checkout main
git pull upstream main
git checkout feature/your-feature
git rebase main
```

### قالب PR Template

عند إنشاء PR، استخدم القالب التالي:

When creating a PR, use the following template:

```markdown
## 📝 الوصف - Description

وصف مختصر للتغييرات
Brief description of the changes

## 🎯 نوع التغيير - Type of Change

- [ ] 🐛 Bug fix (إصلاح خطأ)
- [ ] ✨ New feature (ميزة جديدة)
- [ ] 📝 Documentation (توثيق)
- [ ] ⚡ Performance (تحسين أداء)
- [ ] 🔒 Security (أمان)
- [ ] 🧪 Tests (اختبارات)

## 🔗 القضايا ذات الصلة - Related Issues

Closes #123
Relates to #124

## ✅ Checklist

- [ ] تم تشغيل الاختبارات بنجاح - Tests pass
- [ ] تم تشغيل linting بنجاح - Linting passes
- [ ] تم تحديث التوثيق - Documentation updated
- [ ] تم إضافة اختبارات - Tests added
- [ ] التغطية > 80% - Coverage > 80%
- [ ] لا توجد breaking changes - No breaking changes

## 📸 لقطات الشاشة - Screenshots (إن وجدت)

إذا كان هناك تغييرات في الواجهة
If there are UI changes

## 📌 ملاحظات إضافية - Additional Notes

أي ملاحظات أخرى للمراجعين
Any other notes for reviewers
```

### حجم PR - PR Size

- ✅ **صغير ومحدد** - Small and focused
- ✅ **تغيير واحد في كل مرة** - One change at a time
- ✅ **أقل من 400 سطر (مثالي)** - Less than 400 lines (ideal)
- ⚠️ **أكثر من 1000 سطر** - قسّمها إلى PRs أصغر
  - More than 1000 lines - Split into smaller PRs

---

## 👀 عملية المراجعة - Review Process

### للمساهمين - For Contributors

بعد إنشاء PR:

After creating a PR:

1. ✅ **انتظر المراجعة** - Wait for review (عادة 1-3 أيام - usually 1-3 days)
2. ✅ **رد على التعليقات** - Respond to comments
3. ✅ **قم بالتعديلات المطلوبة** - Make requested changes
4. ✅ **طلب مراجعة إضافية** - Request re-review

### للمراجعين - For Reviewers

عند مراجعة PR:

When reviewing a PR:

1. ✅ **تحقق من الكود** - Review the code
   - هل يتبع معايير البرمجة؟ - Does it follow coding standards?
   - هل هو مفهوم وواضح؟ - Is it clear and understandable?
   - هل هناك مشاكل أمنية؟ - Are there security issues?

2. ✅ **تحقق من الاختبارات** - Check tests
   - هل الاختبارات كافية؟ - Are tests sufficient?
   - هل جميع الاختبارات تنجح؟ - Do all tests pass?
   - هل التغطية > 80%؟ - Is coverage > 80%?

3. ✅ **تحقق من التوثيق** - Check documentation
   - هل التوثيق محدث؟ - Is documentation updated?
   - هل docstrings واضحة؟ - Are docstrings clear?

4. ✅ **اختبر محلياً** - Test locally
   - استنسخ الفرع واختبره - Clone the branch and test it
   - تحقق من عدم وجود breaking changes - Check for breaking changes

### معايير القبول - Acceptance Criteria

سيتم قبول PR إذا:

A PR will be accepted if:

- ✅ جميع الاختبارات تنجح - All tests pass
- ✅ لا توجد أخطاء linting - No linting errors
- ✅ التغطية > 80% - Coverage > 80%
- ✅ التوثيق محدث - Documentation updated
- ✅ لا توجد مشاكل أمنية - No security issues
- ✅ موافقة مراجع واحد على الأقل - At least one reviewer approval

---

## 🏗️ البنية التحتية - Infrastructure

### Docker Configuration

عند تعديل Docker:

When modifying Docker:

```bash
# اختبر Docker build
# Test Docker build
docker build -t k2panel-test .

# اختبر docker-compose
# Test docker-compose
docker-compose up --build

# اختبر override للتطوير
# Test override for development
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

### CI/CD Workflows

عند تعديل GitHub Actions:

When modifying GitHub Actions:

```bash
# الملفات في
# Files in: .github/workflows/

# اختبر محلياً باستخدام act (اختياري)
# Test locally using act (optional)
act -j test
```

**Workflows الموجودة:**
- `ci.yml` - اختبارات ولinting لكل PR
- `deploy.yml` - نشر تلقائي للإنتاج
- `security.yml` - فحص أمني أسبوعي

### Documentation

عند تحديث التوثيق:

When updating documentation:

- ✅ حدّث README.md إذا لزم - Update README.md if needed
- ✅ حدّث DEVELOPER_GUIDE.md للتعليمات التطويرية - Update DEVELOPER_GUIDE.md for dev instructions
- ✅ حدّث DEPLOYMENT.md لإجراءات النشر - Update DEPLOYMENT.md for deployment procedures
- ✅ أضف تعليقات في الكود - Add comments in code
- ✅ حدّث docstrings - Update docstrings

---

## 🙏 شكراً لك - Thank You!

شكراً لك على مساهمتك في K2Panel! 🎉

Thank you for contributing to K2Panel! 🎉

نحن نقدّر وقتك وجهدك في تحسين هذا المشروع.

We appreciate your time and effort in improving this project.

### الموارد المفيدة - Useful Resources

- 📖 [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - دليل المطورين
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - دليل النشر
- 🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - استكشاف الأخطاء
- 📝 [README.md](README.md) - نظرة عامة على المشروع

### اتصل بنا - Contact Us

- 💬 GitHub Discussions: https://github.com/K2Panel/K2Panel/discussions
- 📧 Email: support@k2panel.com
- 🌐 Website: https://www.k2panel.com
- 📖 Documentation: https://doc.k2panel.com

---

<div align="center">

**صُنع بـ ❤️ من قبل مجتمع K2Panel**

**Made with ❤️ by the K2Panel Community**

</div>
