help:
	@echo 'Usage:'
	@echo '  make docs 			generate local docs (and serve on localhost)'
	@echo '  make ghp 			regenerate docs and push to github pages'

docs:
	mkdocs serve

ghp:
	# mkdocs gh-deploy --clean
	# Mar 2016: deploying with mkdocs fails for unknown reason 
	mkdocs build
	ghp-import -n build
	git push origin gh-pages

.PHONY: help
