from django.shortcuts import render, redirect, HttpResponse
from .forms import Sentiment_Typed_Tweet_analyse_form
from .sentiment_analysis_code import sentiment_analysis_code
from .forms import Sentiment_Imported_Tweet_analyse_form
from .tweepy_sentiment import Import_tweet_sentiment
from .models import Tweet
from .utils import get_plot
from wordcloud import WordCloud
import csv
import os
import re
# MatPlotLib
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 12, 8
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

def sentiment_analysis(request):
    return render(request, 'home/sentiment.html')


def sentiment_analysis_type(request):
    if request.method == 'POST':
        form = Sentiment_Typed_Tweet_analyse_form(request.POST)
        analyse = sentiment_analysis_code()
        if form.is_valid():
            tweet = form.cleaned_data['sentiment_typed_tweet']
            sentiment = analyse.get_tweet_sentiment(tweet)
            args = {'tweet': tweet, 'sentiment': sentiment}
            return render(request, 'home/sentiment_type_result.html', args)

    else:
        form = Sentiment_Typed_Tweet_analyse_form()
        return render(request, 'home/sentiment_type.html')


def sentiment_analysis_import(request):
    if request.method == 'POST':
        form = Sentiment_Imported_Tweet_analyse_form(request.POST)
        tweet_text = Import_tweet_sentiment()
        analyse = sentiment_analysis_code()

        if form.is_valid():
            handle = form.cleaned_data['sentiment_imported_tweet']

            if handle[0] == '#':
                list_of_tweets = tweet_text.get_hashtag(handle)
                list_of_tweets_and_sentiments = []
                # Open/create a file to append data to
                i = 0
                while os.path.exists('sentiment/static/dokumen/crawling-hashtag%s.csv' % i):
                    i += 1
                csvFile = open('sentiment/static/dokumen/crawling-hashtag%s.csv' % i, 'w', encoding='utf-8')
                #Use csv writer
                csvWriter = csv.writer(csvFile)
                for i in list_of_tweets:
                    list_of_tweets_and_sentiments.append(
                        (i, analyse.get_tweet_sentiment(i)))
                
                convert = ('\n '.join(map(str, list_of_tweets_and_sentiments)))
                csvWriter.writerow([convert])
                csvWriter = csv.writer(csvFile)
                csvFile.close()
                # print(list_of_tweets)

                # Tweet.objects.create(
				# content 		= request.POST.get('content'),
				# sentiment		= request.POST.get('sentiment'),
			    # )
                #Hitung Rata-rata sentiment
                tweet_positif = [t for t, j in list_of_tweets_and_sentiments if j == 'Positive']
                tweet_netral = [t for t, j in list_of_tweets_and_sentiments if j == 'Neutral']
                tweet_negatif = [t for t, j in list_of_tweets_and_sentiments if j  == 'Negative']

                positif = len(tweet_positif), "({}%)".format(100*len(tweet_positif)/len(list_of_tweets_and_sentiments))
                netral = len(tweet_netral), "({}%)".format(100*len(tweet_netral)/len(list_of_tweets_and_sentiments))
                negatif = len(tweet_negatif), "({}%)".format(100*len(tweet_negatif)/len(list_of_tweets_and_sentiments))
                #graph 
                objects = ['Positive', 'Neutral', 'Negative']
                y_pos = np.arange(len(objects))
                qty = [46, 46, 1]
                plt.bar(y_pos, qty, align='center', alpha=0.5, color=['green', 'blue', 'red'])
                plt.xticks(y_pos, objects)
                plt.ylabel('Average')
                plt.title('Sentiment Classification')
                plt.savefig('sentiment/static/media/barchart.png')

                # Creating a word cloud
                words = ' '.join([t for t, j in list_of_tweets_and_sentiments if j == 'Positive'])
                tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", words).split())
                stop = stopword.remove(tweet_bersih)
                wordCloud = WordCloud(width=700, height=500, background_color="white").generate(stop)
                # plt.imshow(wordCloud)
                # plt.savefig('sentiment/static/media/wordcloud.png')
                wordCloud.to_file("sentiment/static/media/wordcloud.png")

                # Creating a word cloud
                words = ' '.join([t for t, j in list_of_tweets_and_sentiments if j == 'Negative'])
                tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", words).split())
                stop = stopword.remove(tweet_bersih)
                wordCloud = WordCloud(width=700, height=500, background_color="white").generate(stop)
                # plt.imshow(wordCloud)
                # plt.savefig('sentiment/static/media/wordcloud.png')
                wordCloud.to_file("sentiment/static/media/wordcloud2.png")

                args = {
                        'list_of_tweets_and_sentiments': list_of_tweets_and_sentiments, 'handle': handle, 'positif': positif, 'netral': netral, 'negatif': negatif}
                # args = {
                #      'list_of_tweets_and_sentiments': list_of_tweets_and_sentiments, 'handle': handle}
                
                return render(request, 'home/sentiment_import_result_hashtag.html', args)

            list_of_tweets = tweet_text.get_tweets(handle) 
            list_of_tweets_and_sentiments = []
            # Open/create a file to append data to
            i = 0
            while os.path.exists('sentiment/static/dokumen/crawling-handle%s.csv' % i):
                i += 1
            csvFile = open('sentiment/static/dokumen/crawling-handle%s.csv' % i, 'w', encoding='utf-8')
            #Use csv writer
            csvWriter = csv.writer(csvFile)
            if handle[0] != '@':
                handle = str('@'+handle)
            for i in list_of_tweets:
                list_of_tweets_and_sentiments.append(
                    (i, analyse.get_tweet_sentiment(i)))
            convert = ('\n '.join(map(str, list_of_tweets_and_sentiments)))
            csvWriter.writerow([convert])
            csvWriter = csv.writer(csvFile)
            csvFile.close()
            # Graph
            objects = ['Positive', 'Neutral', 'Negative']
            y_pos = np.arange(len(objects))
            qty = [20, 2, 5]
            plt.bar(y_pos, qty, align='center', alpha=0.5, color=['green', 'blue', 'red'])
            plt.xticks(y_pos, objects)
            plt.ylabel('Average')
            plt.title('Sentiment Classification')
            plt.savefig('sentiment/static/media/barchart_handle.png')
            #Hitung Rata-rata sentiment
            tweet_positif = [t  for t, j in list_of_tweets_and_sentiments if j == 'Positive']
            tweet_netral = [t for t, j in list_of_tweets_and_sentiments if j == 'Neutral']
            tweet_negatif = [t for t, j in list_of_tweets_and_sentiments if j  == 'Negative']


            positif = len(tweet_positif), "({}%)".format(100*len(tweet_positif)/len(list_of_tweets_and_sentiments))
            netral = len(tweet_netral), "({}%)".format(100*len(tweet_netral)/len(list_of_tweets_and_sentiments))
            negatif = len(tweet_negatif), "({}%)".format(100*len(tweet_negatif)/len(list_of_tweets_and_sentiments))
           
            # Creating a word cloud
            words = ' '.join([t for t, j in list_of_tweets_and_sentiments if j == 'Positive'])
            tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", words).split())
            stop = stopword.remove(tweet_bersih)
            wordCloud = WordCloud(width=700, height=500, background_color="white").generate(stop)
            # plt.imshow(wordCloud)
            # plt.savefig('sentiment/static/media/wordcloud.png')
            wordCloud.to_file("sentiment/static/media/wordcloud_handle.png")

            # Creating a word cloud
            words = ' '.join([t for t, j in list_of_tweets_and_sentiments if j == 'Negative'])
            tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", words).split())
            stop = stopword.remove(tweet_bersih)
            wordCloud = WordCloud(width=700, height=500, background_color="white").generate(stop)
            # plt.imshow(wordCloud)
            # plt.savefig('sentiment/static/media/wordcloud.png')
            wordCloud.to_file("sentiment/static/media/wordcloud_handle2.png")

            args = {
                    'list_of_tweets_and_sentiments': list_of_tweets_and_sentiments, 'handle': handle, 'positif': positif, 'netral': netral, 'negatif': negatif}
            # args = {
            #         'list_of_tweets_and_sentiments': list_of_tweets_and_sentiments, 'handle': handle}
    
            return render(request, 'home/sentiment_import_result.html', args)
    

    else:
        form = Sentiment_Imported_Tweet_analyse_form()
        return render(request, 'home/sentiment_import.html')



