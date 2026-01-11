from enum import Enum

class DocType(str, Enum):
    ARTICLE = "ARTICLE"
    JOURNAL = "JOURNAL"
    BOOK = "BOOK"
    OTHER = "OTHER"

class Sentiment(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"