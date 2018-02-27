PROJECT = stock_sentiment_analyser
AWS_REGION = eu-west-2
VIRTUAL_ENV = env
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

#SCRAPE FUNCTION
NAIVE_BAYES_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:NaiveBayes
NAIVE_BAYES_FILE_NAME = naive_bayes
NAIVE_BAYES_FUNCTION_HANDLER = lambda_handler

build_naive_bayes: clean_package organise_naive_bayes

refresh_naive_bayes: build_naive_bayes naive_bayes_delete naive_bayes_create

clean_package:
	# Clean the build folder
	sudo rm -rf build

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

naive_bayes_delete:
	aws lambda delete-function \
		--function-name $(NAIVE_BAYES_FUNCTION_NAME)
