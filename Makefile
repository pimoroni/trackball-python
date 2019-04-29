LIBRARY_VERSION=`cat library/setup.py | grep version | awk -F"'" '{print $$2}'`
LIBRARY_NAME=`cat library/setup.py | grep name | awk -F"'" '{print $$2}'`

.PHONY: usage install uninstall
usage:
	@echo Library: ${LIBRARY_NAME} v$(LIBRARY_VERSION)
	@echo "Usage: make <target>, where target is one of:\n"
	@echo "install:       install the library locally from source"
	@echo "uninstall:     uninstall the local library"
	@echo "python-readme: generate library/README.rst from README.md"
	@echo "python-wheels: build python .whl files for distribution"
	@echo "python-sdist:  build python source distribution"
	@echo "python-clean:  clean python build and dist directories"
	@echo "python-dist:   build all python distribution files" 

install:
	./install.sh

uninstall:
	./uninstall.sh

sanity-check:
	@echo "Checking library/CHANGELOG.txt"
	@cat library/CHANGELOG.txt | grep ^${LIBRARY_VERSION}
	@echo "Checking library/${LIBRARY_NAME}/__init__.py"
	@cat library/${LIBRARY_NAME}/__init__.py | grep "^__version__ = '${LIBRARY_VERSION}'"

python-readme: library/README.rst

python-license: library/LICENSE.txt

library/README.rst: README.md
	pandoc --from=markdown --to=rst -o library/README.rst README.md

library/LICENSE.txt: LICENSE
	cp LICENSE library/LICENSE.txt

python-wheels: python-readme python-license
	cd library; python3 setup.py bdist_wheel
	cd library; python setup.py bdist_wheel

python-sdist: python-readme python-license
	cd library; python setup.py sdist

python-clean:
	-rm -r library/dist
	-rm -r library/build
	-rm -r library/*.egg-info

python-dist: python-clean python-wheels python-sdist
	ls library/dist

python-deploy: sanity-check python-dist
	twine upload library/dist/*

python-deploy-test: python-dist
	twine upload --repository-url https://test.pypi.org/legacy/ library/dist/*
