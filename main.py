from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, send
import subprocess
from time import sleep
import io
import string
import random 
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer 
import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense, Dropout
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
error = {"error": ["Could you repeat that please?", "Ummm?", "Pardon?", "wut"],
}
data = {"intents": [
             {"tag": "greeting",
              "patterns": ["hello", "hi there", "hi"],
              "responses": ["hi there", "hello", "greetings!"],
             },
             {"tag": "smalltalk",
              "patterns": [ "great thanks for asking", "dunno", "idk", "Im going to ", "Im going to go "],
              "responses": [ "What are you going to do this week?", "well have a good time"]
             },
             {"tag": "how are you",
              "patterns": [ "how are you"],
              "responses": ["good you?"]
             },
             {"tag": "how",
              "patterns": ["good Thanks for asking." ],
              "responses": ["no problem"]
             },
             {"tag": "age",
              "patterns": ["how old are you?", "when is your birthday?", "when was you born?"],
              "responses": ["I am 1 years old", "I was born in 2021", "My birthday is  and I was born in 2021", ""] 
             },
             {"tag": "date",
              "patterns": ["what are you doing this weekend?",
"do you want to hang out some time?", "what are your plans for this week"],
              "responses": ["I am available all week", "I don't have any plans", "I am not busy"]
             },
             {"tag": "name",
              "patterns": ["what's your name?", "what are you called?", "who are you?"],
              "responses": ["My name is Karen", "I'm Karen", "Karen"]
             },
             {"tag": "goodbye",
              "patterns": [ "bye", "g2g", "see ya", "adios", "cya"],
              "responses": ["It was nice speaking to you", "See you later", "Speak soon!"]
             }
]}
lemmatizer = WordNetLemmatizer()
words = []
classes = []
doc_X = []
doc_y = []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_y.append(intent["tag"])
    if intent["tag"] not in classes:
        classes.append(intent["tag"])
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
words = sorted(set(words))
classes = sorted(set(classes))
training = []
out_empty = [0] * len(classes)
for idx, doc in enumerate(doc_X):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    output_row = list(out_empty)
    output_row[classes.index(doc_y[idx])] = 1
    training.append([bow, output_row])
random.shuffle(training)
training = np.array(training, dtype=object)
train_X = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))
input_shape = (len(train_X[0]),)
output_shape = len(train_y[0])
epochs = 500
model = Sequential()
model.add(Dense(128, input_shape=input_shape, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(output_shape, activation = "softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=["accuracy"])
model.fit(x=train_X, y=train_y, epochs=10000
          , verbose=0)
def clean_text(text): 
  tokens = nltk.word_tokenize(text)
  tokens = [lemmatizer.lemmatize(word) for word in tokens]
  return tokens

def bag_of_words(text, vocab): 
  tokens = clean_text(text)
  bow = [0] * len(vocab)
  for w in tokens: 
    for idx, word in enumerate(vocab):
      if word == w: 
        bow[idx] = 1
  return np.array(bow)

def pred_class(text, vocab, labels): 
  bow = bag_of_words(text, vocab)
  result = model.predict(np.array([bow]))[0]
  thresh = 0.2
  y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

  y_pred.sort(key=lambda x: x[1], reverse=True)
  return_list = []
  for r in y_pred:
    return_list.append(labels[r[0]])
  return return_list

def get_response(intents_list, intents_json): 
  tag = intents_list[0]
  list_of_intents = intents_json["intents"]
  for i in list_of_intents: 
    if i["tag"] == tag:
      '''error_message = random.choice(i)'''
      result = random.choice(i["responses"])
      break
  return result

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def home():
    print(request.method)
    if request.method == "POST":
        if request.form['button'] == "About":
            return redirect(url_for("about"))
        if request.form['button'] == "Enter Chat":
            return redirect(url_for("chat"))
    return render_template("home.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html")

@app.route("/bot", methods=["GET", "POST"])
def bot():
    return render_template("bot.html")

@socketio.on('message', namespace="/")
def handle_message(data2):
    if data2[0] != "":
        if data2[1] == "message":
            print(data2)
            print('received message: ' + data2[0])
            send(data2[0], broadcast=True)
        elif data2[1] == "username":
            print(data2[0]+" connected")
        elif data2[1] == "botMessage":
            send("&lt;you&gt; "+data2[0], broadcast=True)
            message = data2[0].lower()
            intents = pred_class(message, words, classes)
            result = get_response(intents, data)
            print(result)
            send("&lt;bot&gt; "+result, broadcast=True)
    print(data2)

if __name__ == '__main__':
    socketio.run(app) # Runs on localhost:5000