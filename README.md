# Currently Algorithm in production


### Explanation of the 4 files below. Comments inside the files describe what they do

### 1.5csv

This has the cleaned data. Your own version of this can be made by simply running the transformDataset.py function and choosing what you want. 

### originalDataset.csv

This has the original data thats taken from S3. Note that 1.5csv is not only already cleaned but also only contains data prior to Coronavirus affecting the market in late February.

### transformDataset.py

This function takes in originalDataset.csv and cleans, shortens, and creates an extra column that bins the results. Then it spits out a new file.

### bestModel.py

Our current model that is in production. It uses "Quarter's Headline Sentiment" and "Perf Week" as parameters. After 200 iterations it usually averages its accuracy around 60% overall and 60% for true positive accuracy.