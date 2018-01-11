ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

IMAGE_NAME        ?= opencord/mavenrepo
DOCKER_REGISTRY   ?= docker-registry:5000
DEPLOY_DOCKER_TAG ?= candidate

MAKE_CONFIG       ?= config.mk
ifeq ($(realpath $(MAKE_CONFIG)),)
$(info Makefile configuration not found, defaults will be used.)
else
$(info Using makefile configuration "$(MAKE_CONFIG)")
include $(MAKE_CONFIG)
endif

.PHONY: all
all: build

.PHONY: build
build:
	docker build -f Dockerfile.make -t $(IMAGE_NAME):$(DEPLOY_DOCKER_TAG) $(ROOT_DIR)

.PHONY: onos
onos:
	docker build -t cord/onos:latest -f docker/Dockerfile.onos .

.PHONY: publish
publish:
	docker tag $(IMAGE_NAME):$(DEPLOY_DOCKER_TAG) $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(DEPLOY_DOCKER_TAG)
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(DEPLOY_DOCKER_TAG)

.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME):$(DEPLOY_DOCKER_TAG) | true
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(DEPLOY_DOCKER_TAG) | true

.PHONY: test
test:
	@echo "No unit tests at present"

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build:  build the Docker image (Maven repo with the CORD ONOS apps)"
	@echo "  clean:  remove the Docker image"
	@echo "  test:   run unit tests"
	@echo "  help:   print this help message"

