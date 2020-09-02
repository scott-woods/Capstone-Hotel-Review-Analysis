from textblob import TextBlob
import string
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


# Cleans String by removing special characters and converting to Lowercase
def cleanText(x):
    x = (x.lower()).translate(str.maketrans('', '', string.punctuation))
    return x


# Returns Polarity value for a String
def getPolarity(x):
    blob = TextBlob(x)
    resultPolarity = blob.sentiment.polarity
    return resultPolarity


# Returns Subjectivity value for a String
def getSubjectivity(x):
    blob = TextBlob(x)
    resultSubjectivity = blob.sentiment.subjectivity
    return resultSubjectivity


# Determine Sentiment based on Rating
def getOverallSentiment(x):
    if x >= 4:
        return 1
    elif x <= 2:
        return -1
    else:
        return 0


# Encodes Non-Numeric Columns
def encodeColumns(df):
    newDf = pd.DataFrame()
    for column in df:
        # If Column is not Numeric
        if df[column].dtype != 'int64' and df[column].dtype != 'float64' and df[column].dtype != 'int32':
            labelEncoder = LabelEncoder()
            # Add new Column with numeric code
            newDf[column + '_Code'] = labelEncoder.fit_transform(df[column])
        else:
            newDf[column] = df[column]
    return newDf


def interpretInput(str):
    cleanText(str)
    strPolarity = getPolarity(str)
    strSubjectivity = getSubjectivity(str)
    return strPolarity, strSubjectivity


def elimNullReview(x):
    if x == 'no positive':
        return ''
    elif x == 'no negative':
        return ''
    else:
        return x


def prepareModel():
    df = pd.read_csv('Hotel_Reviews_2_Formatted.csv')
    # Split into X and Y with Rating as Target
    ratingX = df.filter(['Review_Polarity', 'Review_Subjectivity', 'Title_Polarity', 'Title_Subjectivity'])
    ratingY = df['Reviewer_Score']

    # Split into X and Y with Overall Sentiment as Target
    sentimentX = df.filter(['Review_Polarity', 'Review_Subjectivity', 'Title_Polarity', 'Title_Subjectivity'])
    sentimentY = df['Overall_Sentiment']

    ratingModel = RandomForestRegressor(n_estimators=200,
                                        min_samples_split=5,
                                        min_samples_leaf=2,
                                        max_features='sqrt',
                                        max_depth=10,
                                        bootstrap=True)
    ratingModelFit = ratingModel.fit(ratingX, ratingY)

    sentimentModel = RandomForestClassifier(n_estimators=1200,
                                            min_samples_split=2,
                                            min_samples_leaf=4,
                                            max_features='sqrt',
                                            max_depth=10,
                                            bootstrap=False)
    sentimentModelFit = sentimentModel.fit(sentimentX, sentimentY)
    return ratingModelFit, sentimentModelFit


def makePrediction(review, title, ratingModelFit, sentimentModelFit):
    reviewPol, reviewSub = interpretInput(review)
    titlePol, titleSub = interpretInput(title)
    estRating = round(ratingModelFit.predict([[reviewPol, reviewSub, titlePol, titleSub]])[0], 2)
    estSentiment = sentimentModelFit.predict([[reviewPol, reviewSub, titlePol, titleSub]])[0]
    estSentimentStr = None
    if estSentiment == 1:
        estSentimentStr = 'Positive'
    elif estSentiment == 0:
        estSentimentStr = 'Neutral'
    elif estSentiment == -1:
        estSentimentStr = 'Negative'
    return estRating, estSentimentStr


# Get Mean Absolute Error
def getAccuracy():
    df = pd.read_csv('Hotel_Reviews_2_Formatted.csv')
    x = df.filter(['Review_Polarity', 'Review_Subjectivity', 'Title_Polarity', 'Title_Subjectivity'], axis=1)
    y = df['Reviewer_Score']
    a = df.filter(['Review_Polarity', 'Review_Subjectivity', 'Title_Polarity', 'Title_Subjectivity'], axis=1)
    b = df['Overall_Sentiment']

    # Split into Train and Test Set
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        test_size=0.2)
    a_train, a_test, b_train, b_test = train_test_split(a,
                                                        b,
                                                        test_size=0.2)
    ratingModel = RandomForestRegressor(n_estimators=200,
                                        min_samples_split=5,
                                        min_samples_leaf=2,
                                        max_features='sqrt',
                                        max_depth=10,
                                        bootstrap=True)
    ratingModelFit = ratingModel.fit(x_train, y_train)
    y_preds = ratingModelFit.predict(x_test)
    mae = round(mean_absolute_error(y_test, y_preds), 2)

    sentimentModelFit = RandomForestClassifier().fit(a_train, b_train)
    accuracy = round((sentimentModelFit.score(a_test, b_test) * 100), 2)
    return mae, accuracy
