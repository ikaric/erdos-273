.PHONY: help init

help:
	@echo "formalia — available make targets:"
	@echo ""
	@echo "  make init   One-time per-clone setup. Prompts for your GitHub"
	@echo "              username, full name, and email; substitutes the"
	@echo "              GH_USERNAME, GIT_USER_NAME, GIT_USER_EMAIL"
	@echo "              placeholders across template files; sets repo-local"
	@echo "              git config. Idempotent — safe to re-run."
	@echo ""
	@echo "              Non-interactive form:"
	@echo "                GH_USERNAME=foo GIT_USER_NAME='Foo Bar' \\"
	@echo "                  GIT_USER_EMAIL=foo@bar.com make init"
	@echo ""
	@echo "  make help   Show this message."

init:
	@command -v python3 >/dev/null 2>&1 || { \
	  echo "error: python3 is required (install via brew, your package manager, or pyenv)" >&2; \
	  exit 1; \
	}
	@python3 scripts/init.py
