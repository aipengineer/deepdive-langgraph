# Terminal colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
BLUE   := $(shell tput -Txterm setaf 4)
RED    := $(shell tput -Txterm setaf 1)

# Python settings
PYTHON_VERSION = 3.13.0
VENV_PATH = .venv
VENV_BIN = $(VENV_PATH)/bin
PYTHON = $(VENV_BIN)/python
ACTIVATE = . $(VENV_BIN)/activate

.PHONY: help
help: ## Show this help message
	@echo ''
	@echo '${YELLOW}LangGraph Tutorial Development Guide${RESET}'
	@echo ''
	@echo '${YELLOW}Quick Start:${RESET}'
	@echo '  One-command setup:'
	@echo '  ${GREEN}make setup${RESET}   - Creates environment and installs all dependencies'
	@echo ''
	@echo '${YELLOW}Development Workflow:${RESET}'
	@echo '  1. ${GREEN}source .venv/bin/activate${RESET} - Activate virtual environment'
	@echo '  2. ${GREEN}make format${RESET}       - Format code before committing'
	@echo '  3. ${GREEN}make lint${RESET}         - Check code style'
	@echo '  4. ${GREEN}make test${RESET}         - Run tests'
	@echo '  5. ${GREEN}make structure${RESET}    - Display project structure'
	@echo ''
	@echo '${YELLOW}Available Targets:${RESET}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${GREEN}%s${RESET}\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Create environment and install dependencies
	@echo "${BLUE}Setting up development environment...${RESET}"
	@echo "${BLUE}Using Python ${PYTHON_VERSION}${RESET}"
	pyenv local ${PYTHON_VERSION}
	uv venv
	$(ACTIVATE) && uv pip install -e ".[dev]"
	@echo "${GREEN}Environment created and dependencies installed${RESET}"
	@echo "${YELLOW}To activate the environment:${RESET}"
	@echo "${GREEN}source ${VENV_PATH}/bin/activate${RESET}"

.PHONY: format
format: ## Format code with ruff
	@echo "${BLUE}Formatting code...${RESET}"
	$(ACTIVATE) && ruff format .
	$(ACTIVATE) && ruff check --fix .

.PHONY: lint
lint: ## Check style with ruff
	@echo "${BLUE}Linting code...${RESET}"
	$(ACTIVATE) && ruff check .

.PHONY: test
test: ## Run tests with pytest
	@echo "${BLUE}Running tests...${RESET}"
	$(ACTIVATE) && pytest -v tests/ --disable-socket

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests (requires API keys)
	@echo "${BLUE}Running end-to-end tests...${RESET}"
	$(ACTIVATE) && pytest -v tests/ --use-real-api

.PHONY: clean
clean: ## Remove all generated files
	@echo "${BLUE}Cleaning generated files...${RESET}"
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "${GREEN}Clean complete!${RESET}"

.PHONY: structure
structure: ## Show current project structure
	@echo "${YELLOW}Current Project Structure:${RESET}"
	@echo "${BLUE}"
	@if command -v tree > /dev/null; then \
		tree -a -I '.git|.venv|__pycache__|*.pyc|*.pyo|*.pyd|.pytest_cache|.ruff_cache|.coverage|htmlcov'; \
	else \
		echo "Note: Install 'tree' for better directory visualization:"; \
		echo "  macOS:     brew install tree"; \
		echo "  Ubuntu:    sudo apt-get install tree"; \
		echo "  Fedora:    sudo dnf install tree"; \
		echo ""; \
		find . -not -path '*/\.*' -not -path '*.pyc' -not -path '*/__pycache__/*' \
			-not -path './.venv/*' -not -path './build/*' -not -path './dist/*' \
			-not -path './*.egg-info/*' \
			| sort \
			| sed -e "s/[^-][^\/]*\// │   /g" -e "s/├── /│── /" -e "s/└── /└── /"; \
	fi
	@echo "${RESET}"


.DEFAULT_GOAL := help