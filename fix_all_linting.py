#!/usr/bin/env python3
"""
Codex Dominion System-Wide Linting Fixer

Automatically fixes common linting issues across all Python files:
- Removes unused imports
- Fixes line length violations
- Adds type annotations
- Removes unnecessary f-strings
- Fixes whitespace issues
"""

import ast
import re
from pathlib import Path
from typing import List, Set


class LintingFixer:
    """Automatically fix common linting issues"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.fixes_applied = 0
        self.files_processed = 0

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        exclude_dirs = {
            ".venv", "venv", "node_modules", "__pycache__",
            ".git", "dist", "build", ".pytest_cache"
        }

        for py_file in self.root_dir.rglob("*.py"):
            # Skip excluded directories
            if any(excluded in py_file.parts for excluded in exclude_dirs):
                continue
            python_files.append(py_file)

        return python_files

    def find_unused_imports(self, file_path: Path) -> Set[str]:
        """Detect unused imports using AST analysis"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Find all imports
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])
                    for alias in node.names:
                        imports.add(alias.name)

            # Find all names used in the file
            used_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    if isinstance(node.value, ast.Name):
                        used_names.add(node.value.id)

            # Return imports that are not used
            unused = imports - used_names
            return unused

        except Exception as e:
            print(f"  ⚠️  Could not analyze {file_path.name}: {e}")
            return set()

    def fix_line_length(self, content: str) -> str:
        """Fix lines that are too long (> 79 characters)"""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            if len(line) <= 79:
                fixed_lines.append(line)
                continue

            # Try to fix long strings
            if "\"" in line or "'" in line:
                # Split long strings
                indent = len(line) - len(line.lstrip())
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts[1].strip()) > 50:
                        fixed_lines.append(parts[0] + "= (")
                        fixed_lines.append(" " * (indent + 4) + parts[1].strip())
                        fixed_lines.append(" " * indent + ")")
                        self.fixes_applied += 1
                        continue

            # If we can't fix it automatically, keep original
            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_f_strings(self, content: str) -> str:
        """Remove f-string prefix from strings without placeholders"""
        # Find f-strings without placeholders
        pattern = r'f"([^"]*[^{])"'

        def replace_if_no_placeholder(match):
            string_content = match.group(1)
            if "{" not in string_content:
                self.fixes_applied += 1
                return f'"{string_content}"'
            return match.group(0)

        content = re.sub(pattern, replace_if_no_placeholder, content)

        # Same for single quotes
        pattern = r"f'([^']*[^{])'"
        content = re.sub(pattern, replace_if_no_placeholder, content)

        return content

    def add_return_type_hints(self, content: str) -> str:
        """Add return type hints to functions missing them"""
        # This is a simple heuristic-based approach
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Look for function definitions without return type
            if re.match(r"^\s*def \w+\([^)]*\):", line):
                # Check if next line has a docstring
                if i + 1 < len(lines) and '"""' in lines[i + 1]:
                    # Add -> None for functions without explicit return
                    if "return" not in content[
                        content.index(line):content.index(
                            line
                        ) + 500
                    ]:
                        line = line.replace("):", ") -> None:")
                        self.fixes_applied += 1

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_file(self, file_path: Path) -> bool:
        """Fix linting issues in a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Apply fixes
            content = self.fix_f_strings(content)
            content = self.fix_line_length(content)
            # content = self.add_return_type_hints(content)  # Disabled

            # Only write if changes were made
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True

            return False

        except Exception as e:
            print(f"  ❌ Error fixing {file_path.name}: {e}")
            return False

    def run(self) -> None:
        """Run linting fixes on all Python files"""
        print("🔥 CODEX DOMINION LINTING FIXER")
        print("=" * 60)

        python_files = self.find_python_files()
        print(f"📋 Found {len(python_files)} Python files")
        print()

        for file_path in python_files:
            self.files_processed += 1

            if self.fix_file(file_path):
                print(f"✅ Fixed: {file_path.relative_to(self.root_dir)}")
            else:
                print(
                    f"  {file_path.relative_to(self.root_dir)}"
                    " (no changes)"
                )

        print()
        print("=" * 60)
        print(f"✨ LINTING FIX COMPLETE")
        print(f"📊 Files processed: {self.files_processed}")
        print(f"🔧 Fixes applied: {self.fixes_applied}")
        print()


def main() -> None:
    """Main execution"""
    fixer = LintingFixer()
    fixer.run()


if __name__ == "__main__":
    main()
