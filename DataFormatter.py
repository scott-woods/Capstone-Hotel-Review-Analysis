import time
import pandas as pd
from Functions import cleanText, getPolarity, getSubjectivity, getOverallSentiment


# This Code was used to clean the original Dataset, and it exports the cleaned Data as a
# new CSV file for ease of use in the final application, so it is not in use for the Main Application.
# It includes all Descriptive Methods that were used to clean/organize/select appropriate Data.
# See app.py for actual Entry Point.


def cleanData():
    startTime = time.time()
    print("Reading Import Data...")
    df = pd.read_csv('Hotel_Reviews2.csv', usecols=['reviews.rating', 'reviews.text', 'reviews.title'])
    df = df.dropna()
    df.rename(columns={'reviews.rating': 'Reviewer_Score', 'reviews.text': 'Full_Review',
                       'reviews.title': 'Review_Title'}, inplace=True)

    df['Review_Polarity'] = None
    df['Review_Subjectivity'] = None
    df['Title_Polarity'] = None
    df['Title_Subjectivity'] = None
    df['Overall_Sentiment'] = None

    # Clean all Text
    print("Cleaning Text Data...")
    df['Full_Review'] = df['Full_Review'].apply(lambda x: cleanText(x))
    df['Review_Title'] = df['Review_Title'].apply(lambda x: cleanText(x))

    # Populate Polarity/Subjectivity Columns
    print("Populating Polarity/Subjectivity Columns...")
    df['Review_Polarity'] = df['Full_Review'].apply(lambda x: getPolarity(x))
    df['Review_Subjectivity'] = df['Full_Review'].apply(lambda x: getSubjectivity(x))
    df['Title_Polarity'] = df['Review_Title'].apply(lambda x: getPolarity(x))
    df['Title_Subjectivity'] = df['Review_Title'].apply(lambda x: getSubjectivity(x))

    df['Overall_Sentiment'] = df['Reviewer_Score'].apply(lambda x: getOverallSentiment(x))

    # Delete where Polarity doesn't match score
    df.drop(df[(df['Review_Polarity'] < 0.01) & (df['Reviewer_Score'] >= 4)].index, inplace=True)
    df.drop(df[(df['Review_Polarity'] > -0.01) & (df['Reviewer_Score'] <= 2)].index, inplace=True)
    df.drop(df[(df['Title_Polarity'] < 0.01) & (df['Reviewer_Score'] >= 4)].index, inplace=True)
    df.drop(df[(df['Title_Polarity'] > -0.01) & (df['Reviewer_Score'] <= 2)].index, inplace=True)

    # Export New CSV
    print("Exporting New CSV...")
    df.to_csv('Hotel_Reviews_2_Formatted.csv')

    endTime = time.time()
    print("Processing Time: {}".format(round((endTime - startTime) / 60), 2))
