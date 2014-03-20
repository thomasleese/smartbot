import collections
import math

from textblob import TextBlob


class Statistics():
    """
    This class is based on Donald Knuth"s "The Art of Computer Programming, Volume 2:
    Seminumerical Algorithms" section 4.2.2, of which a summary can be seen on
    http://mathcentral.uregina.ca/QQ/database/QQ.09.02/carlos1.html
    It uses a recurrence relation, so that the time and space complexity
    is O(1), compared to O(n) of a naive approach by storing the full dataset.
    """

    def __init__(self):
        self.n = 0
        self.M = None
        self.S = None

    def add(self, value):
        self.n += 1
        if self.n <= 1:
            self.M, self.S = value, 0.0
        else:
            m = self.M + (value - self.M) / self.n
            s = self.S + (value - self.M) * (value - m)
            self.M, self.S = m, s

    @property
    def mean(self):
        return self.M

    @property
    def pvariance(self):
        return self.S / self.n if self.n > 0 else 0

    @property
    def pstdev(self):
        return math.sqrt(self.pvariance)

    @property
    def variance(self):
        return self.S / (self.n - 1) if self.n > 1 else 0

    @property
    def stdev(self):
        return math.sqrt(self.variance)


class Plugin:
    stats_string = "{}:    Polarity: {p: f},   Subjectivity: {s: f}"

    def sentiments(self, bot):
        return bot.storage.setdefault("sentiments", collections.defaultdict(dict))

    def on_message(self, bot, msg, reply):
        message_sentiment = TextBlob(msg["message"]).sentiment

        polarity = message_sentiment.polarity
        subjectivity = message_sentiment.subjectivity
        if not polarity and not subjectivity:
            return

        sender_sentiments = self.sentiments(bot)[msg["sender"]]
        sender_sentiments.setdefault('polarity', Statistics()).add(polarity)
        sender_sentiments.setdefault('subjectivity', Statistics()).add(subjectivity)

        bot.storage.commit()

    def on_command(self, bot, msg, stdin, stdout, reply):
        if len(msg["args"]) >= 2:
            user_list = " ".join(msg["args"][1:])
        else:
            user_list = stdin.read().strip()

        if not user_list:
            print(self.on_help(), file=stdout)
            return

        for user in user_list.split():
            if user not in self.sentiments(bot):
                print("'{user}' is unknown or has not said anything useful yet".format(user=user), file=stdout)
                continue

            user_sentiments = self.sentiments(bot)[user]
            polarity = user_sentiments["polarity"]
            subjectivity = user_sentiments["subjectivity"]

            print("Sentiments of {user}".format(user=user), file=stdout)
            print(self.stats_string.format("μ", p=polarity.mean, s=subjectivity.mean), file=stdout)
            print(self.stats_string.format("σ", p=polarity.stdev, s=subjectivity.stdev), file=stdout)

    def on_help(self):
        return "Usage: sentiments <user> [<user>...]"
