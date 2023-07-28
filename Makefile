install/dev_env:
	poetry run pre-commit install

deploy:
	poetry version ${VERSION}
	poetry build
	git tag v${VERSION}
	git push origin v${VERSION}
	poetry publish

format:
	poetry run black app_toggles
	poetry run isort app_toggles
	poetry run mypy app_toggles

test:
	poetry run pytest tests