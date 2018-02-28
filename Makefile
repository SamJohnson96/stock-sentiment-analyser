PROJECT = stock_sentiment_analyser
AWS_REGION = eu-west-2
VIRTUAL_ENV = env
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

# NAIVE BAYES FUNCTION
NAIVE_BAYES_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:NaiveBayes
NAIVE_BAYES_FILE_NAME = naive_bayes
NAIVE_BAYES_FUNCTION_HANDLER = lambda_handler

# SUPPORT VECTOR MACHINE FUNCTION
SUPPORT_VECTOR_MACHINE_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:SupportVectorMachine
SUPPORT_VECTOR_MACHINE_FILE_NAME = support_vector_machine
SUPPORT_VECTOR_MACHINE_HANDLER = lambda_handler

# BUILD AND CREATE PACKAGES
build_naive_bayes: clean_package organise_naive_bayes

build_support_vector_machine: clean_package organise_support_vector_machine


# BUILD - DELETE - CREATE
refresh_naive_bayes: build_naive_bayes naive_bayes_delete naive_bayes_create

refresh_support_vector_machine: build_support_vector_machine support_vector_machine_delete support_vector_machine_create

# CLEAN BUILD
clean_package:
	# Clean the build folder
	sudo rm -rf build


# DOWNLOAD ALL PACKAGES AND FILES NEEDED FOR DEPLOYMENT FOR METHODS
organise_naive_bayes:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_sentiment_analyser/naive_bayes.py build/site-packages

	# Create virtual environment in build/scrape
	virtualenv -p /usr/bin/python3.4 build/naive_bayes

	# Install dependencies in virtual environment
	sudo python3 -m pip install -U requests -t build/site-packages/
	sudo python3 -m pip install -U boto3 -t build/site-packages/

	# Activate the virtual environment
	. build/naive_bayes/bin/activate; \

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../naive_bayes.zip . -x "*__pycache__*"

organise_support_vector_machine:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_sentiment_analyser/support_vector_machine.py build/site-packages

	# Create virtual environment in build/support_vector_machine
	virtualenv -p /usr/bin/python3.4 build/support_vector_machine

	# Activate the virtual environment
	. build/support_vector_machine/bin/activate; \

	# Install dependencies in virtual environment
	sudo python3 -m pip install -U requests -t build/site-packages/
	sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../naive_bayes.zip . -x "*__pycache__*"


# CREATION AWS CLI CALLS FOR EVERY METHOD.
naive_bayes_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(NAIVE_BAYES_FUNCTION_NAME) \
		--zip-file fileb://./build/naive_bayes.zip \
		--handler $(NAIVE_BAYES_FILE_NAME).$(NAIVE_BAYES_FUNCTION_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

support_vector_machine_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(SUPPORT_VECTOR_MACHINE_FUNCTION_NAME) \
		--zip-file fileb://./build/naive_bayes.zip \
		--handler $(SUPPORT_VECTOR_MACHINE_FILE_NAME).$(SUPPORT_VECTOR_MACHINE_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

# DELETION AWS CLI CALLS FOR EVERY METHOD
naive_bayes_delete:
	aws lambda delete-function \
		--function-name $(NAIVE_BAYES_FUNCTION_NAME)

support_vector_machine_delete:
	aws lambda delete-function \
		--function-name $(SUPPORT_VECTOR_MACHINE_FUNCTION_NAME)
