import spacy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC


class IntentClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.nlp = spacy.load("en_core_web_sm")  # Load spaCy NLP model
        self.intents = ["greeting", "time_query", "exit", "log_query", "task_query"]

    def preprocess_text(self, text):
        """Lemmatize text and remove stopwords"""
        doc = self.nlp(text.lower())
        return " ".join([token.lemma_ for token in doc if not token.is_stop])

    def train_model(self, dataset):
        """Train SVM intent classifier"""
        texts = [self.preprocess_text(sample["text"]) for sample in dataset]
        labels = [sample["intent"] for sample in dataset]

        # Convert text into feature vectors
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts)

        # Train SVM model
        self.model = SVC(kernel="linear", probability=True)
        self.model.fit(X, labels)

        # Save trained model and vectorizer
        joblib.dump(self.model, "intent_model.pkl")

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.nlp = spacy.load("en_core_web_sm")  # Load spaCy NLP model
        self.intents = ["greeting", "time_query", "exit", "log_query", "task_query"]

    def preprocess_text(self, text):
        """Lemmatize text and remove stopwords"""
        doc = self.nlp(text.lower())
        return " ".join([token.lemma_ for token in doc if not token.is_stop])

    def train_model(self, dataset):
        """Train SVM intent classifier"""
        texts = [self.preprocess_text(sample["text"]) for sample in dataset]
        labels = [sample["intent"] for sample in dataset]

        # Convert text into feature vectors
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts)

        # Train SVM model
        self.model = SVC(kernel="linear", probability=True)
        self.model.fit(X, labels)

        # Save trained model and vectorizer
        joblib.dump(self.model, "intent_model.pkl")
        joblib.dump(self.vectorizer, "vectorizer.pkl")

    def load_model(self):
        """Load trained model and vectorizer"""
        self.model = joblib.load("intent_model.pkl")
        self.vectorizer = joblib.load("vectorizer.pkl")

    def predict_intent(self, text):
        """Predict intent of a given user input"""
        processed_text = self.preprocess_text(text)
        vectorized_text = self.vectorizer.transform([processed_text])
        intent = self.model.predict(vectorized_text)[0]
        return intent
        joblib.dump(self.vectorizer, "vectorizer.pkl")

    def load_model(self):
        """Load trained model and vectorizer"""
        self.model = joblib.load("intent_model.pkl")
        self.vectorizer = joblib.load("vectorizer.pkl")

    def predict_intent(self, text):
        """Predict intent of a given user input"""
        processed_text = self.preprocess_text(text)
        vectorized_text = self.vectorizer.transform([processed_text])
        intent = self.model.predict(vectorized_text)[0]
        return intent


# Train the model
if __name__ == "__main__":
    dataset = [
        {"text": "Hello", "intent": "greeting"},
        {"text": "Hey there!", "intent": "greeting"},
        {"text": "What time is it?", "intent": "time_query"},
        {"text": "Tell me the current time", "intent": "time_query"},
        {"text": "Exit the program", "intent": "exit"},
        {"text": "Quit", "intent": "exit"},
        {"text": "Log this as a note", "intent": "log_query"},
        {"text": "Remember this for later", "intent": "log_query"},
        {"text": "Set a reminder for 6 PM", "intent": "task_query"},
        {"text": "Schedule an event", "intent": "task_query"},
    ]

    classifier = IntentClassifier()
    # classifier.train_model(dataset)
    classifier.load_model()
    print("Intent : ", classifier.predict_intent("set a reminder"))