#!/bin/bash

# wayru-os migration script
# Helps transition from Make + pip to Just + UV

set -e

echo "wayru-os migration script"
echo "========================"
echo ""

# Check if required tools are installed
check_dependencies() {
    echo "Checking dependencies..."

    # Check for just
    if ! command -v just &> /dev/null; then
        echo "ERROR: 'just' is not installed."
        echo "   Install it with: cargo install just"
        echo "   Or visit: https://github.com/casey/just#installation"
        exit 1
    else
        echo "OK: just is installed ($(just --version))"
    fi

    # Check for uv
    if ! command -v uv &> /dev/null; then
        echo "ERROR: 'uv' is not installed."
        echo "   Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo "   Or visit: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    else
        echo "OK: uv is installed ($(uv --version))"
    fi

    echo ""
}

# Backup old files
backup_old_files() {
    echo "Backing up old configuration files..."

    if [ -f "requirements.txt" ]; then
        cp requirements.txt requirements.txt.backup
        echo "OK: Backed up requirements.txt"
    fi

    if [ -f "Makefile" ]; then
        cp Makefile Makefile.backup
        echo "OK: Backed up Makefile"
    fi

    echo ""
}

# Setup new environment
setup_environment() {
    echo "Setting up new Python environment..."

    # Remove old virtual environment if it exists
    if [ -d ".venv" ]; then
        echo "Removing old virtual environment..."
        rm -rf .venv
    fi

    # Create new environment with uv
    echo "Creating new environment with uv..."
    uv sync

    echo "OK: Environment setup complete"
    echo ""
}

# Verify migration
verify_migration() {
    echo "Verifying migration..."

    # Test just commands
    if just --list > /dev/null 2>&1; then
        echo "OK: just recipes are working"
    else
        echo "ERROR: justfile has issues"
        exit 1
    fi

    # Test uv environment
    if uv run python --version > /dev/null 2>&1; then
        echo "OK: uv Python environment is working"
    else
        echo "ERROR: uv environment has issues"
        exit 1
    fi

    echo ""
}

# Show next steps
show_next_steps() {
    echo "Migration completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review the new justfile: cat justfile"
    echo "2. Check available commands: just"
    echo "3. Set up your profile in .env (copy from .env.example)"
    echo "4. Try a quick build: just full-build"
    echo ""
    echo "For more information:"
    echo "- Read MIGRATION.md for detailed changes"
    echo "- Read README.md for updated documentation"
    echo ""
    echo "Old files backed up with .backup extension"
    echo "You can now delete the old Makefile and requirements.txt if everything works"
}

# Main migration process
main() {
    echo "Starting migration process..."
    echo ""

    check_dependencies
    backup_old_files
    setup_environment
    verify_migration
    show_next_steps
}

# Run migration
main
