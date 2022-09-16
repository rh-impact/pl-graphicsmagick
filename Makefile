CONTAINER_MGR ?= podman

build:
	$(CONTAINER_MGR) build -t localhost/pl-graphicsmagick .

virtualenv:
	python3 -m virtualenv venv

virtualenv-requirements: virtualenv
	source venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install -r test-requirements.txt

test:
	source ./venv/bin/activate && \
		pytest -o cache_dir=tmp/pytest
