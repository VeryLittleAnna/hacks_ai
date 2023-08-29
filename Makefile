# Makefile

# Set the default target to start both Django and React servers
.DEFAULT_GOAL := run

# Define the virtual environment activation command
VENV_ACTIVATE := . myenv/bin/activate

# Define commands for starting Django and React servers
DJANGO_CMD := $(VENV_ACTIVATE) && python3 fullstack_django/manage.py runserver
REACT_CMD := npm start --prefix frontend

# ⛹️‍♂️ Target to start both Django and React servers and environment
run:
#	@echo "Activating virtual environment..."
#	@$(VENV_ACTIVATE) && echo "Virtual environment activated."
	@echo "Starting Django server..."
	@$(DJANGO_CMD) &
	@echo "Starting React server..."
	@$(REACT_CMD)

run-env:
	@$(VENV_ACTIVATE) && echo "Virtual environment activated."
# Target to start only Django server
run-django:
	@$(DJANGO_CMD)

# ☢️ Target to start only React server
run-react:
	@$(REACT_CMD)

# ⛔️ Target to stop both servers
stop:
	@echo "Stopping servers..."
	@pkill -f "$(DJANGO_CMD)"
	@pkill -f "$(REACT_CMD)"

.PHONY: run run-django run-react stop
