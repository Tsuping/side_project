import random 
import json
from shutil import SameFileError
import torch
from model import NeuralNet
from nltk_util import bag_of_word, tokenize
from weather import weather_call

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = 'data.pth'
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)

model.load_state_dict(model_state)

model.eval()

bot_name = "Sam"
print("Let's chat! type quit to quit the chat room")
while True:
    sentence = input(f'you:')
    if sentence == "quit":
        break
    if sentence == "weather?":
        city = input("city you are looking for: ")
        weather = weather_call(city)
        print(bot_name, ': ', weather)
    else:
        sentence = tokenize(sentence)
        x = bag_of_word(sentence, all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x).to(device)
        output = model(x)
        _, predict = torch.max(output, dim=1)
        tag = tags[predict.item()]

        probs = torch.softmax(output, dim = 1)
        probs = probs[0][predict.item()]

        if probs.item() > 0.8:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    print(f'{bot_name}: {random.choice(intent["responses"])}')
        else:
            print(f'{bot_name}: I do not understand')