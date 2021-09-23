
black:
	black .

clean:
	-rm -r build/*
	-(cd docs/; make clean)
	find src/ docs/ tests/ -name '*.pyc' -exec rm -f {} +
	find src/ docs/ tests/ -name '*.pyo' -exec rm -f {} +
	find src/ docs/ tests/ -name '*~' -exec rm -f {} +
	find src/ docs/ tests/ -name '__pycache__' -exec rm -fr {} +
	find src/ -name '*.htm' -exec rm -f {} +
	find src/ -name '*.html' -exec rm -f {} +
	find src/ -name '*.so' -exec rm -f {} +
	find src/ -name 'octave-workspace' -exec rm -f {} +
	-rm -r dist/*
	-rm -r src/*.egg-info

demo:
	python demo/demo.py

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
	make docs
	make test_quick

test_quick:
	make clean
	HYPOTHESIS_PROFILE=dev pytest --cov=bewegung --cov-config=setup.cfg --hypothesis-show-statistics # --capture=no
	coverage html

.PHONY: clean demo docs release test
