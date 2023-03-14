import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article, Config
from wordcloud import WordCloud, STOPWORDS


def word_cloud(text):
    stopwords = set(STOPWORDS)
    allWords = ' '.join([nws for nws in text])
    wordCloud = WordCloud(background_color='black', width=1600, height=800, stopwords=stopwords, min_font_size=20,
                          max_font_size=150, colormap='prism').generate(allWords)
    fig, ax = plt.subplots(figsize=(20, 10), facecolor='k')
    plt.imshow(wordCloud)
    ax.axis("off")
    fig.tight_layout(pad=0)
    plt.show()


# word_cloud(news_df['Summary'].values)


def drawPieChart(company_name, positive, neutral, negative):
    labels = ['Positive [' + str(round(positive)) + '%]', 'Neutral [' + str(round(neutral)) + '%]',
              'Negative [' + str(round(negative)) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.style.use('default')
    plt.legend(labels)
    plt.title("Sentiment Analysis Result for stock= " + company_name + "")
    plt.axis('equal')
    plt.show()


# Sentiment Analysis percentage
def percentage(part, whole):
    return 100 * float(part) / float(whole)


def computeSentimentPercentage(sentiment_analyzer):
    positive = 0
    negative = 0
    neutral = 0
    sentiment_list = {}
    for index, analyzer in sentiment_analyzer.iterrows():
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']
        if neg > pos:
            negative += 1  # increasing the count by 1
        elif pos > neg:
            positive += 1  # increasing the count by 1
        elif pos == neg:
            neutral += 1  # increasing the count by 1
    positive = percentage(positive, len(sentiment_analyzer))  # percentage is the function defined above
    neutral = percentage(neutral, len(sentiment_analyzer))
    negative = percentage(negative, len(sentiment_analyzer))
    sentiment_list['positive'] = positive
    sentiment_list['neutral'] = neutral
    sentiment_list['negative'] = negative
    # df = pd.DataFrame.from_dict(sentiment_list)
    # return sentiment_list
    return sentiment_list


def gen_ticker_sentiment(ticker_name, from_last_days=2):
    """generate sentiment analysis of a ticker since from last <from_last_days> date
    default: last 2 days
    """

    now = dt.date.today()
    now = now.strftime('%m-%d-%Y')
    yesterday = dt.date.today() - dt.timedelta(days=from_last_days)
    yesterday = yesterday.strftime('%m-%d-%Y')
    google_news = GoogleNews(start=yesterday, end=now)
    google_news.search(ticker_name)
    result = pd.DataFrame(google_news.result())
    sentiment = []
    analyzer = None
    for news in result['title']:
        analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
        sentiment.append(analyzer)
    sentiment = pd.DataFrame(sentiment)
    sentiResult = pd.concat([result, sentiment], axis=1)
    combinedSentiment = computeSentimentPercentage(sentiment)
    # word_cloud(sentiResult['desc'].values)
    # drawPieChart(ticker_name, sentiResult['pos'], sentiResult['neu'], sentiResult['neg'])
    return sentiResult, combinedSentiment


def getSentimentAnalysis(company_name):
    ### sentiment analysis configuration starts here
    # nltk.download('vader_lexicon') #required for Sentiment Analysis
    pd.set_option("max_columns", None)
    now = dt.date.today()
    now = now.strftime('%m-%d-%Y')
    yesterday = dt.date.today() - dt.timedelta(days=2)
    yesterday = yesterday.strftime('%m-%d-%Y')

    # nltk.download('punkt')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    ### sentiment analysis configuration ends herer

    # As long as the company name is valid, not empty...
    if company_name != '':
        print(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

        # Extract News with Google News
        google_news = GoogleNews(start=yesterday, end=now)
        google_news.search(company_name)
        result = google_news.result()
        # store the results
        df = pd.DataFrame(result)
        # print(df.columns)

    try:
        list = []  # creating an empty list
        for i in df.index:
            article_dict = {}  # creating an empty article_dictionary to append an article in every single iteration
            article = Article(df['link'][i], config=config)  # providing the link
            try:
                article.download()  # downloading the article
                article.parse()  # parsing the article
                article.nlp()  # performing natural language processing (nlp)
            except Exception as error:
                pass
            # storing results in our empty article_dictionary
            article_dict['Date'] = df['date'][i]
            article_dict['Media'] = df['media'][i]
            article_dict['Title'] = article.title
            article_dict['Article'] = article.text
            article_dict['Summary'] = article.summary
            article_dict['Key_words'] = article.keywords
            list.append(article_dict)
        check_empty = not any(list)
        # print(check_empty)
        if not check_empty:
            news_df = pd.DataFrame(list)  # creating dataframe
            # print("news_df", news_df.columns, news_df)
        else:
            news_df = pd.DataFrame()

    except Exception as e:
        # exception handling
        print("exception occurred:" + str(e))
        print(
            'Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.')

    # Sentiment Analysis
    def percentage(part, whole):
        return 100 * float(part) / float(whole)

    # Assigning Initial Values
    positive, negative, neutral = 0, 0, 0
    news_list, neutral_list, negative_list, positive_list = [], [], [], []

    # Iterating over the tweets in the dataframe
    for news in news_df['Summary']:
        news_list.append(news)
        analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']
        news_df['analyze'] = [analyzer]
        if neg > pos:
            negative_list.append(news)
            negative += 1
        elif pos > neg:
            positive_list.append(news)
            positive += 1
        elif pos == neg:
            neutral_list.append(news)
            neutral += 1

    positive = percentage(positive, len(news_df))
    negative = percentage(negative, len(news_df))
    neutral = percentage(neutral, len(news_df))

    # Converting lists to pandas dataframe
    news_list = pd.DataFrame(news_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    # overallSentiment = pd.DataFrame()
    # overallSentiment['news'] = news_list
    # overallSentiment['neutral_list'] = neutral_list
    # overallSentiment['negative_list'] = negative_list
    # overallSentiment['positive_list'] = positive_list

    # news_list['news_list'] = news_list
    # news_list['positive_list'] = positive_list
    # news_list['neutral_list'] = neutral_list
    # news_list['negative_list'] = negative_list

    # using len(length) function for counting
    # print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
    # print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
    # print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')

    # Creating PieCart
    # drawPieChart(company_name, positive, neutral, negative)

    # display word_cloud
    # print('Wordcloud for ' + company_name)
    # word_cloud(news_df['Summary'].values)

    df['positive'] = positive
    df['neutral'] = neutral
    df['negative'] = negative
    # print(type([[news_list, positive_list, neutral_list, negative_list]]))

    return positive

print(getSentimentAnalysis("adani ent"))
