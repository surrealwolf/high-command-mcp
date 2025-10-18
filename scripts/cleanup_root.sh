#!/bin/bash
# Cleanup script for High-Command root directory
# Moves scattered files to appropriate locations

echo "🧹 Cleaning up High-Command root directory..."

# Move duplicate/old copilot instructions
if [ -f ".copilot-instructions.md" ]; then
    echo "❌ Removing duplicate .copilot-instructions.md (use .github/copilot-instructions.md)"
    rm .copilot-instructions.md
fi

# Move markdown files to docs/ (if they're not already there)
for file in COMPLETION_REPORT.md ENDPOINT_EXPANSION.md GETTING_STARTED.md ITERATION_SUMMARY.md PROJECT_SUMMARY.md; do
    if [ -f "$file" ] && [ ! -f "docs/$file" ]; then
        echo "📄 Moving $file to docs/"
        mv "$file" "docs/"
    elif [ -f "$file" ]; then
        echo "❌ Removing duplicate $file (already in docs/)"
        rm "$file"
    fi
done

# Move test/debug scripts to scripts/
for file in test_all_endpoints.py test_api.py test_api_data.py test_imports.py test_new_endpoints.py \
            check_campaigns.py check_pagination.py check_structure.py debug_api.py \
            discover_endpoints.py list_tools.py verify_project.py; do
    if [ -f "$file" ]; then
        echo "🧪 Moving $file to scripts/"
        mv "$file" "scripts/"
    fi
done

# Remove empty/unnecessary directories
for dir in asyncio json ui; do
    if [ -d "$dir" ] && [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        echo "🗑️  Removing empty directory: $dir"
        rmdir "$dir" 2>/dev/null || rm -rf "$dir"
    fi
done

# Remove coverage cache if empty
if [ -d "htmlcov" ] && [ ! -f "htmlcov/index.html" ]; then
    echo "🗑️  Removing htmlcov directory"
    rm -rf htmlcov
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Root directory now contains only:"
echo "  - Core files: README.md, LICENSE, Makefile, Dockerfile, docker-compose.yml, pyproject.toml"
echo "  - Configuration: .env.example, .gitignore"
echo "  - Documentation: PROJECT_STATUS.md, CONTRIBUTING.md, REORGANIZATION_SUMMARY.md"
echo "  - Folders: .github/, docs/, highcommand/, tests/, scripts/, venv/"
