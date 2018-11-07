import re

class Tweet:
    def __init__(self, data):
        self.data = data
    
    def user_link(self):
        return "http://twitter.com/{}".format(self.data["username"])
    
    def filtered_text(self):
        return self.filter_topics(self.filter_urls(self.data['text']))

    def filter_topics(self, text):
        topics = ["football"

        for topic in topics:
            if (topic in text):
                # Mark tag adds highlighting on a work
                text = text.replace(topic, "<mark>{}</mark>".format(topic))
            else:
                continue

        return text

        def filter_urls(self, text):
            # Filters for url elements.  Need to update.
            return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)", r'<a href="\1" target="_blank">\1</a>', text)
