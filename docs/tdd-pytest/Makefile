help:
	@echo 'Usage:'
	@echo '  make docs 			generate local docs (and serve on localhost)'
	@echo '  make ghp 			regenerate docs and push to github pages'

docs:
	mkdocs serve

ghp:
	rm -rf ./build/*
	mkdocs gh-deploy

.PHONY: help
