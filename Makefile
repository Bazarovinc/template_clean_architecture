#!make

CI_PROJECT_PATH := dreap/backend/template
CI_COMMIT_REF_SLUG := $(shell git rev-parse --abbrev-ref HEAD)
CI_COMMIT_SHORT_SHA := $(shell git rev-parse --short HEAD)
CI_ENV := $(shell cat .env |cut -f 2 -d" "|sed 's/^/--env /g'|xargs)
CI_WORKDIR := $(shell pwd)
CI_COMMAND := gitlab-runner -l info exec docker \
      --docker-privileged \
      --cache-dir "/cache" \
      $(CI_ENV) \
	  --env "CI_COMMIT_REF_SLUG=${CI_COMMIT_REF_SLUG}" \
	  --env "CI_PROJECT_PATH=${CI_PROJECT_PATH}" \
	  --env "CI_COMMIT_SHORT_SHA=${CI_COMMIT_SHORT_SHA}" \
  	  --docker-volumes "$(CI_WORKDIR)/key.json:/tmp/key.json" \
  	  --docker-volumes "/certs/client"

ci-build:
	$(CI_COMMAND) build

ci-isort:
	$(CI_COMMAND) lint-isort

ci-black:
	$(CI_COMMAND) lint-black

ci-mypy:
	$(CI_COMMAND) lint-mypy

ci-test:
	$(CI_COMMAND) test

test-env:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build -d control-center schema-registry zookeeper kafka db
