#!/bin/bash
# Development helper script for Docker operations

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored message
print_msg() {
    echo -e "${BLUE}[SaaS Planz]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Show usage
show_usage() {
    cat << EOF
${BLUE}SaaS Planz - Docker Development Commands${NC}

Usage: ./docker-dev.sh [command]

Commands:
  ${GREEN}start${NC}        - Build and start the application
  ${GREEN}stop${NC}         - Stop the application
  ${GREEN}restart${NC}      - Restart the application
  ${GREEN}logs${NC}         - Show application logs (follow mode)
  ${GREEN}test${NC}         - Run all tests in Docker
  ${GREEN}test-models${NC}  - Run model tests only (no dependencies)
  ${GREEN}test-parser${NC}  - Run parser validation (requires pandas)
  ${GREEN}shell${NC}        - Open bash shell in running container
  ${GREEN}clean${NC}        - Stop and remove containers, images, volumes
  ${GREEN}rebuild${NC}      - Clean rebuild (no cache)
  ${GREEN}status${NC}       - Show container status
  ${GREEN}url${NC}          - Show application URL

Examples:
  ./docker-dev.sh start       # Start the app
  ./docker-dev.sh logs        # View logs
  ./docker-dev.sh test        # Run tests
  ./docker-dev.sh shell       # Open shell for debugging

EOF
}

# Check if docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        print_error "Docker Compose is not installed."
        exit 1
    fi
}

# Start application
start_app() {
    print_msg "Building and starting SaaS Planz application..."
    docker compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_success "Application started successfully!"
        echo ""
        print_msg "Application URL: ${GREEN}http://localhost:8501${NC}"
        echo ""
        print_msg "Use './docker-dev.sh logs' to view logs"
        print_msg "Use './docker-dev.sh stop' to stop the application"
    else
        print_error "Failed to start application"
        exit 1
    fi
}

# Stop application
stop_app() {
    print_msg "Stopping application..."
    docker compose down
    print_success "Application stopped"
}

# Restart application
restart_app() {
    print_msg "Restarting application..."
    docker compose restart
    print_success "Application restarted"
}

# Show logs
show_logs() {
    print_msg "Showing application logs (Ctrl+C to exit)..."
    docker compose logs -f app
}

# Run tests
run_tests() {
    print_msg "Running all tests..."
    docker compose run --rm test
}

# Run model tests only
run_model_tests() {
    print_msg "Running model tests (no dependencies)..."
    docker compose run --rm app python3 /app/scripts/test_models_only.py
}

# Run parser validation
run_parser_tests() {
    print_msg "Running parser validation..."
    docker compose run --rm app python3 /app/scripts/manual_test.py
}

# Open shell
open_shell() {
    print_msg "Opening bash shell in container..."
    docker compose exec app bash || docker compose run --rm app bash
}

# Clean everything
clean_all() {
    print_warning "This will remove all containers, images, and volumes."
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_msg "Cleaning up..."
        docker compose down -v --rmi all
        print_success "Cleanup complete"
    else
        print_msg "Cleanup cancelled"
    fi
}

# Rebuild from scratch
rebuild_app() {
    print_msg "Rebuilding application (no cache)..."
    docker compose down
    docker compose build --no-cache
    docker compose up -d
    print_success "Rebuild complete"
}

# Show status
show_status() {
    print_msg "Container status:"
    docker compose ps
}

# Show URL
show_url() {
    echo ""
    echo "📱 Application URL: ${GREEN}http://localhost:8501${NC}"
    echo ""
    
    if docker compose ps | grep -q "Up"; then
        print_success "Application is running"
    else
        print_warning "Application is not running. Use './docker-dev.sh start' to start it."
    fi
    echo ""
}

# Main script
main() {
    check_docker
    
    case "${1:-}" in
        start)
            start_app
            ;;
        stop)
            stop_app
            ;;
        restart)
            restart_app
            ;;
        logs)
            show_logs
            ;;
        test)
            run_tests
            ;;
        test-models)
            run_model_tests
            ;;
        test-parser)
            run_parser_tests
            ;;
        shell)
            open_shell
            ;;
        clean)
            clean_all
            ;;
        rebuild)
            rebuild_app
            ;;
        status)
            show_status
            ;;
        url)
            show_url
            ;;
        *)
            show_usage
            ;;
    esac
}

main "$@"
