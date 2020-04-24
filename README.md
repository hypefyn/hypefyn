# hypefyn
Have you thought about the effect of social media hype on financial information? We have.
1. The package is a made of a sentiment classifier for tweets and a computation for hype score. The folders contain the following:
- /data: contains the training data for the sentiment model, and the predictions of the same.
- /nlp: contains code for the ML model
- /get_data: contains code for getting the tweets and stock data via API
- /website: contains the interactive code for the website

2. To install the necessary libraries, run on the command line \
	pip install -r requirements.txt

3. To run the code instead, you would need to have access to the cloud database where the tweets are. However, the folder contains already the data from a precious run. To see the website instead, you need to run on the command line \
	python -m http.server 8000 \
then open on a browser localhost:8000/ and click on hypefyn.html
