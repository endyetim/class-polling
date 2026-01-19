.PHONY: import-polls run clean

# Import polls from polls.yaml
import-polls:
	@python import_polls.py

# Run Streamlit app
run:
	@~/.local/bin/uv run streamlit run poll_app.py

# Import and run
start: import-polls run

# Clean data
clean:
	@rm -f polls_data.json
	@echo "✓ Cleared poll data"

# Help
help:
	@echo "Available commands:"
	@echo "  make import-polls  - Import polls from polls.yaml"
	@echo "  make run          - Run Streamlit app"
	@echo "  make start        - Import polls and run app"
	@echo "  make clean        - Clear all poll data"
