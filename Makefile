.PHONY: run

api:
	uvicorn amergebot.api.app:app --host="0.0.0.0" --port=8000

slack:
	python -m amergebot.apps.slack
