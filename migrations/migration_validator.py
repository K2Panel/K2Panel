#!/usr/bin/env python
# coding: utf-8
"""
Migration Validator for K2Panel
نظام التحقق من صحة Migrations

A comprehensive validation system for Alembic migration files.
نظام شامل للتحقق من صحة ملفات Alembic migrations.

Usage:
    python migrations/migration_validator.py
    python migrations/migration_validator.py --file migrations/versions/001_initial_baseline.py
    python migrations/migration_validator.py --dir migrations/versions
"""

import os
import sys
import ast
import re
from typing import List, Dict, Tuple, Optional, Set, Any
from pathlib import Path
import argparse


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    @staticmethod
    def disable():
        """Disable colors for non-terminal output"""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.RESET = ''


def print_header(text: str, color: str = Colors.CYAN) -> None:
    """Print a formatted header"""
    print(f"\n{color}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{color}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{color}{Colors.BOLD}{'=' * 70}{Colors.RESET}\n")


def print_error(text: str) -> None:
    """Print an error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_warning(text: str) -> None:
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_success(text: str) -> None:
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_info(text: str) -> None:
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def validate_migration_file(file_path: str) -> List[str]:
    """
    Validate migration file structure and metadata
    التحقق من بنية الملف و metadata
    
    Checks:
    - File exists / التحقق من وجود الملف
    - Valid Python syntax / صحة بنية Python
    - Required imports (alembic, sqlalchemy) / الـ imports المطلوبة
    - Metadata (revision, down_revision) / البيانات الوصفية
    - Docstring / وثائق الملف
    
    Args:
        file_path: Path to migration file
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if not os.path.exists(file_path):
        errors.append(f"File does not exist | الملف غير موجود: {file_path}")
        return errors
    
    if not file_path.endswith('.py'):
        errors.append(f"File is not a Python file | الملف ليس ملف Python: {file_path}")
        return errors
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Cannot read file | لا يمكن قراءة الملف: {str(e)}")
        return errors
    
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as e:
        errors.append(f"Invalid Python syntax | خطأ في بنية Python: Line {e.lineno}: {e.msg}")
        return errors
    
    has_alembic_import = False
    has_sqlalchemy_import = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'alembic':
                has_alembic_import = True
            elif node.module == 'sqlalchemy' or (node.module and node.module.startswith('sqlalchemy.')):
                has_sqlalchemy_import = True
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'sqlalchemy' or alias.name.startswith('sqlalchemy.'):
                    has_sqlalchemy_import = True
    
    if not has_alembic_import:
        errors.append("Missing 'from alembic import op' | الـ import من alembic مفقود")
    
    if not has_sqlalchemy_import:
        errors.append("Missing 'import sqlalchemy as sa' | الـ import من sqlalchemy مفقود")
    
    has_revision = False
    has_down_revision = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == 'revision':
                        has_revision = True
                    elif target.id == 'down_revision':
                        has_down_revision = True
    
    if not has_revision:
        errors.append("Missing 'revision' variable | متغير 'revision' مفقود")
    
    if not has_down_revision:
        errors.append("Missing 'down_revision' variable | متغير 'down_revision' مفقود")
    
    docstring = ast.get_docstring(tree)
    if not docstring or len(docstring.strip()) < 10:
        errors.append("Missing or insufficient docstring | وثائق الملف مفقودة أو غير كافية")
    
    if docstring and 'Revision ID:' not in docstring:
        errors.append("Docstring missing 'Revision ID:' | وثائق الملف لا تحتوي على 'Revision ID:'")
    
    return errors


def validate_upgrade_downgrade(file_path: str) -> List[str]:
    """
    Validate upgrade() and downgrade() functions
    التحقق من دالتي upgrade و downgrade
    
    Checks:
    - upgrade() function exists / وجود دالة upgrade
    - downgrade() function exists / وجود دالة downgrade
    - Correct signature (-> None) / التوقيع الصحيح
    - Functions are not completely empty / الدالات ليست فارغة تماماً
    
    Args:
        file_path: Path to migration file
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if not os.path.exists(file_path):
        errors.append(f"File does not exist | الملف غير موجود: {file_path}")
        return errors
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content, filename=file_path)
    except Exception as e:
        errors.append(f"Cannot parse file | لا يمكن تحليل الملف: {str(e)}")
        return errors
    
    upgrade_func = None
    downgrade_func = None
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == 'upgrade':
                upgrade_func = node
            elif node.name == 'downgrade':
                downgrade_func = node
    
    if not upgrade_func:
        errors.append("Missing upgrade() function | دالة upgrade() مفقودة")
    else:
        if upgrade_func.returns:
            if isinstance(upgrade_func.returns, ast.Constant):
                if upgrade_func.returns.value is not None:
                    errors.append("upgrade() should return None (-> None) | upgrade() يجب أن ترجع None")
            elif not (isinstance(upgrade_func.returns, ast.Name) and upgrade_func.returns.id == 'None'):
                if not isinstance(upgrade_func.returns, ast.Constant):
                    errors.append("upgrade() should return None (-> None) | upgrade() يجب أن ترجع None")
        
        if len(upgrade_func.body) == 0:
            errors.append("upgrade() function is completely empty | دالة upgrade() فارغة تماماً")
        elif len(upgrade_func.body) == 1 and isinstance(upgrade_func.body[0], ast.Pass):
            pass
        elif len(upgrade_func.body) == 1 and isinstance(upgrade_func.body[0], ast.Expr) and isinstance(upgrade_func.body[0].value, ast.Constant):
            pass
    
    if not downgrade_func:
        errors.append("Missing downgrade() function | دالة downgrade() مفقودة")
    else:
        if downgrade_func.returns:
            if isinstance(downgrade_func.returns, ast.Constant):
                if downgrade_func.returns.value is not None:
                    errors.append("downgrade() should return None (-> None) | downgrade() يجب أن ترجع None")
            elif not (isinstance(downgrade_func.returns, ast.Name) and downgrade_func.returns.id == 'None'):
                if not isinstance(downgrade_func.returns, ast.Constant):
                    errors.append("downgrade() should return None (-> None) | downgrade() يجب أن ترجع None")
        
        if len(downgrade_func.body) == 0:
            errors.append("downgrade() function is completely empty | دالة downgrade() فارغة تماماً")
    
    return errors


def validate_revision_format(file_path: str, all_revisions: Optional[Set[str]] = None) -> List[str]:
    """
    Validate revision ID format and uniqueness
    التحقق من صحة معرف الـ revision وتفرده
    
    Checks:
    - Revision ID format is valid / صحة معرف الـ revision
    - Revision is unique / الـ revision فريد
    - down_revision is valid / down_revision صحيح
    
    Args:
        file_path: Path to migration file
        all_revisions: Set of all known revisions for uniqueness check
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if not os.path.exists(file_path):
        errors.append(f"File does not exist | الملف غير موجود: {file_path}")
        return errors
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content, filename=file_path)
    except Exception as e:
        errors.append(f"Cannot parse file | لا يمكن تحليل الملف: {str(e)}")
        return errors
    
    revision = None
    down_revision = None
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == 'revision' and isinstance(node.value, ast.Constant):
                        revision = node.value.value
                    elif target.id == 'down_revision':
                        if isinstance(node.value, ast.Constant):
                            down_revision = node.value.value
    
    if not revision:
        errors.append("Revision ID not found or invalid | معرف الـ revision غير موجود أو غير صحيح")
    else:
        if not isinstance(revision, str):
            errors.append(f"Revision ID must be a string | معرف الـ revision يجب أن يكون نص: {type(revision)}")
        elif len(revision.strip()) == 0:
            errors.append("Revision ID is empty | معرف الـ revision فارغ")
        elif len(revision) < 3:
            errors.append(f"Revision ID is too short | معرف الـ revision قصير جداً: '{revision}'")
        
        if all_revisions is not None and revision in all_revisions:
            errors.append(f"Revision ID is not unique | معرف الـ revision غير فريد: '{revision}'")
    
    if down_revision is not None and not isinstance(down_revision, str):
        if down_revision is not None:
            errors.append(f"down_revision must be a string or None | down_revision يجب أن يكون نص أو None")
    
    return errors


def check_sql_injection(file_path: str) -> List[str]:
    """
    Check for SQL injection patterns
    فحص أنماط SQL injection الخطيرة
    
    Checks:
    - Dangerous SQL injection patterns / أنماط SQL injection خطيرة
    - String concatenation in SQL / دمج النصوص في SQL
    - Use of parameterized queries / استخدام parameterized queries
    
    Args:
        file_path: Path to migration file
        
    Returns:
        List of warning messages (empty if safe)
    """
    warnings = []
    
    if not os.path.exists(file_path):
        return [f"File does not exist | الملف غير موجود: {file_path}"]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Cannot read file | لا يمكن قراءة الملف: {str(e)}"]
    
    sql_concat_patterns = [
        (r'["\']\s*\+\s*[a-zA-Z_][a-zA-Z0-9_]*', 'String concatenation with variable'),
        (r'[a-zA-Z_][a-zA-Z0-9_]*\s*\+\s*["\']', 'Variable concatenation with string'),
        (r'%s.*%.*\(', 'Old-style string formatting with variables'),
        (r'\.format\([a-zA-Z_]', 'String format with variables'),
        (r'f["\'].*\{[a-zA-Z_]', 'F-string with variables in SQL'),
    ]
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        if any(keyword in line_lower for keyword in ['select', 'insert', 'update', 'delete', 'alter', 'drop', 'create']):
            for pattern, description in sql_concat_patterns:
                if re.search(pattern, line):
                    warnings.append(
                        f"Line {i}: Possible SQL injection risk - {description} | "
                        f"السطر {i}: احتمال وجود SQL injection - {description}\n"
                        f"  {line.strip()}"
                    )
    
    execute_pattern = r'op\.execute\s*\(["\'].*\+.*["\']'
    if re.search(execute_pattern, content, re.MULTILINE):
        warnings.append(
            "Found op.execute() with string concatenation | "
            "وجد op.execute() مع دمج نصوص - استخدم parameterized queries"
        )
    
    return warnings


def validate_batch_mode(file_path: str) -> List[str]:
    """
    Validate batch_alter_table usage for SQLite compatibility
    التحقق من استخدام batch_alter_table للتوافق مع SQLite
    
    Checks:
    - Use of batch_alter_table for SQLite / استخدام batch_alter_table
    - Direct ALTER TABLE statements / جمل ALTER TABLE مباشرة
    
    Args:
        file_path: Path to migration file
        
    Returns:
        List of warning messages (empty if valid)
    """
    warnings = []
    
    if not os.path.exists(file_path):
        return [f"File does not exist | الملف غير موجود: {file_path}"]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Cannot read file | لا يمكن قراءة الملف: {str(e)}"]
    
    lines = content.split('\n')
    
    has_alter_column = False
    has_batch_alter = False
    
    for i, line in enumerate(lines, 1):
        if 'op.alter_column' in line and 'batch_op' not in line:
            has_alter_column = True
            warnings.append(
                f"Line {i}: Direct op.alter_column() without batch mode | "
                f"السطر {i}: استخدام op.alter_column() مباشرة بدون batch mode\n"
                f"  Consider using: with op.batch_alter_table('table_name') as batch_op:\n"
                f"  {line.strip()}"
            )
        
        if 'op.drop_column' in line and 'batch_op' not in line:
            warnings.append(
                f"Line {i}: Direct op.drop_column() without batch mode | "
                f"السطر {i}: استخدام op.drop_column() مباشرة بدون batch mode\n"
                f"  {line.strip()}"
            )
        
        if 'batch_alter_table' in line:
            has_batch_alter = True
    
    alter_table_pattern = r'op\.execute\s*\(["\'].*ALTER\s+TABLE.*["\']'
    matches = list(re.finditer(alter_table_pattern, content, re.IGNORECASE | re.MULTILINE))
    
    if matches:
        warnings.append(
            f"Found {len(matches)} direct ALTER TABLE statement(s) via op.execute() | "
            f"وجد {len(matches)} جملة ALTER TABLE مباشرة - قد لا تعمل مع SQLite"
        )
    
    if not has_batch_alter and has_alter_column:
        warnings.append(
            "Migration uses column alterations without batch mode | "
            "الـ Migration يستخدم تعديلات على الأعمدة بدون batch mode\n"
            "  For SQLite compatibility, use: with op.batch_alter_table('table') as batch_op:"
        )
    
    return warnings


def validate_all_migrations(migrations_dir: str = 'migrations/versions') -> Dict[str, Any]:
    """
    Validate all migrations in directory
    التحقق من جميع الـ migrations في المجلد
    
    Args:
        migrations_dir: Directory containing migration files
        
    Returns:
        Dictionary with validation results
    """
    print_header("Migration Validator | التحقق من صحة Migrations", Colors.CYAN)
    print_info(f"Scanning directory | فحص المجلد: {migrations_dir}")
    
    if not os.path.exists(migrations_dir):
        print_error(f"Directory does not exist | المجلد غير موجود: {migrations_dir}")
        return {'error': 'Directory not found'}
    
    migration_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.py') and not f.startswith('__')
    ])
    
    if not migration_files:
        print_warning(f"No migration files found | لم يتم العثور على ملفات migrations في: {migrations_dir}")
        return {'files': [], 'total': 0}
    
    print_success(f"Found {len(migration_files)} migration file(s) | وجد {len(migration_files)} ملف migrations\n")
    
    all_revisions = set()
    results = {
        'total_files': len(migration_files),
        'valid_files': 0,
        'files_with_errors': 0,
        'files_with_warnings': 0,
        'details': {}
    }
    
    for filename in migration_files:
        file_path = os.path.join(migrations_dir, filename)
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'─' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}📄 Checking | فحص: {filename}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'─' * 70}{Colors.RESET}\n")
        
        file_errors = []
        file_warnings = []
        
        errors = validate_migration_file(file_path)
        if errors:
            file_errors.extend(errors)
            for error in errors:
                print_error(error)
        
        errors = validate_upgrade_downgrade(file_path)
        if errors:
            file_errors.extend(errors)
            for error in errors:
                print_error(error)
        
        errors = validate_revision_format(file_path, all_revisions)
        if errors:
            file_errors.extend(errors)
            for error in errors:
                print_error(error)
        else:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == 'revision':
                                if isinstance(node.value, ast.Constant):
                                    all_revisions.add(node.value.value)
            except:
                pass
        
        warnings = check_sql_injection(file_path)
        if warnings:
            file_warnings.extend(warnings)
            for warning in warnings:
                print_warning(warning)
        
        warnings = validate_batch_mode(file_path)
        if warnings:
            file_warnings.extend(warnings)
            for warning in warnings:
                print_warning(warning)
        
        results['details'][filename] = {
            'errors': file_errors,
            'warnings': file_warnings
        }
        
        if file_errors:
            results['files_with_errors'] += 1
            print(f"\n{Colors.RED}{Colors.BOLD}❌ FAILED | فشل: {len(file_errors)} error(s){Colors.RESET}")
        elif file_warnings:
            results['files_with_warnings'] += 1
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  PASSED WITH WARNINGS | نجح مع تحذيرات: {len(file_warnings)} warning(s){Colors.RESET}")
        else:
            results['valid_files'] += 1
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ PASSED | نجح{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print_header("Summary | الملخص", Colors.CYAN)
    
    print(f"{Colors.BOLD}Total Files | إجمالي الملفات:{Colors.RESET} {results['total_files']}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ Valid | صحيح:{Colors.RESET} {results['valid_files']}")
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  With Warnings | مع تحذيرات:{Colors.RESET} {results['files_with_warnings']}")
    print(f"{Colors.RED}{Colors.BOLD}❌ With Errors | مع أخطاء:{Colors.RESET} {results['files_with_errors']}")
    
    if results['files_with_errors'] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All migrations passed validation! | جميع الـ migrations صحيحة!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  Some migrations have errors. Please fix them before deploying.{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}   بعض الـ migrations بها أخطاء. يرجى إصلاحها قبل النشر.{Colors.RESET}")
    
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")
    
    return results


def main():
    """CLI interface for migration validator"""
    parser = argparse.ArgumentParser(
        description='K2Panel Migration Validator | التحقق من صحة Migrations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples | أمثلة:
  python migrations/migration_validator.py
  python migrations/migration_validator.py --file migrations/versions/001_initial_baseline.py
  python migrations/migration_validator.py --dir migrations/versions
  python migrations/migration_validator.py --no-color
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Validate a single migration file | التحقق من ملف واحد',
        type=str
    )
    
    parser.add_argument(
        '--dir', '-d',
        help='Directory containing migrations (default: migrations/versions)',
        default='migrations/versions',
        type=str
    )
    
    parser.add_argument(
        '--no-color',
        help='Disable colored output | تعطيل الألوان',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()
    
    if args.file:
        print_header(f"Validating Single File | التحقق من ملف واحد", Colors.CYAN)
        print_info(f"File | الملف: {args.file}\n")
        
        errors = validate_migration_file(args.file)
        if errors:
            print_error("File Structure Issues | مشاكل في بنية الملف:")
            for error in errors:
                print(f"  • {error}")
        
        errors = validate_upgrade_downgrade(args.file)
        if errors:
            print_error("\nUpgrade/Downgrade Issues | مشاكل في upgrade/downgrade:")
            for error in errors:
                print(f"  • {error}")
        
        errors = validate_revision_format(args.file)
        if errors:
            print_error("\nRevision Format Issues | مشاكل في معرف الـ revision:")
            for error in errors:
                print(f"  • {error}")
        
        warnings = check_sql_injection(args.file)
        if warnings:
            print_warning("\nSQL Injection Warnings | تحذيرات SQL injection:")
            for warning in warnings:
                print(f"  • {warning}")
        
        warnings = validate_batch_mode(args.file)
        if warnings:
            print_warning("\nBatch Mode Warnings | تحذيرات batch mode:")
            for warning in warnings:
                print(f"  • {warning}")
        
        total_issues = len(errors) + len(warnings)
        if total_issues == 0:
            print_success("\n✅ File passed all validations! | الملف صحيح!")
        else:
            print_error(f"\n❌ Found {total_issues} issue(s) | وجد {total_issues} مشكلة")
    else:
        validate_all_migrations(args.dir)


if __name__ == '__main__':
    main()
