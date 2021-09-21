
black:
	black .

clean:
	-rm -r build/*
	-(cd docs/; make clean)
	find src/ docs/ -name '*.pyc' -exec rm -f {} +
	find src/ docs/ -name '*.pyo' -exec rm -f {} +
	find src/ docs/ -name '*~' -exec rm -f {} +
	find src/ docs/ -name '__pycache__' -exec rm -fr {} +
	find src/ -name '*.htm' -exec rm -f {} +
	find src/ -name '*.html' -exec rm -f {} +
	find src/ -name '*.so' -exec rm -f {} +
	find src/ -name 'octave-workspace' -exec rm -f {} +
	-rm -r dist/*
	-rm -r src/*.egg-info

docs:
	@(cd docs; make clean; make html)

release:
	make clean
	python setup.py sdist bdist_wheel
	python setup.py sdist
	gpg --detach-sign -a dist/bewegung*.whl
	gpg --detach-sign -a dist/bewegung*.tar.gz

install:
	pip install -vU pip setuptools
	pip install -v -e .[all]

upload:
	for filename in $$(ls dist/*.tar.gz dist/*.whl) ; do \
		twine upload $$filename $$filename.asc ; \
	done

test:
	python demo/demo.py

.PHONY: clean docs release test
