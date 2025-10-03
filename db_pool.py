#!/usr/bin/env python3
# coding: utf-8
"""
نظام إدارة اتصالات قاعدة البيانات - Database Connection Pool Manager
يوفر connection pooling وإدارة متقدمة للاتصالات مع retry logic ومراقبة

المميزات:
- Connection pooling لـ SQLite, PostgreSQL, MySQL
- Retry logic تلقائي للاتصالات الفاشلة
- مراقبة وإحصائيات للاتصالات
- Health checks للاتصال
- Thread-safe operations
"""

import os
import sys
import time
import logging
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Any, Callable
from datetime import datetime
from functools import wraps

# إضافة المجلد الجذر للـ PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config_factory import get_config
except ImportError:
    print("❌ خطأ: لا يمكن استيراد config_factory")
    sys.exit(1)

# محاولة استيراد SQLAlchemy (اختياري)
try:
    from sqlalchemy import create_engine, event, pool, text
    from sqlalchemy.exc import OperationalError, DBAPIError
    from sqlalchemy.pool import QueuePool, NullPool

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    # Dummy classes للتوافق
    OperationalError = Exception
    DBAPIError = Exception
    QueuePool = None
    NullPool = None
    text = lambda x: x  # Dummy text function
    print("⚠️  SQLAlchemy غير متوفر - سيتم استخدام pooling بسيط")

# إعداد Logging
logger = logging.getLogger("DBPool")
logger.setLevel(logging.INFO)


class PoolStatistics:
    """إحصائيات Connection Pool"""

    def __init__(self):
        self.connections_created = 0
        self.connections_closed = 0
        self.connections_recycled = 0
        self.connection_errors = 0
        self.retry_attempts = 0
        self.total_queries = 0
        self.failed_queries = 0
        self.start_time = datetime.now()
        self._lock = threading.Lock()

    def increment(self, metric: str, value: int = 1):
        """زيادة قيمة metric"""
        with self._lock:
            if hasattr(self, metric):
                setattr(self, metric, getattr(self, metric) + value)

    def get_stats(self) -> Dict[str, Any]:
        """الحصول على جميع الإحصائيات"""
        with self._lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            return {
                "connections_created": self.connections_created,
                "connections_closed": self.connections_closed,
                "connections_recycled": self.connections_recycled,
                "connection_errors": self.connection_errors,
                "retry_attempts": self.retry_attempts,
                "total_queries": self.total_queries,
                "failed_queries": self.failed_queries,
                "uptime_seconds": uptime,
                "success_rate": self._calculate_success_rate(),
            }

    def _calculate_success_rate(self) -> float:
        """حساب نسبة نجاح الاتصالات"""
        total = self.total_queries
        if total == 0:
            return 100.0
        success = total - self.failed_queries
        return (success / total) * 100.0

    def reset(self):
        """إعادة تعيين الإحصائيات"""
        with self._lock:
            self.__init__()


class DatabaseConnectionPool:
    """
    مدير Connection Pool لقاعدة البيانات

    يوفر:
    - Connection pooling متقدم
    - Retry logic تلقائي
    - مراقبة الاتصالات
    - Health checks
    """

    def __init__(
        self,
        config=None,
        pool_size: int = 5,
        max_overflow: int = 10,
        retry_attempts: int = 3,
        retry_delay: float = 0.5,
    ):
        """
        تهيئة Connection Pool

        Args:
            config: كائن الإعدادات (من config_factory)
            pool_size: حجم Pool الأساسي (افتراضي: 5)
            max_overflow: عدد الاتصالات الإضافية (افتراضي: 10)
            retry_attempts: عدد محاولات إعادة الاتصال (افتراضي: 3)
            retry_delay: التأخير بين المحاولات بالثواني (افتراضي: 0.5)
        """
        self.config = config or get_config()
        # استخدام الإعدادات من config كمصدر رئيسي
        self.pool_size = getattr(self.config, "DB_POOL_SIZE", pool_size)
        self.max_overflow = getattr(self.config, "DB_MAX_OVERFLOW", max_overflow)
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.stats = PoolStatistics()
        self.engine = None
        self._lock = threading.Lock()

        # إنشاء Engine
        self._create_engine()

        logger.info(
            f"تم تهيئة DatabaseConnectionPool - البيئة: {self.config.ENVIRONMENT}"
        )
        logger.info(f"Database Type: {self.config.DATABASE_TYPE}")
        logger.info(f"Pool Size: {self.pool_size}, Max Overflow: {self.max_overflow}")

    def _create_engine(self):
        """إنشاء SQLAlchemy Engine مع إعدادات Pool"""
        if not SQLALCHEMY_AVAILABLE:
            logger.warning("SQLAlchemy غير متوفر - Connection pooling محدود")
            return

        database_uri = self.config.DATABASE_URI

        # إعدادات Pool حسب نوع قاعدة البيانات
        pool_config = self._get_pool_config()

        try:
            # إنشاء Engine
            self.engine = create_engine(  # type: ignore[possibly-unbound]
                database_uri,
                **pool_config,
                echo=False,  # تعطيل SQL logging (يمكن تفعيله في DEBUG)
                future=True,  # استخدام SQLAlchemy 2.0 style
            )

            # إضافة event listeners للإحصائيات
            self._setup_event_listeners()

            logger.info("تم إنشاء Database Engine بنجاح")

        except Exception as e:
            logger.error(f"فشل إنشاء Database Engine: {e}")
            self.stats.increment("connection_errors")
            raise

    def _get_pool_config(self) -> Dict[str, Any]:
        """
        الحصول على إعدادات Pool حسب نوع قاعدة البيانات

        Returns:
            dict: إعدادات Pool
        """
        db_type = self.config.DATABASE_TYPE

        if db_type == "sqlite":
            # SQLite: استخدام NullPool (لا pooling حقيقي لأن SQLite single-threaded)
            return {"poolclass": NullPool, "connect_args": {"check_same_thread": False}}

        elif db_type in ("postgresql", "mysql"):
            # PostgreSQL/MySQL: استخدام QueuePool
            return {
                "poolclass": QueuePool,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": getattr(self.config, "DB_POOL_TIMEOUT", 30),
                "pool_recycle": getattr(self.config, "DB_POOL_RECYCLE", 3600),
                "pool_pre_ping": getattr(self.config, "DB_POOL_PRE_PING", True),
            }

        else:
            # افتراضي: QueuePool
            return {
                "poolclass": QueuePool,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_pre_ping": True,
            }

    def _setup_event_listeners(self):
        """إعداد Event Listeners لتتبع الاتصالات"""
        if not self.engine or not SQLALCHEMY_AVAILABLE:
            return

        # ربط events مع engine.pool للتأكد من تشغيلها
        pool_obj = self.engine.pool

        @event.listens_for(pool_obj, "connect")  # type: ignore[possibly-unbound]
        def receive_connect(dbapi_conn, connection_record):
            """عند إنشاء اتصال جديد"""
            self.stats.increment("connections_created")
            logger.debug("اتصال جديد تم إنشاؤه")

        @event.listens_for(pool_obj, "close")  # type: ignore[possibly-unbound]
        def receive_close(dbapi_conn, connection_record):
            """عند إغلاق اتصال"""
            self.stats.increment("connections_closed")
            logger.debug("تم إغلاق اتصال")

        @event.listens_for(pool_obj, "checkin")  # type: ignore[possibly-unbound]
        def receive_checkin(dbapi_conn, connection_record):
            """عند إرجاع اتصال للـ pool"""
            self.stats.increment("connections_recycled")

    @contextmanager
    def get_connection(self):
        """
        الحصول على اتصال من Pool (Context Manager)

        Yields:
            connection: كائن الاتصال

        Example:
            with pool.get_connection() as conn:
                result = conn.execute("SELECT * FROM users")
        """
        if not self.engine:
            raise RuntimeError("Database Engine غير متوفر")

        connection = None
        try:
            # محاولة الحصول على اتصال مع retry logic
            connection = self._get_connection_with_retry()
            yield connection

        except Exception as e:
            self.stats.increment("failed_queries")
            logger.error(f"خطأ في الاتصال: {e}")
            raise

        finally:
            if connection:
                connection.close()

    def _get_connection_with_retry(self):
        """
        الحصول على اتصال مع retry logic

        Returns:
            connection: كائن الاتصال
        """
        last_error: Optional[Exception] = None

        for attempt in range(self.retry_attempts):
            try:
                if not self.engine:
                    raise RuntimeError("Database Engine غير متوفر")
                connection = self.engine.connect()
                # عدّ الاتصالات الناجحة فقط (ليس الاستعلامات)
                return connection

            except (OperationalError, DBAPIError) as e:
                last_error = e
                self.stats.increment("connection_errors")
                self.stats.increment("retry_attempts")

                logger.warning(f"محاولة {attempt + 1}/{self.retry_attempts} فشلت: {e}")

                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    raise

        # إذا وصلنا هنا، جميع المحاولات فشلت
        if last_error:
            raise last_error
        raise RuntimeError("فشل الاتصال بقاعدة البيانات")

    def execute_with_retry(self, query: str, params: Optional[Dict] = None):
        """
        تنفيذ استعلام مع retry logic

        Args:
            query: الاستعلام SQL
            params: معاملات الاستعلام

        Returns:
            result: نتيجة الاستعلام
        """
        with self.get_connection() as conn:
            if params:
                result = conn.execute(text(query), params)
            else:
                result = conn.execute(text(query))
            # عدّ الاستعلامات الناجحة بعد التنفيذ
            self.stats.increment("total_queries")
            return result

    def health_check(self) -> bool:
        """
        فحص صحة الاتصال بقاعدة البيانات

        Returns:
            bool: True إذا كان الاتصال سليماً
        """
        try:
            with self.get_connection() as conn:
                # استعلام بسيط للتحقق
                if self.config.DATABASE_TYPE == "postgresql":
                    conn.execute(text("SELECT 1"))
                elif self.config.DATABASE_TYPE == "mysql":
                    conn.execute(text("SELECT 1"))
                else:  # sqlite
                    conn.execute(text("SELECT 1"))

                logger.info("✅ Database health check: OK")
                return True

        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return False

    def get_pool_status(self) -> Dict[str, Any]:
        """
        الحصول على حالة Pool الحالية

        Returns:
            dict: معلومات حالة Pool
        """
        if not self.engine:
            return {"status": "unavailable", "type": "no engine"}

        pool_obj = self.engine.pool

        # التحقق من نوع Pool
        if not hasattr(pool_obj, "size"):
            return {
                "status": "available",
                "type": "NullPool (no pooling)",
                "database_type": self.config.DATABASE_TYPE,
                "statistics": self.stats.get_stats(),
            }

        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "current_size": pool_obj.size(),  # type: ignore[attr-defined]
            "checked_in": pool_obj.checkedin(),  # type: ignore[attr-defined]
            "checked_out": pool_obj.checkedout(),  # type: ignore[attr-defined]
            "overflow": pool_obj.overflow(),  # type: ignore[attr-defined]
            "database_type": self.config.DATABASE_TYPE,
            "statistics": self.stats.get_stats(),
        }

    def close(self):
        """إغلاق Pool والتنظيف"""
        if self.engine:
            self.engine.dispose()
            logger.info("تم إغلاق Database Connection Pool")

    def __enter__(self):
        """دعم Context Manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """إغلاق تلقائي عند الخروج"""
        self.close()


# ==================== Decorators ====================


def with_db_retry(max_attempts: int = 3, delay: float = 0.5):
    """
    Decorator لإضافة retry logic لأي دالة تتعامل مع قاعدة البيانات

    Args:
        max_attempts: عدد المحاولات
        delay: التأخير بين المحاولات

    Example:
        @with_db_retry(max_attempts=5, delay=1.0)
        def fetch_user(user_id):
            return db.query(User).filter_by(id=user_id).first()
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error: Optional[Exception] = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"{func.__name__} - محاولة {attempt + 1}/{max_attempts} فشلت: {e}"
                    )

                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    else:
                        raise

            # إذا وصلنا هنا، جميع المحاولات فشلت
            if last_error:
                raise last_error
            raise RuntimeError(f"فشل تنفيذ {func.__name__}")

        return wrapper

    return decorator


# ==================== مثيل عام (Singleton) ====================

_global_pool = None
_pool_lock = threading.Lock()


def get_db_pool(force_new: bool = False) -> DatabaseConnectionPool:
    """
    الحصول على المثيل العام لـ DatabaseConnectionPool (Singleton)

    Args:
        force_new: إنشاء pool جديد بدلاً من استخدام الموجود

    Returns:
        DatabaseConnectionPool: المثيل العام
    """
    global _global_pool

    with _pool_lock:
        if _global_pool is None or force_new:
            _global_pool = DatabaseConnectionPool()

        return _global_pool


# ==================== CLI Interface ====================


def main():
    """واجهة سطر الأوامر لاختبار Connection Pool"""
    import argparse

    parser = argparse.ArgumentParser(description="Database Connection Pool Manager")
    parser.add_argument(
        "--test", action="store_true", help="تشغيل اختبار Connection Pool"
    )
    parser.add_argument("--status", action="store_true", help="عرض حالة Pool")
    parser.add_argument("--health", action="store_true", help="فحص صحة الاتصال")
    parser.add_argument("--stats", action="store_true", help="عرض الإحصائيات")

    args = parser.parse_args()

    # إنشاء Pool
    pool = get_db_pool()

    if args.health:
        # فحص الصحة
        print("\n🔍 فحص صحة الاتصال...")
        is_healthy = pool.health_check()
        print(f"الحالة: {'✅ سليم' if is_healthy else '❌ فشل'}\n")

    elif args.status:
        # عرض الحالة
        print("\n📊 حالة Connection Pool:")
        status = pool.get_pool_status()
        for key, value in status.items():
            if key != "statistics":
                print(f"  • {key}: {value}")
        print()

    elif args.stats:
        # عرض الإحصائيات
        print("\n📈 إحصائيات Connection Pool:")
        stats = pool.stats.get_stats()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  • {key}: {value:.2f}")
            else:
                print(f"  • {key}: {value}")
        print()

    elif args.test:
        # اختبار Pool
        print("\n🧪 اختبار Connection Pool...\n")

        # 1. Health Check
        print("1️⃣ Health Check:")
        is_healthy = pool.health_check()
        print(
            f"   {'✅' if is_healthy else '❌'} النتيجة: {'سليم' if is_healthy else 'فشل'}\n"
        )

        # 2. اختبار الاتصال
        print("2️⃣ اختبار الحصول على اتصال:")
        try:
            with pool.get_connection() as conn:
                print("   ✅ تم الحصول على اتصال بنجاح\n")
        except Exception as e:
            print(f"   ❌ فشل: {e}\n")

        # 3. عرض الحالة
        print("3️⃣ حالة Pool:")
        status = pool.get_pool_status()
        for key, value in status.items():
            if key != "statistics":
                print(f"   • {key}: {value}")

        print("\n✅ اكتمل الاختبار\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
