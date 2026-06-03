AWS_ACCOUNT_ID := $(shell aws sts get-caller-identity --query Account --output text)
ECR_REGION := us-east-1
ECR_REPOSITORY_NAME := betr-eats


install:
	uv build
	uv pip install -e .

build:
	docker buildx build --platform linux/amd64 -t $(AWS_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com/$(ECR_REPOSITORY_NAME):latest .

create:
	aws ecr create-repository --repository-name $(ECR_REPOSITORY_NAME) --region $(ECR_REGION)

auth:
	aws ecr get-login-password --region $(ECR_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com

create_repo: auth create

local_run: 
	docker run --env-file .env --rm -it -p 8501:8501 \
		$(AWS_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com/$(ECR_REPOSITORY_NAME):latest

push:
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(ECR_REGION).amazonaws.com/$(ECR_REPOSITORY_NAME):latest


build_and_push: build auth push