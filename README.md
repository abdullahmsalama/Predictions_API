# Predictions API

## Introduction

In this Readme file, I will explain the structure of the codes and the part each component plays in the API. The python code I created is also commented.

## Context

The marketing department of a mobility company (also operates in ride-hailing and ride sharing) is doing a lot of campaigns, and they would like to know beforehand if the user segment that they are targeting is relevant for specific campaigns. One of the core information they need is the estimated
customer-life-time-value of a passenger. Given that we know the activity of a passenger within the first week of signing
up, we would like to know how, much money will they spend on trips within one month from registration.

## Data

The data columns will be explained in the following lines:

passenger_activity_after_registration (stored in database.sqlite):

- *passenger_id*: a unique id of each passenger
- *recency_7* (1-7): high value means passenger did their last tour 7 days after registration
- *frequency_7*: number of tours done within 7 days after registration
- *monetary_value_7*: total money spent on tours within 7 days
- *frequency_30*: number of tours done within 30 days
- *monetary_value_30*: total money spent on tours within 30 days

## Files Structure

The files are saved into 3 locations, app folder, the test folder, and the root folder. 

- app
This folder contains api.py and db.py.
  - api.py
  api.py is concerned with configuring the API endpoints, its configurations and the structure of the requests and responses.
  - db.py
  db.py is concerned with defining the database connection. It included also functions to create the prediction table, insert the new prediction fetched from the model to the prediction table, and query the number of occurences of a certain passenger id in the passenger table

- test
This folder contains conftest.py and test_api.py
  - conftest.py
  Shared resources for tests
  - test_api.py
  This python file contains test to be performed to ensure that the API is working correctly

- root folder
  - database.sqlite
  The sqlite database
  - docker-compose.yml
  Contains the definitions for different services needed to run the API.
  - Dockerfile
  The dockerfile containing command to define the image, resources that will be needed during the run of the API such as the trained model.
  - fitted_scaler.pkl
  A scaler file that contains the scaler attributes used to noramlize features during training time. To be used to normalize new data before inserting it to the model.
  - freenow_training.ipynb
  A Jupyter notebook containing all steps including preprocessing, analysis, training and saving the model. The jupyter notebook steps are explained in markdown cells.
  - Makefile
  This docker Makefile are used to compile parts of the code such as train for training the model, tests for testing the API, setup for setting up the dependencies and run for running the API. You can also find the part for training the model and to invoke the jupyter file inside.
  - poetry.*
  For installing the dependencies
  - trained_model.pkl
  The trained model (pickled)

## How to run

1- Run `make setup` to initialize the envoirment and install dependencies.

2- Run `make train` to invoke the jupyter notebook and train then save the ML model.

3- Run `make run` to run the API. while the API is running, you can do one of two requests:
3.1- "POST" resquest, through Postman or curl, for ex.:`curl -X POST -v -d '{"id": 1112, "recency_7": 1, "frequency_7": 4, "monetary_7": 4.5}' http://0.0.0.0:8080/api/predict`
3.2- "GET" request, through curl, or using the URL given through the browser, for ex. http://0.0.0.0:8080/api/requests/1112. This will retreive the number of times the passenger_id 1112 occured in the database table. Also get_health can be invoked via a "GET" request through curl or through the browser, for ex. http://0.0.0.0:8080/health. If the message dispalyed is "API is healthy", then the API is healthy.

4- Run `make test` to test the API.

## Closure

Thank you for visiting the repo. I tested the API and "make train" trains the model sucessfully, "make run" runs the API sucessfully and the post requests inserts sucessfully to the table in teh database, and the get requests retreives the number of occurences for a certain passenger_id sucessfully. "make test" invokes the tests and the tests passed sucesfully. In case you find any bug or you ran into any problem or you want to suggest an improvement, please send me or create an issue!. Thanks :D
