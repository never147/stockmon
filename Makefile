VERSION = $(shell cat .version)
DOCKER_TAG := 'never147/stockmon'

all: dev image k8s

clean:
	rm -rf venv

# Development
dev: lint

venv:
	python3.6 -m venv venv
	venv/bin/pip install -r requirements.txt

lint: venv
	venv/bin/pip install -r requirements_test.txt
	. venv/bin/activate && prospector -DFM

# Image
image: build upload

build:
	docker build -t $(DOCKER_TAG):$(VERSION) .

upload:
	docker push $(DOCKER_TAG):$(VERSION)

# Infra
k8s_secret: api_key.txt
	 kubectl get secret stockmon-secret 2>/dev/null || \
	 kubectl create secret generic stockmon-secret --from-file=api_key.txt

k8s: k8s_secret

	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/ingress.yaml
	kubectl apply -f k8s/configmap.yaml

update:
	kubectl rollout status deployment stockmon