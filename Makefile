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

# K NEAREST FUNCTION
K_NEAREST_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:K_Nearest
K_NEAREST_FILE_NAME = k_nearest_neighbors
K_NEAREST_HANDLER = lambda_handler

# EXTRA TREES
EXTRA_TREES_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:ExtraTrees
EXTRA_TREES_FILE_NAME = extra_trees_classifier
EXTRA_TREES_HANDLER = lambda_handler

# EXTRA TREES
LINEAR_PERCEPTRON_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:Linear_Perceptron
LINEAR_PERCEPTRON_FILE_NAME = linear_perceptron
LINEAR_PERCEPTRON_HANDLER = lambda_handler


# BUILD AND CREATE PACKAGES
build_naive_bayes: clean_package organise_naive_bayes

build_support_vector_machine: clean_package organise_support_vector_machine

build_k_nearest: clean_package organise_k_nearest_neighbors

build_extra_trees: clean_package organise_extra_trees

build_linear_perceptron: clean_package organise_linear_perceptron

# BUILD - DELETE - CREATE
refresh_naive_bayes: build_naive_bayes naive_bayes_delete naive_bayes_create

refresh_support_vector_machine: build_support_vector_machine support_vector_machine_delete support_vector_machine_create

refresh_k_nearest: build_k_nearest k_nearest_delete k_nearest_create

refresh_extra_trees: build_extra_trees extra_trees_delete extra_trees_create

refresh_linear_perceptron: build_linear_perceptron linear_perceptron_delete linear_perceptron_create

refresh_all: refresh_naive_bayes refresh_support_vector_machine refresh_k_nearest refresh_extra_trees refresh_linear_perceptron

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
	cd build/site-packages; zip -g -r ../support_vector_machine.zip . -x "*__pycache__*"

organise_k_nearest_neighbors:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_sentiment_analyser/k_nearest_neighbors.py build/site-packages

	# Create virtual environment in build/support_vector_machine
	virtualenv -p /usr/bin/python3.4 build/k_nearest_neighbors

	# Activate the virtual environment
	. build/k_nearest_neighbors/bin/activate; \

	# Install dependencies in virtual environment
	sudo python3 -m pip install -U requests -t build/site-packages/
	sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../k_nearest_neighbors.zip . -x "*__pycache__*"

organise_extra_trees:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_sentiment_analyser/extra_trees_classifier.py build/site-packages

	# Create virtual environment in build/support_vector_machine
	virtualenv -p /usr/bin/python3.4 build/extra_trees

	# Activate the virtual environment
	. build/extra_trees/bin/activate; \

	# Install dependencies in virtual environment
	sudo python3 -m pip install -U requests -t build/site-packages/
	sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../extra_trees_classifier.zip . -x "*__pycache__*"

organise_linear_perceptron:
	# Make site-packages
	mkdir -p build/site-packages

	# Move
	cp stock_sentiment_analyser/linear_perceptron.py build/site-packages

	# Create virtual environment in build/support_vector_machine
	virtualenv -p /usr/bin/python3.4 build/linear_perceptron

	# Activate the virtual environment
	. build/linear_perceptron/bin/activate; \

	# Install dependencies in virtual environment
	sudo python3 -m pip install -U requests -t build/site-packages/
	sudo python3 -m pip install -U boto3 -t build/site-packages/

  # Move to build/site-packages
	cd build/site-packages; zip -g -r ../linear_perceptron.zip . -x "*__pycache__*"

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
		--zip-file fileb://./build/support_vector_machine.zip \
		--handler $(SUPPORT_VECTOR_MACHINE_FILE_NAME).$(SUPPORT_VECTOR_MACHINE_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

k_nearest_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(K_NEAREST_FUNCTION_NAME) \
		--zip-file fileb://./build/k_nearest_neighbors.zip \
		--handler $(K_NEAREST_FILE_NAME).$(K_NEAREST_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

extra_trees_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(EXTRA_TREES_FUNCTION_NAME) \
		--zip-file fileb://./build/extra_trees_classifier.zip \
		--handler $(EXTRA_TREES_FILE_NAME).$(EXTRA_TREES_HANDLER) \
		--runtime python3.6 \
		--timeout 15 \
		--memory-size 128

linear_perceptron_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role $(LAMBDA_ROLE) \
		--function-name $(LINEAR_PERCEPTRON_FUNCTION_NAME) \
		--zip-file fileb://./build/linear_perceptron.zip \
		--handler $(LINEAR_PERCEPTRON_FILE_NAME).$(LINEAR_PERCEPTRON_HANDLER) \
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

k_nearest_delete:
	aws lambda delete-function \
		--function-name $(K_NEAREST_FUNCTION_NAME)

extra_trees_delete:
	aws lambda delete-function \
		--function-name $(EXTRA_TREES_FUNCTION_NAME)

linear_perceptron_delete:
	aws lambda delete-function \
		--function-name $(LINEAR_PERCEPTRON_FUNCTION_NAME)
