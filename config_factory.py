# coding: utf-8
"""
مصنع الإعدادات - Configuration Factory
يوفر نظام إعدادات موحد للتطبيق يدعم بيئات التطوير والإنتاج
"""

import os
import sys
import secrets
from environment_detector import detect_environment, is_production, is_replit


class BaseConfig:
    """
    الإعدادات الأساسية المشتركة بين جميع البيئات
    Base Configuration - Shared settings across all environments
    """

    def __init__(self):
        """تهيئة الإعدادات الأساسية"""
        # الكشف عن البيئة الحالية
        self.ENVIRONMENT = detect_environment()

        # ==================== SECRET KEY ====================
        # المفتاح السري للتطبيق - يستخدم للتشفير والجلسات
        # ملاحظة: في الإنتاج، يجب تعيين SECRET_KEY من المتغيرات
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        if not self.SECRET_KEY:
            self.SECRET_KEY = self._generate_secret_key()
            # تحذير: المفتاح المولد تلقائياً للتطوير فقط
            import warnings

            warnings.warn(
                "SECRET_KEY not set. Using auto-generated key (development only). "
                "This key will change on restart, invalidating sessions.",
                RuntimeWarning,
            )

        # ==================== PORT CONFIGURATION ====================
        # إعدادات المنفذ (Port)
        self.PORT = self._get_port()
        self.HOST = "0.0.0.0"  # الاستماع على جميع الواجهات

        # ==================== SECURITY SETTINGS ====================
        # إعدادات الأمان الأساسية
        self.SESSION_COOKIE_SECURE = False  # سيتم تفعيله في الإنتاج
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = "Lax"
        self.PERMANENT_SESSION_LIFETIME = 3600  # ساعة واحدة

        # ==================== DATABASE CONFIGURATION ====================
        # سيتم تعيين إعدادات قاعدة البيانات في الفئات الفرعية
        self.DATABASE_URI = None
        self.DATABASE_TYPE = None

        # ==================== DATABASE CONNECTION POOL ====================
        # إعدادات Connection Pool للأداء المحسن
        self.DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", "5"))
        self.DB_MAX_OVERFLOW = int(os.environ.get("DB_MAX_OVERFLOW", "10"))
        self.DB_POOL_TIMEOUT = int(os.environ.get("DB_POOL_TIMEOUT", "30"))
        self.DB_POOL_RECYCLE = int(os.environ.get("DB_POOL_RECYCLE", "3600"))
        self.DB_POOL_PRE_PING = (
            os.environ.get("DB_POOL_PRE_PING", "true").lower() == "true"
        )

        # ==================== APPLICATION SETTINGS ====================
        # إعدادات التطبيق العامة
        self.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
        self.JSON_AS_ASCII = False  # دعم UTF-8 في JSON
        self.JSONIFY_PRETTYPRINT_REGULAR = True

    def _generate_secret_key(self):
        """
        توليد مفتاح سري عشوائي آمن

        Returns:
            str: مفتاح سري بطول 32 بايت (64 حرف hex)
        """
        return secrets.token_hex(32)

    def _get_port(self):
        """
        الحصول على رقم المنفذ من المتغيرات أو الملف

        الأولوية:
        1. متغير البيئة PORT (أعلى أولوية)
        2. ملف data/port.pl
        3. القيمة الافتراضية 5000

        Returns:
            int: رقم المنفذ
        """
        # أولاً: فحص متغير البيئة PORT (أعلى أولوية)
        port_env = os.environ.get("PORT")
        if port_env:
            try:
                port = int(port_env)
                print(f"✓ تم قراءة المنفذ من المتغيرات البيئية: {port}")
                return port
            except (ValueError, TypeError) as e:
                print(
                    f"⚠️ قيمة PORT غير صحيحة في المتغيرات البيئية: {port_env}, الخطأ: {e}"
                )

        # ثانياً: قراءة من ملف data/port.pl إن وجد
        port_file = "data/port.pl"
        if os.path.exists(port_file):
            try:
                with open(port_file, "r") as f:
                    port = int(f.read().strip())
                    print(f"✓ تم قراءة المنفذ من الملف {port_file}: {port}")
                    return port
            except (ValueError, TypeError, IOError) as e:
                print(f"⚠️ خطأ في قراءة المنفذ من الملف {port_file}: {e}")

        # افتراضياً: المنفذ 5000
        print(f"ℹ️ استخدام المنفذ الافتراضي: 5000")
        return 5000

    def get_config_dict(self, include_sensitive=False):
        """
        ترجع جميع الإعدادات كقاموس

        Args:
            include_sensitive: إذا كان True، يتضمن المتغيرات الحساسة (غير آمن)
                              يُتجاهل في بيئة الإنتاج لمنع التسريب

        Returns:
            dict: قاموس يحتوي على جميع الإعدادات
        """
        # في الإنتاج، لا نسمح أبداً بتضمين المتغيرات الحساسة
        # التحقق من نوع الكائن بدلاً من ENVIRONMENT لأنه قد يكون محرفاً
        if isinstance(self, ProductionConfig):
            include_sensitive = False

        # المتغيرات الحساسة التي يجب إخفاؤها
        SENSITIVE_KEYS = {
            "SECRET_KEY",
            "DB_PASSWORD",
            "SSL_KEY_PATH",
            "DATABASE_URI",
            "CACHE_REDIS_URL",
        }

        config_dict = {}
        for key in dir(self):
            if key.isupper():
                value = getattr(self, key)
                # إخفاء المتغيرات الحساسة
                if key in SENSITIVE_KEYS and not include_sensitive:
                    if isinstance(value, str):
                        config_dict[key] = f"<redacted:{len(value)} chars>"
                    else:
                        config_dict[key] = "<redacted>"
                else:
                    config_dict[key] = value
        return config_dict

    def __repr__(self):
        """تمثيل نصي للإعدادات"""
        return f"<{self.__class__.__name__} environment={self.ENVIRONMENT}>"


class DevelopmentConfig(BaseConfig):
    """
    إعدادات بيئة التطوير - Development Environment Configuration
    تستخدم في بيئة Replit أو التطوير المحلي
    """

    def __init__(self):
        """تهيئة إعدادات التطوير"""
        super().__init__()

        # ==================== DEBUG MODE ====================
        self.DEBUG = True
        self.TESTING = False

        # ==================== DATABASE CONFIGURATION ====================
        # استخدام SQLite للتطوير (قاعدة بيانات محلية)
        self.DATABASE_TYPE = "sqlite"
        db_path = os.environ.get("DEV_DATABASE_PATH", "data/db/dev_database.db")

        # إنشاء المجلد إذا لم يكن موجوداً
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except OSError:
                # إذا فشل الإنشاء، استخدم المسار الحالي
                db_path = "dev_database.db"

        self.DATABASE_URI = f"sqlite:///{db_path}"

        # ==================== PORT CONFIGURATION ====================
        # في التطوير، استخدم PORT من المتغير أو 5000
        port_from_env = os.environ.get("PORT")
        if port_from_env:
            try:
                self.PORT = int(port_from_env)
            except (ValueError, TypeError):
                self.PORT = 5000
        else:
            self.PORT = self.PORT or 5000

        # ==================== DEVELOPMENT INFO ====================
        # معلومات إضافية للتطوير
        self.DEVELOPMENT_MODE = True
        self.LOG_LEVEL = "DEBUG"
        self.SHOW_SQL_QUERIES = True
        self.AUTO_RELOAD = True

        # ==================== SECURITY (مخففة للتطوير) ====================
        # الأمان أقل صرامة في بيئة التطوير
        self.SESSION_COOKIE_SECURE = False  # HTTP مسموح
        self.REQUIRE_HTTPS = False

        # ==================== CORS للتطوير ====================
        self.CORS_ENABLED = True
        self.CORS_ORIGINS = ["*"]  # السماح لجميع المصادر في التطوير


class ProductionConfig(BaseConfig):
    """
    إعدادات بيئة الإنتاج - Production Environment Configuration
    تستخدم في VPS أو الخوادم الإنتاجية
    """

    def __init__(self):
        """تهيئة إعدادات الإنتاج"""
        # ==================== VALIDATE SECRET_KEY ====================
        # في بيئة الإنتاج، SECRET_KEY إلزامي من المتغيرات
        secret_key = os.environ.get("SECRET_KEY", "").strip()

        # فحص الوجود والفراغ
        if not secret_key:
            raise ValueError(
                "SECRET_KEY must be set in production environment.\n"
                "Generate a secure key using:\n"
                "  python -c 'import secrets; print(secrets.token_hex(32))'\n"
                "Then set it in your .env file or environment:\n"
                "  export SECRET_KEY='your-generated-key-here'"
            )

        # فحص الطول الأدنى (32 بايت = 64 حرف hex على الأقل موصى به)
        if len(secret_key) < 32:
            raise ValueError(
                f"SECRET_KEY too short ({len(secret_key)} chars). "
                f"Minimum 32 characters required for security.\n"
                f"Generate a secure 64-char key using:\n"
                f"  python -c 'import secrets; print(secrets.token_hex(32))'"
            )

        # فحص القيم المعروفة/الافتراضية
        placeholder_values = [
            "your-secret-key-here",
            "change-this-key",
            "secret-key-here",
            "secret_key",
            "secretkey",
            "mysecretkey",
        ]
        if secret_key.lower() in placeholder_values:
            raise ValueError(
                f"SECRET_KEY contains a placeholder value: '{secret_key}'\n"
                f"This is insecure. Generate a unique key using:\n"
                f"  python -c 'import secrets; print(secrets.token_hex(32))'"
            )

        # تحديث المتغير البيئي بالقيمة المنظفة (stripped)
        os.environ["SECRET_KEY"] = secret_key

        super().__init__()

        # ==================== DEBUG MODE ====================
        self.DEBUG = False
        self.TESTING = False

        # ==================== DATABASE CONFIGURATION ====================
        # استخدام PostgreSQL أو MySQL في الإنتاج
        self.DATABASE_TYPE = self._detect_database_type()
        self.DATABASE_URI = self._get_production_database_uri()

        # ==================== PORT CONFIGURATION ====================
        # في الإنتاج، استخدم المنفذ 5000 دائماً (أو من المتغيرات)
        self.PORT = 5000
        port_from_env = os.environ.get("PORT")
        if port_from_env:
            try:
                self.PORT = int(port_from_env)
            except (ValueError, TypeError):
                pass

        # ==================== SECURITY HARDENING ====================
        # تشديد الأمان في الإنتاج
        self.SESSION_COOKIE_SECURE = True  # HTTPS فقط
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = "Strict"
        self.REQUIRE_HTTPS = True

        # ==================== SSL/HTTPS SETTINGS ====================
        # إعدادات SSL/TLS
        self.SSL_ENABLED = True
        self.SSL_CERT_PATH = os.environ.get("SSL_CERT_PATH", "/etc/ssl/certs/cert.pem")
        self.SSL_KEY_PATH = os.environ.get("SSL_KEY_PATH", "/etc/ssl/private/key.pem")
        self.FORCE_HTTPS = True

        # ==================== PRODUCTION INFO ====================
        # معلومات الإنتاج
        self.DEVELOPMENT_MODE = False
        self.LOG_LEVEL = "WARNING"
        self.SHOW_SQL_QUERIES = False
        self.AUTO_RELOAD = False

        # ==================== CORS للإنتاج ====================
        self.CORS_ENABLED = False
        allowed_origins = os.environ.get("ALLOWED_ORIGINS", "")
        self.CORS_ORIGINS = allowed_origins.split(",") if allowed_origins else []

        # ==================== PERFORMANCE ====================
        # تحسينات الأداء
        self.CACHE_TYPE = "redis"
        self.CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

        # ==================== MONITORING ====================
        # المراقبة والتسجيل
        self.ENABLE_MONITORING = True
        self.LOG_FILE_PATH = os.environ.get(
            "LOG_FILE_PATH", "/var/log/app/production.log"
        )

    def _detect_database_type(self):
        """
        كشف نوع قاعدة البيانات من المتغيرات

        Returns:
            str: نوع قاعدة البيانات (postgresql أو mysql)
        """
        db_type = os.environ.get("DATABASE_TYPE", "postgresql").lower()
        if db_type in ["postgresql", "postgres", "pgsql"]:
            return "postgresql"
        elif db_type in ["mysql", "mariadb"]:
            return "mysql"
        return "postgresql"  # افتراضياً

    def _get_production_database_uri(self):
        """
        بناء URI لقاعدة البيانات الإنتاجية

        Returns:
            str: URI قاعدة البيانات
        """
        # أولاً: فحص متغير DATABASE_URL الكامل
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            return database_url

        # ثانياً: بناء URI من المتغيرات المنفصلة
        db_user = os.environ.get("DB_USER", "root")
        db_password = os.environ.get("DB_PASSWORD", "")
        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get(
            "DB_PORT", "5432" if self.DATABASE_TYPE == "postgresql" else "3306"
        )
        db_name = os.environ.get("DB_NAME", "production_db")

        # بناء URI حسب نوع قاعدة البيانات
        if self.DATABASE_TYPE == "postgresql":
            uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        elif self.DATABASE_TYPE == "mysql":
            # استخدام pymysql كدرايفر افتراضي (يمكن تغييره عبر DB_DRIVER)
            db_driver = os.environ.get("DB_DRIVER", "pymysql")
            uri = f"mysql+{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            # افتراضياً: PostgreSQL
            uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return uri


def get_config():
    """
    ترجع كائن الإعدادات المناسب حسب البيئة الحالية

    Returns:
        BaseConfig: كائن DevelopmentConfig أو ProductionConfig حسب البيئة

    Examples:
        >>> config = get_config()
        >>> print(config.ENVIRONMENT)
        'development'
        >>> print(config.DEBUG)
        True
    """
    environment = detect_environment()

    if environment == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()


def get_config_for_environment(env_name):
    """
    ترجع إعدادات بيئة محددة (مفيد للاختبار)

    Args:
        env_name (str): اسم البيئة ('development' أو 'production')

    Returns:
        BaseConfig: كائن الإعدادات المطلوب

    Raises:
        ValueError: إذا كان اسم البيئة غير صالح
    """
    env_name = env_name.lower()

    if env_name in ["development", "dev"]:
        return DevelopmentConfig()
    elif env_name in ["production", "prod"]:
        return ProductionConfig()
    else:
        raise ValueError(
            f"اسم بيئة غير صالح: {env_name}. استخدم 'development' أو 'production'"
        )


# ==================== الاختبارات - Unit Tests ====================

if __name__ == "__main__":
    print("=" * 70)
    print("بدء اختبار مصنع الإعدادات - Configuration Factory Tests")
    print("=" * 70)
    print()

    # حفظ المتغيرات الأصلية
    original_env = os.environ.get("ENVIRONMENT")
    original_secret_key = os.environ.get("SECRET_KEY")

    # متغيرات حساب الاختبارات
    tests_passed = 0
    tests_failed = 0
    total_tests = 0

    def run_test(test_name, condition, expected=True):
        """دالة مساعدة لتشغيل الاختبار"""
        global tests_passed, tests_failed, total_tests
        total_tests += 1

        result = condition == expected
        status = "✓ نجح" if result else "✗ فشل"

        if result:
            tests_passed += 1
            print(f"[{status}] {test_name}")
        else:
            tests_failed += 1
            print(f"[{status}] {test_name} - القيمة: {condition}, المتوقع: {expected}")

        return result

    # ==================== الاختبار 1: BaseConfig ====================
    print("\n--- الاختبار 1: BaseConfig - الإعدادات الأساسية ---")
    base_config = BaseConfig()

    run_test("الاختبار: BaseConfig تم إنشاؤها بنجاح", base_config is not None)
    run_test("الاختبار: ENVIRONMENT موجود", hasattr(base_config, "ENVIRONMENT"))
    run_test(
        "الاختبار: ENVIRONMENT قيمة صالحة",
        base_config.ENVIRONMENT in ["development", "production"],
    )
    run_test("الاختبار: SECRET_KEY موجود", hasattr(base_config, "SECRET_KEY"))
    run_test(
        "الاختبار: SECRET_KEY ليس فارغاً",
        base_config.SECRET_KEY is not None and len(base_config.SECRET_KEY) > 0,
    )
    run_test("الاختبار: PORT موجود", hasattr(base_config, "PORT"))
    run_test("الاختبار: PORT رقم صحيح", isinstance(base_config.PORT, int))
    run_test("الاختبار: HOST موجود", base_config.HOST == "0.0.0.0")

    print(f"\nمعلومات BaseConfig:")
    print(f"  - البيئة: {base_config.ENVIRONMENT}")
    print(f"  - المنفذ: {base_config.PORT}")
    print(
        f"  - SECRET_KEY length: {len(base_config.SECRET_KEY) if base_config.SECRET_KEY else 0}"
    )

    # ==================== الاختبار 2: DevelopmentConfig ====================
    print("\n--- الاختبار 2: DevelopmentConfig - إعدادات التطوير ---")
    dev_config = DevelopmentConfig()

    run_test("الاختبار: DevelopmentConfig تم إنشاؤها بنجاح", dev_config is not None)
    run_test("الاختبار: DEBUG مفعل في التطوير", dev_config.DEBUG == True)
    run_test("الاختبار: DATABASE_TYPE هو sqlite", dev_config.DATABASE_TYPE == "sqlite")
    run_test(
        "الاختبار: DATABASE_URI يبدأ بـ sqlite:///",
        dev_config.DATABASE_URI.startswith("sqlite:///"),
    )
    run_test("الاختبار: DEVELOPMENT_MODE مفعل", dev_config.DEVELOPMENT_MODE == True)
    run_test(
        "الاختبار: SESSION_COOKIE_SECURE معطل في التطوير",
        dev_config.SESSION_COOKIE_SECURE == False,
    )
    run_test("الاختبار: LOG_LEVEL هو DEBUG", dev_config.LOG_LEVEL == "DEBUG")

    print(f"\nمعلومات DevelopmentConfig:")
    print(f"  - DEBUG: {dev_config.DEBUG}")
    print(f"  - DATABASE_TYPE: {dev_config.DATABASE_TYPE}")
    print(f"  - DATABASE_URI: {dev_config.DATABASE_URI}")
    print(f"  - PORT: {dev_config.PORT}")
    print(f"  - LOG_LEVEL: {dev_config.LOG_LEVEL}")

    # ==================== الاختبار 3: ProductionConfig ====================
    print("\n--- الاختبار 3: ProductionConfig - إعدادات الإنتاج ---")

    # تعيين SECRET_KEY للسماح بإنشاء ProductionConfig (64 حرف للطول الآمن)
    os.environ["SECRET_KEY"] = "a" * 64  # مفتاح اختبار آمن بطول 64 حرف

    prod_config = ProductionConfig()

    run_test("الاختبار: ProductionConfig تم إنشاؤها بنجاح", prod_config is not None)
    run_test("الاختبار: DEBUG معطل في الإنتاج", prod_config.DEBUG == False)
    run_test(
        "الاختبار: DATABASE_TYPE في الإنتاج",
        prod_config.DATABASE_TYPE in ["postgresql", "mysql"],
    )
    run_test(
        "الاختبار: SESSION_COOKIE_SECURE مفعل في الإنتاج",
        prod_config.SESSION_COOKIE_SECURE == True,
    )
    run_test("الاختبار: SSL_ENABLED مفعل", prod_config.SSL_ENABLED == True)
    run_test("الاختبار: DEVELOPMENT_MODE معطل", prod_config.DEVELOPMENT_MODE == False)
    run_test("الاختبار: LOG_LEVEL هو WARNING", prod_config.LOG_LEVEL == "WARNING")

    print(f"\nمعلومات ProductionConfig:")
    print(f"  - DEBUG: {prod_config.DEBUG}")
    print(f"  - DATABASE_TYPE: {prod_config.DATABASE_TYPE}")
    print(f"  - PORT: {prod_config.PORT}")
    print(f"  - SSL_ENABLED: {prod_config.SSL_ENABLED}")
    print(f"  - LOG_LEVEL: {prod_config.LOG_LEVEL}")

    # ==================== الاختبار 4: get_config() ====================
    print("\n--- الاختبار 4: get_config() - الحصول على الإعدادات التلقائية ---")
    auto_config = get_config()

    run_test("الاختبار: get_config() يرجع كائن", auto_config is not None)
    run_test(
        "الاختبار: get_config() يرجع BaseConfig أو فئة فرعية",
        isinstance(auto_config, BaseConfig),
    )

    current_env = detect_environment()
    if current_env == "development":
        run_test(
            "الاختبار: get_config() يرجع DevelopmentConfig في بيئة التطوير",
            isinstance(auto_config, DevelopmentConfig),
        )
    else:
        run_test(
            "الاختبار: get_config() يرجع ProductionConfig في بيئة الإنتاج",
            isinstance(auto_config, ProductionConfig),
        )

    print(f"\nالإعدادات التلقائية:")
    print(f"  - النوع: {type(auto_config).__name__}")
    print(f"  - البيئة: {auto_config.ENVIRONMENT}")
    print(f"  - DEBUG: {auto_config.DEBUG}")

    # ==================== الاختبار 5: get_config_for_environment() ====================
    print("\n--- الاختبار 5: get_config_for_environment() - اختيار البيئة يدوياً ---")

    dev_manual = get_config_for_environment("development")
    run_test(
        "الاختبار: get_config_for_environment('development') يرجع DevelopmentConfig",
        isinstance(dev_manual, DevelopmentConfig),
    )

    prod_manual = get_config_for_environment("production")
    run_test(
        "الاختبار: get_config_for_environment('production') يرجع ProductionConfig",
        isinstance(prod_manual, ProductionConfig),
    )

    # اختبار الاختصارات
    dev_short = get_config_for_environment("dev")
    run_test(
        "الاختبار: get_config_for_environment('dev') يرجع DevelopmentConfig",
        isinstance(dev_short, DevelopmentConfig),
    )

    prod_short = get_config_for_environment("prod")
    run_test(
        "الاختبار: get_config_for_environment('prod') يرجع ProductionConfig",
        isinstance(prod_short, ProductionConfig),
    )

    # اختبار قيمة غير صالحة
    try:
        invalid_config = get_config_for_environment("invalid")
        run_test(
            "الاختبار: get_config_for_environment() يرفع ValueError لقيمة غير صالحة",
            False,
        )
    except ValueError:
        run_test(
            "الاختبار: get_config_for_environment() يرفع ValueError لقيمة غير صالحة",
            True,
        )

    # ==================== الاختبار 6: get_config_dict() ====================
    print("\n--- الاختبار 6: get_config_dict() - تحويل الإعدادات لقاموس ---")
    config_dict = dev_config.get_config_dict()

    run_test("الاختبار: get_config_dict() يرجع قاموس", isinstance(config_dict, dict))
    run_test("الاختبار: القاموس يحتوي على ENVIRONMENT", "ENVIRONMENT" in config_dict)
    run_test("الاختبار: القاموس يحتوي على SECRET_KEY", "SECRET_KEY" in config_dict)
    run_test("الاختبار: القاموس يحتوي على PORT", "PORT" in config_dict)
    run_test("الاختبار: القاموس يحتوي على DEBUG", "DEBUG" in config_dict)

    print(f"\nعدد الإعدادات في القاموس: {len(config_dict)}")

    # ==================== الاختبار 7: توليد SECRET_KEY ====================
    print("\n--- الاختبار 7: توليد SECRET_KEY ---")

    # إزالة SECRET_KEY من المتغيرات
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    config1 = BaseConfig()
    config2 = BaseConfig()

    run_test(
        "الاختبار: SECRET_KEY يتم توليده تلقائياً",
        config1.SECRET_KEY is not None and len(config1.SECRET_KEY) > 0,
    )
    run_test(
        "الاختبار: SECRET_KEY فريد لكل instance",
        config1.SECRET_KEY != config2.SECRET_KEY,
    )
    run_test(
        "الاختبار: SECRET_KEY بالطول الصحيح (64 حرف)",
        config1.SECRET_KEY is not None and len(config1.SECRET_KEY) == 64,
    )

    # اختبار SECRET_KEY من المتغيرات
    os.environ["SECRET_KEY"] = "custom_secret_key_for_testing"
    config_custom = BaseConfig()
    run_test(
        "الاختبار: SECRET_KEY يُقرأ من المتغيرات",
        config_custom.SECRET_KEY == "custom_secret_key_for_testing",
    )

    # ==================== الاختبار 8: __repr__ ====================
    print("\n--- الاختبار 8: __repr__ - التمثيل النصي ---")
    dev_repr = repr(dev_config)
    run_test("الاختبار: __repr__ يحتوي على اسم الفئة", "DevelopmentConfig" in dev_repr)
    run_test("الاختبار: __repr__ يحتوي على environment", "environment=" in dev_repr)

    print(f"\nالتمثيل النصي:")
    print(f"  - DevelopmentConfig: {repr(dev_config)}")
    print(f"  - ProductionConfig: {repr(prod_config)}")

    # ==================== الاختبار 9: الوراثة ====================
    print("\n--- الاختبار 9: الوراثة - Inheritance ---")

    run_test(
        "الاختبار: DevelopmentConfig يرث من BaseConfig",
        issubclass(DevelopmentConfig, BaseConfig),
    )
    run_test(
        "الاختبار: ProductionConfig يرث من BaseConfig",
        issubclass(ProductionConfig, BaseConfig),
    )
    run_test(
        "الاختبار: DevelopmentConfig instance من BaseConfig",
        isinstance(dev_config, BaseConfig),
    )
    run_test(
        "الاختبار: ProductionConfig instance من BaseConfig",
        isinstance(prod_config, BaseConfig),
    )

    # ==================== الاختبار 10: ProductionConfig يتطلب SECRET_KEY ====================
    print("\n--- الاختبار 10: ProductionConfig - التحقق من إلزامية SECRET_KEY ---")

    # حفظ SECRET_KEY الحالي
    current_secret_key = os.environ.get("SECRET_KEY")

    # اختبار: ProductionConfig يرفع ValueError بدون SECRET_KEY
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    try:
        prod_no_secret = ProductionConfig()
        run_test("الاختبار: ProductionConfig يرفع ValueError بدون SECRET_KEY", False)
    except ValueError as e:
        run_test("الاختبار: ProductionConfig يرفع ValueError بدون SECRET_KEY", True)
        run_test(
            "الاختبار: رسالة الخطأ تحتوي على 'SECRET_KEY must be set'",
            "SECRET_KEY must be set" in str(e),
        )

    # اختبار: ProductionConfig يرفع ValueError مع SECRET_KEY فارغ
    os.environ["SECRET_KEY"] = ""
    try:
        prod_empty_secret = ProductionConfig()
        run_test("الاختبار: ProductionConfig يرفع ValueError مع SECRET_KEY فارغ", False)
    except ValueError:
        run_test("الاختبار: ProductionConfig يرفع ValueError مع SECRET_KEY فارغ", True)

    # اختبار: ProductionConfig يرفع ValueError مع SECRET_KEY مسافات فقط
    os.environ["SECRET_KEY"] = "   "
    try:
        prod_spaces_secret = ProductionConfig()
        run_test(
            "الاختبار: ProductionConfig يرفع ValueError مع SECRET_KEY مسافات فقط", False
        )
    except ValueError:
        run_test(
            "الاختبار: ProductionConfig يرفع ValueError مع SECRET_KEY مسافات فقط", True
        )

    # اختبار: ProductionConfig يرفض مفتاح قصير (<32 حرف)
    os.environ["SECRET_KEY"] = "short_key"
    try:
        prod_short_secret = ProductionConfig()
        run_test("الاختبار: ProductionConfig يرفع ValueError مع مفتاح قصير", False)
    except ValueError:
        run_test("الاختبار: ProductionConfig يرفع ValueError مع مفتاح قصير", True)

    # اختبار: ProductionConfig ينجح مع SECRET_KEY صالح (64 حرف)
    os.environ["SECRET_KEY"] = "a" * 64  # مفتاح آمن بطول 64 حرف
    try:
        prod_valid_secret = ProductionConfig()
        run_test("الاختبار: ProductionConfig ينجح مع SECRET_KEY صالح", True)
        run_test(
            "الاختبار: SECRET_KEY المخصص يُستخدم",
            prod_valid_secret.SECRET_KEY == "a" * 64,
        )
    except ValueError:
        run_test("الاختبار: ProductionConfig ينجح مع SECRET_KEY صالح", False)

    # استعادة SECRET_KEY
    if current_secret_key:
        os.environ["SECRET_KEY"] = current_secret_key
    elif "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    # ==================== الاختبار 11: MySQL URI scheme الجديد ====================
    print("\n--- الاختبار 11: MySQL URI - التحقق من schema الجديد ---")

    # حفظ المتغيرات الحالية
    saved_db_type = os.environ.get("DATABASE_TYPE")
    saved_db_driver = os.environ.get("DB_DRIVER")
    saved_secret = os.environ.get("SECRET_KEY")
    saved_db_url = os.environ.get("DATABASE_URL")

    # تعيين SECRET_KEY للسماح بإنشاء ProductionConfig (64 حرف)
    os.environ["SECRET_KEY"] = "a" * 64

    # إزالة DATABASE_URL للسماح ببناء URI من المتغيرات المنفصلة
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]

    # اختبار: MySQL URI يستخدم mysql+pymysql:// افتراضياً
    os.environ["DATABASE_TYPE"] = "mysql"
    if "DB_DRIVER" in os.environ:
        del os.environ["DB_DRIVER"]

    prod_mysql = ProductionConfig()
    run_test(
        "الاختبار: MySQL URI يبدأ بـ mysql+pymysql://",
        prod_mysql.DATABASE_URI.startswith("mysql+pymysql://"),
    )

    # اختبار: MySQL URI يدعم DB_DRIVER مخصص
    os.environ["DB_DRIVER"] = "mysqlconnector"
    prod_mysql_custom = ProductionConfig()
    run_test(
        "الاختبار: MySQL URI يدعم DB_DRIVER مخصص",
        prod_mysql_custom.DATABASE_URI.startswith("mysql+mysqlconnector://"),
    )

    # اختبار: PostgreSQL URI لم يتأثر
    os.environ["DATABASE_TYPE"] = "postgresql"
    prod_postgres = ProductionConfig()
    run_test(
        "الاختبار: PostgreSQL URI يبدأ بـ postgresql://",
        prod_postgres.DATABASE_URI.startswith("postgresql://"),
    )

    print(f"\nأمثلة على URIs:")
    os.environ["DATABASE_TYPE"] = "mysql"
    if "DB_DRIVER" in os.environ:
        del os.environ["DB_DRIVER"]
    prod_example = ProductionConfig()
    print(f"  - MySQL (افتراضي): {prod_example.DATABASE_URI}")

    os.environ["DB_DRIVER"] = "mysqlconnector"
    prod_example2 = ProductionConfig()
    print(f"  - MySQL (مخصص): {prod_example2.DATABASE_URI}")

    # استعادة المتغيرات
    if saved_db_type:
        os.environ["DATABASE_TYPE"] = saved_db_type
    elif "DATABASE_TYPE" in os.environ:
        del os.environ["DATABASE_TYPE"]

    if saved_db_driver:
        os.environ["DB_DRIVER"] = saved_db_driver
    elif "DB_DRIVER" in os.environ:
        del os.environ["DB_DRIVER"]

    if saved_db_url:
        os.environ["DATABASE_URL"] = saved_db_url
    elif "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]

    if saved_secret:
        os.environ["SECRET_KEY"] = saved_secret
    elif "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    # ==================== استعادة المتغيرات الأصلية ====================
    if original_env:
        os.environ["ENVIRONMENT"] = original_env
    elif "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]

    if original_secret_key:
        os.environ["SECRET_KEY"] = original_secret_key
    elif "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    # ==================== ملخص النتائج ====================
    print("\n" + "=" * 70)
    print("ملخص نتائج الاختبار - Test Summary")
    print("=" * 70)
    print(f"إجمالي الاختبارات: {total_tests}")
    print(f"الاختبارات الناجحة: {tests_passed} ✓")
    print(f"الاختبارات الفاشلة: {tests_failed} ✗")

    success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"نسبة النجاح: {success_rate:.1f}%")

    # ==================== عرض مثال على الاستخدام ====================
    print("\n" + "=" * 70)
    print("مثال على الاستخدام - Usage Example")
    print("=" * 70)
    print(
        """
# في التطبيق الرئيسي:
from config_factory import get_config

# الحصول على الإعدادات المناسبة للبيئة الحالية
config = get_config()

# استخدام الإعدادات
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)
    """
    )

    if tests_failed == 0:
        print("\n🎉 جميع الاختبارات نجحت!")
        sys.exit(0)
    else:
        print(f"\n⚠️ هناك {tests_failed} اختبار(ات) فشل(ت)")
        sys.exit(1)
