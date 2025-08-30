import pandas as pd

def preprocess(df,region_df):

    # Filtering data 
    df = df[df['Season']=='Summer']
    
    # merging both df on NOc
    df = df.merge(region_df,on="NOC",how="left")

    #Dropping duplicates
    df.drop_duplicates(inplace=True)
    
    # one hot encoding for gold , silver , medail
    df = pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)

    return df