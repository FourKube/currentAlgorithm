import pandas as pd
import numpy as np
import datetime
import csv


'''
These variables change the strings of expert rankings to numerical values that can be used
by the predictive models.
'''
scale_mapper_zacks = {'5-StrongSell': 1, 
                '4-Sell': 2,
                '3-Hold': 3,
                '2-Buy': 4,
                '1-StrongBuy': 5}
scale_mapper_yahoo = {'STRONG SELL': 1,
                'SELL': 2, 
                'UNDERPERFORM': 3,
                'HOLD': 4,
                'BUY': 5,
                'STRONG BUY': 6}
scale_mapper_thestreet = {'(Sell)': 1, 
                '(Hold)': 2,
                '(Buy)': 3}
scale_mapper_investor = {'F': 1, 
                'D': 2,
                'C': 3,
                'B': 4,
                'A': 5}


def excludeCoronavirusDates(df):
    df = df[:478]
    return df
'''
This function makes the bins array that chooses 
what bins certain % returns for stocks would fall in
'''
def chooseBins(numBins):
    if (numBins==2):
        bins = [-1000,3, 1000]
    elif (numBins==4):
        bins = [-1000,-3,0,3,1000]
    elif (numBins==6):
        bins = [-1000,-6,-3,0,3,6,1000]
    elif (numBins==8):
        bins = [-1000,-9,-6,-3,0,3,6,9,1000]
    else:
        return False
    return bins

'''
We chose 6 bins which is 'bins = [-1000,-6,-3,0,3,6,1000]'. This means any values from 
-1000 to -6 will be a 0. Any value from -6 to -3 is a 1, any value from -3 to 0 is a 2
etc ... and finally any value from 6 to 1000 is a 5.
'''
bins = chooseBins(2)
labels = np.arange(0, len(bins) - 1)
    
'''
This function drops rows in the dataframe that do not have a value
for either 'Zachs Ranks', 'Yahoo Ranks' or 'Investor Place'. This is so that
the Random Forest Model can run
'''
def dropEmptyData(df):
    df = df.dropna(subset=["Zacks Ranks","Yahoo Ranks","Investor Place"])
    return df

'''
This function uses those global variables above to change the strings of expert rankings 
to numerical values that can be used by the predictive models.
'''
def applyScaling(df): 
    df['Zacks Ranks'] = df['Zacks Ranks'].str.replace(" ","")
    df['scaleZacks'] = df['Zacks Ranks'].replace(scale_mapper_zacks)
    df['scaleYahoo'] = df['Yahoo Ranks'].replace(scale_mapper_yahoo)
    df['scaleInvestor'] = df['Investor Place'].replace(scale_mapper_investor)
    return df



#Convert market cap string (11.52M) to float (1.152e+10)
def suffix(damage):        
    if damage.endswith("B"):
        damage = float(damage[:-1]) * 1000000000
        return damage

    if damage.endswith("K"):
        damage = float(damage[:-1]) * 1000
        return damage

    if damage.endswith("M"):
        damage = float(damage[:-1]) * 1000000
        return damage

    return damage
'''
This function converts market cap values of M (millions) and B (billions),
to their actual values of 1000000 and 1000000000
'''
def convertMarketCap(df):
    for index, row in df.iterrows():
        mc = str(row['Market Cap'])
        mc = suffix(mc)
        outstanding = str(row['Outstanding'])
        outstanding = suffix(outstanding)
        f = str(row['Float'])
        f = suffix(f)
        avg = str(row['Avg Volume'])
        avg = suffix(avg)
        df.at[index, 'Market Cap'] = mc
        df.at[index, 'Outstanding'] = outstanding
        df.at[index, 'Float'] = f
        df.at[index, 'Avg Volume'] = avg
    return df

'''
This function removes extra characters like '%'' and ',' so that the data can be more 
easily used in a predictive model.
'''
def removeExtraCharacters(df):
    df['EPS this Y'] = df['EPS this Y'].str[:-1]
    df['EPS this Y'] = df['EPS this Y'].astype(float)

    df['EPS next Y'] = df['EPS next Y'].str[:-1]
    df['EPS next Y'] = df['EPS next Y'].astype(float)

    df['EPS past 5Y'] = df['EPS past 5Y'].str[:-1]
    df['EPS past 5Y'] = df['EPS past 5Y'].astype(float)

    df['EPS next 5Y'] = df['EPS next 5Y'].str[:-1]
    df['EPS next 5Y'] = df['EPS next 5Y'].astype(float)

    df['Sales past 5Y'] = df['Sales past 5Y'].str[:-1]
    df['Sales past 5Y'] = df['Sales past 5Y'].astype(float)

    df['Divident'] = df['Divident'].str[:-1]
    df['Divident'] = df['Divident'].astype(float)

    df['ROA'] = df['ROA'].str[:-1]
    df['ROA'] = df['ROA'].astype(float)

    df['ROE'] = df['ROE'].str[:-1]
    df['ROE'] = df['ROE'].astype(float)

    df['ROI'] = df['ROI'].str[:-1]
    df['ROI'] = df['ROI'].astype(float)

    df['Gross M'] = df['Gross M'].str[:-1]
    df['Gross M'] = df['Gross M'].astype(float)

    df['Oper M'] = df['Oper M'].str[:-1]
    df['Oper M'] = df['Oper M'].astype(float)

    df['Profit M'] = df['Profit M'].str[:-1]
    df['Profit M'] = df['Profit M'].astype(float)

    df['Insider Own'] = df['Insider Own'].str[:-1]
    df['Insider Own'] = df['Insider Own'].astype(float)

    df['Insider Trans'] = df['Insider Trans'].str[:-1]
    df['Insider Trans'] = df['Insider Trans'].astype(float)

    df['Inst Own'] = df['Inst Own'].str[:-1]
    df['Inst Own'] = df['Inst Own'].astype(float)

    df['Inst Trans'] = df['Inst Trans'].str[:-1]
    df['Inst Trans'] = df['Inst Trans'].astype(float)

    df['Float Short'] = df['Float Short'].str[:-1]
    df['Float Short'] = df['Float Short'].astype(float)

    df['Perf Week'] = df['Perf Week'].str[:-1]
    df['Perf Week'] = df['Perf Week'].astype(float)

    df['Perf Month'] = df['Perf Month'].str[:-1]
    df['Perf Month'] = df['Perf Month'].astype(float)

    df['Perf Quart'] = df['Perf Quart'].str[:-1]
    df['Perf Quart'] = df['Perf Quart'].astype(float)

    df['Perf Half'] = df['Perf Half'].str[:-1]
    df['Perf Half'] = df['Perf Half'].astype(float)

    df['Perf Year'] = df['Perf Year'].str[:-1]
    df['Perf Year'] = df['Perf Year'].astype(float)

    df['Perf YTD'] = df['Perf YTD'].str[:-1]
    df['Perf YTD'] = df['Perf YTD'].astype(float)

    df['Volatility W'] = df['Volatility W'].str[:-1]
    df['Volatility W'] = df['Volatility W'].astype(float)

    df['Volatility M'] = df['Volatility M'].str[:-1]
    df['Volatility M'] = df['Volatility M'].astype(float)

    df['SMA20'] = df['SMA20'].str[:-1]
    df['SMA20'] = df['SMA20'].astype(float)

    df['SMA50'] = df['SMA50'].str[:-1]
    df['SMA50'] = df['SMA50'].astype(float)

    df['SMA200'] = df['SMA200'].str[:-1]
    df['SMA200'] = df['SMA200'].astype(float)
    df
    df['52W High'] = df['52W High'].str[:-1]
    df['52W High'] = df['52W High'].astype(float)

    df['52W Low'] = df['52W Low'].str[:-1]
    df['52W Low'] = df['52W Low'].astype(float)

    df['from Open'] = df['from Open'].str[:-1]
    df['from Open'] = df['from Open'].astype(float)

    df['Gap'] = df['Gap'].str[:-1]
    df['Gap'] = df['Gap'].astype(float)


    df['Price'] = df['Price'].astype(str).str.replace(',', '')
    df['Price'] = df['Price'].astype(float)

    df['Volume'] = df['Volume'].astype(str).str.replace(',', '')
    df['Volume'] = df['Volume'].astype(float)
    return df

'''
This function changes the result column from continous values to discrete ones inside of bins,
the column name is 'result'.
'''
def addResultColumn(df):
    #remove % signs and convert to numerical var (float)
    df['pricediff'] = df['Change'].str[:-1]
    df['pricediff'] = df['pricediff'].astype(float)
    #Convert Purchase (labels) to categories
    df["results"] = pd.cut(df["pricediff"], bins=bins,labels=labels)
    df['results'].unique()

    df.reset_index(drop=True, inplace=True)
    #df = df.drop(['Change', 'pricediff'], axis=1)
    return df



######################################################################################################
df = pd.read_csv("currentTrainingData.csv")
df = convertMarketCap(df)
df = excludeCoronavirusDates(df)
df = removeExtraCharacters(df)
#df = applyScaling(df) 
df = dropEmptyData(df)
df = addResultColumn(df)
print(df)
df.to_csv("3.csv")

######################################################################################################


