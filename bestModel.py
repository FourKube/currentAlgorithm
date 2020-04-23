'''
After 200 Iterations, & DF size of 480, test_size=0.20 here are the results:

Average Overall Acuracy: 0.6035915492957742
Average True Positive Acuracy: 0.5960952271404407
Total Stocks: 14200. Number of Stocks Bought: 4352
Overall Profit: $38772.79 (this puts $1000 into every trade)
'''

import pandas as pd
import numpy as np
import datetime
import csv
#Machine Learning Libraries
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.utils.multiclass import unique_labels
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score

'''
This is the actual Random Forest model. It returns the Model 'clf' and the Accuracy,
the predictions 'y_pred', and actual correct answers 'y-test'
'''
def make_RF_model():
    df = pd.read_csv("1.5.csv")
    #Features
    #X = df[['scaleZacks', 'scaleYahoo', 'scaleInvestor', 'Price','Market Cap']].copy()
    #feat_labels = ['scaleZacks', 'scaleYahoo', 'scaleInvestor', 'Price','Market Cap']

    #Just columns with all values there including ranks. No categorical variables
    X = df[["Quarter's Headline Sentiment", "Perf Week"]].copy()
    feat_labels = ["Quarter's Headline Sentiment","Perf Week"]

    stock = df[['Stock Name']]
    theDate = df[["Date"]]
    theReturn = df[["pricediff"]]
    #Labels
    y = np.array(df['results'])
    #Split Datasets to Training and Testing
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=5, shuffle=False)
    #X_train, X_test, y_train, y_test, stock_train, stock_test, theDate_train, theDate_test, theReturn_train,theReturn_test = train_test_split(X, y, stock, theDate, theReturn, test_size=0.20, random_state=5)
    X_train, X_test, y_train, y_test, stock_train, stock_test = train_test_split(X, y, stock, test_size=0.20)
    #make model
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    #Feature importance
    print("")
    print("Feature Importance:")
    for feature in zip(feat_labels, clf.feature_importances_):
        print(feature)
    print("")
    #Make Prediction on Test data
    y_pred=clf.predict(X_test)
    #Accuracy
    theAccuracy = metrics.accuracy_score(y_test, y_pred)
    #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    stock_test_list = stock_test['Stock Name'].tolist()
    return clf, theAccuracy, y_pred, y_test, stock_test_list, df

'''
This calculates a different type of accuracy than the 'theAccuracy' given from the make_RF_model().
This accuracy is to find what percent of the time that the model predicts a 5 (a strong buy), does 
that particular stock go up (a 3, 4, or 5). Therefore this value is a lot higher than the normal accuracy.
'''
def true_positive_accuracy(y_pred, y_test, stock_test_list, df, balance, overallProfit,totalStocks,numStocksBought):
    swung = 0
    struck = 0
    cumulativeReturn = 0
    for i in range(len(y_pred)):
        profitChange = 0
        totalStocks += 1
        #whats our recommendation
        if (y_pred[i] == 1):
            perc = (df[df["Stock Name"]==str(stock_test_list[i])]["pricediff"].iloc[0]/100)
            cumulativeReturn = cumulativeReturn + perc
            balance = balance * (1 + perc)
            numStocksBought +=1 
            recom = 'BUY'
            profitChange = (1000 * (1 + perc)) - 1000
            overallProfit = overallProfit + profitChange
        else:
            recom = '-'
        #print statements
        print("Stock: " + '{0: <5}'.format(str(stock_test_list[i])) + " || Prediction: " + str(y_pred[i]) + 
        " || Actual: " + str(y_test[i]) + 
        " || " + '{0: <10}'.format(str(df[df["Stock Name"]==str(stock_test_list[i])]["Date"].iloc[0])) +
        " || Recommendation: " + '{0: <4}'.format(str(recom)) + " || %-Return: " + 
        '{0: <7}'.format(str(df[df["Stock Name"]==str(stock_test_list[i])]["Change"].iloc[0])) +
        " || Balance: $" + '{0: <9}'.format(str(balance)[:9]) + " || Profit: $" + 
        '{0: <6}'.format(str(profitChange)[:6]) + " || Overall Profit: $" + 
        str(overallProfit)[:8])
        #this is for keeping track of the accuracy
        if(y_pred[i]==1):
            swung += 1
            perc = (df[df["Stock Name"]==str(stock_test_list[i])]["pricediff"].iloc[0]/100)
            if (perc > 0):
                struck += 1
    if (swung == 0):
        print("swung = 0...")
        swingAccuracy = 0
    else:
        swingAccuracy = struck/swung
    cumulativeReturn = cumulativeReturn/numStocksBought
    return swingAccuracy, balance, cumulativeReturn, overallProfit, totalStocks, numStocksBought

def Reverse(lst): 
    return [ele for ele in reversed(lst)] 

# def avgOfAllReturns():
#     df = pd.read_csv("clean_dataset_bins_0_1000.csv")
#     listOfReturns = df["pricediff"].tolist()
#     print(len(listOfReturns))
#     avg = 0
#     balance = 0
#     posCount = 0
#     for i in range(len(listOfReturns)):
#         if (listOfReturns[i] > 0):
#             posCount += 1
#     print("sum")
#     print(sum(listOfReturns))
#     print("final")
#     print(balance)
#     print("Percent")
#     print(posCount/len(listOfReturns))

#     return avg

#print(avgOfAllReturns())

###############################################################################################################
listOfAcc = []
listOfSwingAcc = []

'''
This for loop does calculates the accuracy and true positive accuracy five times each and saves
them to a list.
'''

# #change the data set
# df = pd.read_csv("originalDataset.csv")
# df = addResultColumn(df)
# df.to_csv("clean_dataset_2_bins.csv")



#Run the back test
balance = 1000 #starting balance... each iteration the new balance is thrown in at the start
overallProfit = 0
iterationCount = 1
totalStocks = 0
numStocksBought = 0
for i in range(3): #choose the amount of iterations you want
    clf, theAccuracy, y_pred, y_test, stock_test_list, df = make_RF_model()
    swingAccuracy, balance, cumulativeReturn, overallProfit, totalStocks, numStocksBought = true_positive_accuracy(y_pred,y_test, stock_test_list, df, balance, overallProfit, totalStocks, numStocksBought)
    listOfAcc.append(theAccuracy)
    listOfSwingAcc.append(swingAccuracy)
    print("")
    print("Iteration Count: " + str(iterationCount) + " Complete. " + "Total Stocks: " + 
    str(totalStocks) + ". Number of Stocks Bought: " + str(numStocksBought))
    iterationCount += 1
    print("Length of Dataframe: " + str(len(df)))
    print("")


'''
This part calculates the average after the 5 iterations above
'''
accTotal = 0
swingAccTotal = 0
for i in range(len(listOfSwingAcc)):
    accTotal = accTotal + listOfAcc[i]
    swingAccTotal = swingAccTotal + listOfSwingAcc[i]
avgAcc = accTotal/len(listOfAcc)
avgSwingAcc = swingAccTotal/len(listOfSwingAcc)
print("")
print("List containing each iterations general Accuracy:")
print(listOfAcc)
print("List containing each iterations True Positive Accuracy:")
print(listOfSwingAcc)
print("")
print("Average Overall Acuracy: " + str(avgAcc))
print("Average True Positive Acuracy: " + str(avgSwingAcc))





