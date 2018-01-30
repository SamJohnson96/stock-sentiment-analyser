PROJECT = stock_sentiment_analyser
VIRTUAL_ENV = env
AWS_REGION = eu-west-2
LAMBDA_ROLE = arn:aws:iam::329627156298:role/service-role/lambda_basic

#PREPROCESS FUNCTION
PREPROCESS_FUNCTION_NAME = arn:aws:lambda:eu-west-2:329627156298:function:Bag_Of_Words
PREPROCESS_FILE_NAME = bag_of_words
PREPROCESS_FUNCTION_HANDLER = lambda_handler

# Default commands
install: virtual

build_bow: clean_package build_package_tmp copy_python remove_unused change_nltk_settings zip

preprocess_refresh: build_preprocess preprocess_delete preprocess_create

#If the machine doesn't have Virtual Environment, download it.
virtual:
	@echo "--> Setup and activate virtualenv"
	if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv $(VIRTUAL_ENV); \
	fi
	@echo ""

# Remove everything in the package file
clean_package:
	sudo rm -rf ./package/*/**
	sudo rm -rf ./package/source.zip

# Create tmp folder
build_package_tmp:
	mkdir -p ./package/tmp/lib
	cp -a ./$(PROJECT)/. ./package/tmp/

# Copy python library
copy_python:
	if test ! -d "$(VIRTUAL_ENV)"; then \
		cp -a $(VIRTUAL_ENV)/lib/python2.7/site-packages/. ./package/tmp/; \
	fi

# Removed unused python tools that take up memory
remove_unused:
	rm -rf ./packages/tmp/wheel*
	rm -rf ./packages/tmp/easy-install*
	rm -rf ./packages/tmp/setuptools*

# Run script to change location where we look for nltk in the lambda
change_nltk_settings:
	sudo python ./$(PROJECT)/helpers/nltk_settings_changer.py

# Zip it up
zip:
	cd ./package/tmp && zip -r ../$(PROJECT).zip .

bag_of_words_create:
	aws lambda create-function \
		--region $(AWS_REGION) \
		--role arn:aws:iam::329627156298:role/service-role/lambda_basic \
		--function-name $(PREPROCESS_FUNCTION_NAME) \
		--zip-file fileb://./package/$(PROJECT).zip \
		--handler $(PREPROCESS_FILE_NAME).$(PREPROCESS_FUNCTION_HANDLER) \
		--runtime python2.7 \
		--timeout 15 \
		--memory-size 128


# METHODS
bag_of_words_delete:
	aws lambda delete-function \
		--function-name $(PREPROCESS_FUNCTION_NAME)
