# Makefile

RUBY_VERSION := 3.2.2
RUBY := $(shell command -v ruby 2>/dev/null)
RBENV := $(HOME)/.rbenv/bin/rbenv

.PHONY: all check-ruby install-ruby install-ruby-deps install-python-deps regenerate_docs init clean

# Default target
all: check-ruby install-ruby-deps install-python-deps regenerate_docs

# Check if Ruby is installed, otherwise install via rbenv
check-ruby:
	@if [ -z "$(RUBY)" ]; then \
		echo "Ruby not found. Installing Ruby $(RUBY_VERSION) using rbenv..."; \
		curl -fsSL https://github.com/rbenv/rbenv-installer/raw/main/bin/rbenv-installer | bash; \
		export PATH="$(HOME)/.rbenv/bin:$(PATH)"; \
		eval "$$($(RBENV) init -)"; \
		$(RBENV) install $(RUBY_VERSION); \
		$(RBENV) global $(RUBY_VERSION); \
	else \
		echo "Ruby is already installed: $(RUBY)"; \
	fi

# Install bundler and gems
install-ruby-deps:
	@if [ ! -f Gemfile ]; then make init; fi
	bundle install


# Install bundler and gems
install-python-deps:
	pip install -r requirements.txt -q
	@echo "Adding Ansible collections path to site-packages..."
	@SITE_PACKAGES=$$(python -c 'import site; print(site.getsitepackages()[0])'); \
	PTH_FILE="$$SITE_PACKAGES/ansible_collections.pth"; \
	ANSIBLE_PATH="$$HOME/.ansible/collections"; \
	if [ -d "$$ANSIBLE_PATH" ]; then \
		if [ ! -f "$$PTH_FILE" ] || ! grep -Fxq "$$ANSIBLE_PATH" "$$PTH_FILE"; then \
			echo "$$ANSIBLE_PATH" >> "$$PTH_FILE"; \
			echo "✅ Added $$ANSIBLE_PATH to $$PTH_FILE"; \
		else \
			echo "✅ Path already present in $$PTH_FILE, skipping"; \
		fi \
	else \
		echo "⚠️  Skipped: $$ANSIBLE_PATH does not exist"; \
	fi

# Run the script
regenerate_docs: check-ruby install-ruby-deps install-python-deps
	./regenerate_docs.sh

# Create a basic Gemfile
init:
	@echo "source 'https://rubygems.org'" > Gemfile
	@echo "gem 'oas_parser'" >> Gemfile
	@echo "gem 'activesupport', '~> 7.0'" >> Gemfile
	@echo "Gemfile created."

# Optional cleanup
clean:
	rm -rf .bundle vendor Gemfile.lock
