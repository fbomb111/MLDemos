
.PHONY: clean lint git

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = sagemaker-byo-iris
PYTHON_INTERPRETER = python3

# name that docker will use for creating the image which will also be uploaded to AWS ECR
DOCKER_IMAGE_NAME = $(PROJECT_NAME)
DOCKER_IMAGE_NAME_IS_VALID := $(shell [[ $(DOCKER_IMAGE_NAME) =~ ^[a-zA-Z0-9](-*[a-zA-Z0-9])*$$ ]] && echo TRUE || echo FALSE)
DOCKER_IMAGE_EXISTS := $(shell docker images -q $(DOCKER_IMAGE_NAME))

# S3 bucket prefix
S3_BUCKET_PREFIX = arn:aws:s3:::sagemaker-us-east-2-117588387775

# IAM Role with sagemaker permissions
IAM_ROLE = arn:aws:iam::117588387775:role/service-role/AmazonSageMaker-ExecutionRole-20190513T204887

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: src/data/external/train.csv src/data/external/test.csv

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
	@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Setup git
git:
	@bash 'git_config.sh'

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

predict: models/model.h5 requirements
	$(PYTHON_INTERPRETER) src/models/predict_model.py

submit: ~/.kaggle/kaggle.json src/data/processed/submission.csv
	kaggle competitions submit digit-recognizer -f src/data/processed/submission.csv -m "Automated submission"
	echo "All submissions:"
	kaggle competitions submissions digit-recognizer

grade: src/data/processed/submission.csv
	$(PYTHON_INTERPRETER) test/test_project.py

~/.kaggle/kaggle.json:
	@echo "Configuration error.  Please review the Kaggle setup instructions at https://github.com/Kaggle/kaggle-api#api-credentials"; exit 1;

models/model.h5: train

src/data/processed/submission.csv: predict

#################################################################################
# DEPLOYMENT COMMANDS                                                           #
#################################################################################

train_local: requirements	
ifeq ($(DOCKER_IMAGE_NAME_IS_VALID),)
	@echo "Image name * $(DOCKER_IMAGE_NAME) * failed to satisfy constraint: Member must satisfy regular expression pattern: ^[a-zA-Z0-9](-*[a-zA-Z0-9])*"
else ifeq ($(DOCKER_IMAGE_EXISTS),)
	@echo "Image name * $(DOCKER_IMAGE_NAME) * not found.  Run 'make build_and_push' to create the image and push to ECR"
else
	cd container; local_test/train_local.sh $(DOCKER_IMAGE_NAME)
endif

serve_local:
	cd container; local_test/serve_local.sh $(DOCKER_IMAGE_NAME)

predict_local:
	cd container; local_test/predict.sh local_test/iris_sample.csv

build_and_push:
	cd container; bash build_and_push.sh $(DOCKER_IMAGE_NAME)

deploy_endpoint:
	cd container; $(PYTHON_INTERPRETER) deploy_endpoint.py $(DOCKER_IMAGE_NAME) $(S3_BUCKET_PREFIX) $(IAM_ROLE)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
