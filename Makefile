# Vars
CODE_DIR =  bot
PYTHONPATH = PYTHONPATH=./:$(CODE_DIR)

# Executables
PYTHON = $(PYTHONPATH) python3
POETRY = $(PYTHONPATH) poetry run
ALEMBIC = $(PYTHONPATH) alembic -c $(CODE_DIR)/databases/alembic.ini

# Params
DOWNGRADE_DEFAULT = -1

.PHONY: migrations db_upgrade db_downgrade pretty help


migrations:  ## Создать миграции
	$(ALEMBIC) revision --autogenerate -m "$(message)"

db_upgrade:  ## Запуск миграций
	$(ALEMBIC) upgrade head

db_downgrade:  ## Откат до предыдущей (по умолчанию) миграции
	$(ALEMBIC) downgrade $(DOWNGRADE_DEFAULT)

pretty: ## Причесать код
	isort .
	black .
	autoflake --in-place --verbose -r .

help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
