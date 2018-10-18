"""
text to be summarized is sent to this API in the json format:
{
  title: meeting_title,
  date:  date_of_meeting,
  text:  long_string_of_text_to_be_summarized
}

this API should return a json format of:
{
  title:           meeting_title,
  date:            date_of_meeting,
  og_text:         long_string_of_text_to_be_summarized
  short_text:      less_long_string_of_summarized_text
  keywords:        [list_of_keywords_from_text]
  sentiment_score : mean_sentiment_score_from_keywords
}
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def summarize(text):
    """
        Returns summary and keywords from text provided

        short_text: string
        keywords_from_text: list (of strings)
    """
    # imports - move to the top
    from gensim.summarization import keywords
    from gensim.summarization import summarize

    short_text = summarize(text)
    keywords_from_text = keywords(text).split('\n')

    return short_text, keywords_from_text


def meeting_sentiment(keywords):
    """
        Returns overall sentiment from the keywords_from_text
    """
    sentiment_score = '0'  # for now
    # This needs to be explained by Tshepo
    # my thinking:
    # mean of the sentiment of keywords_from_text to provide overall setiment of meeting
    return sentiment_score


class summarize_meeting(Resource):
    def post(self):
        # step 1: get the posted data
        postedData = request.get_json()

        # step 2: read the data
        title = postedData['title']
        date = postedData['date']
        og_text = postedData['text']

        # summarize and analize sentiment
        short_text, keywords_from_text = summarize(og_text)
        sentiment_score = meeting_sentiment(keywords_from_text)

        # prepare json to be returned
        return_json = {
            "title":           title,
            "date":            date,
            "og_text":         og_text,
            "short_text":      short_text,
            "keywords":        keywords_from_text,
            "sentiment_score": sentiment_score
        }

        return jsonify(return_json)


api.add_resource(summarize_meeting, '/summarizetxt')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
