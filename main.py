import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# Load AFINN lexicon
afinn = {}
with open("AFINN-111.txt", "r") as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        afinn[row[0]] = int(row[1])

# Define emotion thresholds
thresholds = {
    "love": (5, 100), 
    "funny": (3, 4), 
    "amusement": (1, 2), 
    "anger": (-4, -3), 
    "anxiety": (-2, -1), 
    "awkwardness": (-1, 0),
    "boredom": (-2, -1),
    "calmness": (0, 1),
    "confusion": (-1, 0),
    "craving": (2, 3),
    "disgust": (-5, -4),
    "empathic pain": (-5, -4),
    "entrancement": (3, 4),
    "excitement": (4, 5),
    "fear": (-5, -4),
    "horror": (-5, -3),
    "interest": (2, 3),
    "joy": (4, 5),
    "nostalgia": (3, 4),
    "relief": (2, 3),
    "sadness": (-3, -2),
    "satisfaction": (3, 4),
    "surprise": (1, 2)
}

# Define emoji dictionary
emojis = {
    "love": "❤️", 
    "funny": "😂", 
    "amusement": "😊", 
    "anger": "😠", 
    "anxiety": "😰", 
    "awkwardness": "😬",
    "boredom": "😒",
    "calmness": "😌",
    "confusion": "😕",
    "craving": "🍔",
    "disgust": "🤢",
    "empathic pain": "😢",
    "entrancement": "😍",
    "excitement": "🤩",
    "fear": "😱",
    "horror": "👻",
    "interest": "🤔",
    "joy": "😁",
    "nostalgia": "👴",
    "relief": "😌",
    "sadness": "😢",
    "satisfaction": "😌",
    "surprise": "😲"
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    sentiment_score = sum(afinn.get(word, 0) for word in text.split())
    emotion = ''
    for category, threshold in thresholds.items():
        if threshold[0] <= sentiment_score <= threshold[1]:
            emotion = category
            break
    
    if sentiment_score == 0:
        sentiment = 'Neutral 😐'
    elif sentiment_score < 0:
        sentiment = 'Negative 😫'
    else:
        sentiment = 'Positive 😀'
        
    emoji = emojis.get(emotion, '')
    return render_template('result.html', text=text, sentiment=sentiment, emotion=emotion, emoji=emoji)


if __name__ == '__main__':
    app.run(debug=True)
