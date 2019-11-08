
.PHONY: clean data lint requirements sync_to_s3 sync_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = sagemaker-byo-mnist
PYTHON_INTERPRETER = python3

# name that docker will use for creating the image which will also be uploaded to AWS ECR
DOCKER_IMAGE_NAME = $(PROJECT_NAME)
DOCKER_IMAGE_NAME_IS_VALID := $(shell [[ $(DOCKER_IMAGE_NAME) =~ ^[a-zA-Z0-9](-*[a-zA-Z0-9])*$$ ]] && echo TRUE || echo FALSE)
DOCKER_IMAGE_EXISTS := $(shell docker images -q $(DOCKER_IMAGE_NAME))

# S3 buckets
S3_BUCKET = sagemaker-us-east-2-117588387775
S3_BUCKET_PREFIX = arn:aws:s3:::$(S3_BUCKET)

# IAM Role with sagemaker permissions
IAM_ROLE = arn:aws:iam::117588387775:role/service-role/AmazonSageMaker-ExecutionRole-20190513T204887

# AWS profile
PROFILE = default

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
# If conda is not installing pip packages into your actual conda env...
# Try running 'path/to/condaenv/bin/pip install -r requirements.txt' manually.  
# It seems it'll work fine after that.
# Make sure 'which pip' is returning the conda path, not your system path
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	# install application dependencies
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt	
	# install project dependencies
	$(PYTHON_INTERPRETER) -m pip install -r container/requirements.txt	

## Make Dataset
data: container/data/external/train.csv container/data/external/test.csv

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Upload Data to S3
sync_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync container/data/ s3://$(S3_BUCKET)/data/
else
	aws s3 sync container/data/ s3://$(S3_BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(S3_BUCKET)/data/ container/data/
else
	aws s3 sync s3://$(S3_BUCKET)/data/ container/data/ --profile $(PROFILE)
endif

## Set up python interpreter environment
environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3 pip
else
	conda create --name $(PROJECT_NAME) python=2.7 pip
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

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

features: container/data/external/train.csv container/data/external/test.csv requirements
	cd container; $(PYTHON_INTERPRETER) src/features/build_features.py

train: container/data/processed/X_train.npy container/data/processed/y_train.npy requirements
	cd container; $(PYTHON_INTERPRETER) src/models/build_model.py

predict: container/output/models/model.h5 container/data/external/test.csv requirements
	cd container; $(PYTHON_INTERPRETER) src/models/predict_model.py data/test/mnist_sample.csv

submit: ~/.kaggle/kaggle.json container/data/processed/submission.csv
	kaggle competitions submit digit-recognizer -f container/output/submission.csv -m "Automated submission"
	echo "All submissions:"
	kaggle competitions submissions digit-recognizer

grade: container/data/processed/submission.csv
	$(PYTHON_INTERPRETER) test/test_project.py

~/.kaggle/kaggle.json:
	@echo "Configuration error.  Please review the Kaggle setup instructions at https://github.com/Kaggle/kaggle-api#api-credentials"; exit 1;

container/data/external/train.csv: ~/.kaggle/kaggle.json
	kaggle competitions download -c digit-recognizer -f train.csv -p container/data/external --force

container/data/external/test.csv: ~/.kaggle/kaggle.json
	kaggle competitions download -c digit-recognizer -f test.csv -p container/data/external --force

container/output/models/model.h5: train

container/data/processed/submission.csv: predict

container/data/processed/X_train.npy: features

container/data/processed/X_test.npy: features

container/data/processed/y_train.npy: features

container/data/processed/y_test.npy: features

#################################################################################
# DEPLOYMENT COMMANDS                                                           #
#################################################################################

build_and_push:
	bash scripts/build_and_push.sh $(DOCKER_IMAGE_NAME)

train_local: 
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
	cd container; local_test/predict_local.sh data/test/mnist_sample.csv

deploy_endpoint:
	$(PYTHON_INTERPRETER) scripts/deploy_endpoint.py $(DOCKER_IMAGE_NAME) $(S3_BUCKET_PREFIX) $(IAM_ROLE)

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
