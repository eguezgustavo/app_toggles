deploy:
	poetry version ${VERSION}
	git tag v${VERSION}
	git push origin v${VERSION}
