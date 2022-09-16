CONTAINER_MGR ?= podman

build-container:
	$(CONTAINER_MGR) build -t localhost/pl-graphicsmagick .

build-wheel:
	source venv/bin/activate && \
		python3 -m pip install --editable .

virtualenv:
	python3 -m virtualenv venv

virtualenv-requirements: virtualenv
	source venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install -r test-requirements.txt

test: build-wheel
	source ./venv/bin/activate && \
		pytest -o cache_dir=tmp/pytest
