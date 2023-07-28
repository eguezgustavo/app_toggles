deploy:
	poetry version ${VERSION}
	poetry build
	git tag v${VERSION}
	git push origin v${VERSION}
	poetry publish
