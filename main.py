from google_play_scraper import Sort, reviews_all
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import streamlit as st

def extract_app_id(link):

    match = re.search(r"id=([a-zA-Z0-9_.]+)", link)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Play Store link")

def get_reviews(app_id, max_reviews=60):

    reviews = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang='en',
        country='us',
        sort=Sort.MOST_RELEVANT
    )
    return reviews[:max_reviews]

def analyze_sentiment(reviews):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for i, review in enumerate(reviews):
        analysis = TextBlob(review['content'])
        sentiment = analysis.sentiment.polarity

        if sentiment > 0:
            sentiment_label = "Positive"
        elif sentiment < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        sentiment_counts[sentiment_label] += 1

        st.write(f"Review {i + 1}: {review['content']}")
        st.write(f"Sentiment: {sentiment_label}\n")

    return sentiment_counts

def plot_sentiment_pie_chart(sentiment_counts):

    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['#4CAF50', '#FF5252', '#FFC107']
    explode = (0.1, 0.1, 0.1)  

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode, shadow=True)
    plt.title('Sentiment Distribution')
    plt.axis('equal')  
    st.pyplot(plt)


if __name__ == "__main__":
    st.title('Google Play App Review Sentiment Analysis')

    app_link = st.text_input("Enter Google Play Store app link:", "https://play.google.com/store/apps/details?id=com.sidesshmore.aquatrace")
    
    if st.button('Analyze Reviews'):
        try:
            app_id = extract_app_id(app_link)
            st.write(f"Extracted App ID: {app_id}")


            reviews = get_reviews(app_id)
            sentiment_counts = analyze_sentiment(reviews)


            plot_sentiment_pie_chart(sentiment_counts)

        except ValueError as e:
            st.error(e)
