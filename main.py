from flask import Flask, render_template, request, jsonify
import pickle
import nltk
from newspaper import Article
import random
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import numpy as np

warnings.filterwarnings('ignore')
import ssl
try:
    _create_unverified_https_context=ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context=_create_unverified_https_context

nltk.download('punkt', quiet=True)

article=Article('https://www.mayoclinic.org/diseases-conditions/heart-disease/symptoms-causes/syc-20353118')
article.download()
article.parse()
#article="Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high, Blood glucose is your main source of energy and comes from the food you eat, Insulin, a hormone made by the pancreas, helps glucose from food get into your cells to be used for energy, Sometimes your body doesn’t make enough or any insulin or doesn’t use insulin well, Glucose then stays in your blood and doesn’t reach your cells. Over time, having too much glucose in your blood can cause health problems, Although diabetes has no cure, you can take steps to prevent diabetes and stay healthy, Sometimes people call diabetes “a touch of sugar” or “borderline diabetes”. The different types of diabetes are type 1, type 2, and gestational diabetes. TYPE-1: If you have type 1 diabetes, your body does not make insulin, Your immune system attacks and destroys the cells in your pancreas that make insulin., Type 1 diabetes is usually diagnosed in children and young adults, although it can appear at any age, People with type 1 diabetes need to take insulin every day to stay alive, TYPE-2: If you have type 2 diabetes, your body does not make or use insulin well, You can develop type 2 diabetes at any age, even during childhood, However, this type of diabetes occurs most often in middle-aged and older people, Type 2 is the most common type of diabetes, Gestational diabetes: It develops in some women when they are pregnant, Most of the time, this type of diabetes goes away after the baby is born, However, if you’ve had gestational diabetes, you have a greater chance of developing type 2 diabetes later in life, Sometimes diabetes diagnosed during pregnancy is actually type 2 diabetes, Other types: Less common types include monogenic diabetes, which is an inherited form of diabetes, and cystic fibrosis-related diabetes, People diagnosed with diabetes are: As of 2015, 30.3 million people in the United States, or 9.4 percent of the population, had diabetes, More than 1 in 4 of them didn’t know they had the disease, Diabetes affects 1 in 4 people over the age of 65, About 90-95 percent of cases in adults are type 2 diabetes. Over time, diabetes leads to problems such as, heart disease, stroke, kidney disease, eye problems, dental disease, nerve damage, foot problems. Symptoms of diabetes are: Urinate (pee) a lot, often at night, Are very thirsty, Lose weight without trying, Are very hungry, Have blurry vision, Have numb or tingling hands or feet, Feel very tired, Have very dry skin. Ways to prevent diabetes are, 1 Reduce carb intake, 2 Exercise regularly, 3 Drink a lot of water, 4 Try to lose excess weight, 5 Reduce potion sizes, 6 Follow high fibre diet, etc.Treatment for diabetes are: Treatment for type 1 diabetes involves insulin injections or the use of an insulin pump, frequent blood sugar checks, and carbohydrate counting, Treatment of type 2 diabetes primarily involves lifestyle changes, monitoring of your blood sugar, along with diabetes medications, insulin or both.The term “heart disease” refers to several types of heart conditions, The most common type of heart disease is coronary artery disease (CAD), which affects the blood flow to the heart, Decreased blood flow can cause a heart attack. Symptoms of heart disease include, Heart attack: Chest pain or discomfort, upper back or neck pain, indigestion, heartburn, nausea or vomiting, extreme fatigue, upper body discomfort, dizziness, and shortness of breath, Arrhythmia: Fluttering feelings in the chest (palpitations), Heart failure: Shortness of breath, fatigue, or swelling of the feet, ankles, legs, abdomen, or neck veins. In general, treatment for heart disease usually includes: Lifestyle changes: You can lower your risk of heart disease by eating a low-fat and low-sodium diet, getting at least 30 minutes of moderate exercise on most days of the week, quitting smoking, and limiting alcohol intake, Medications: If lifestyle changes alone aren't enough, your doctor may prescribe medications to control your heart disease, The type of medication you receive will depend on the type of heart disease, Medical procedures or surgery: If medications aren't enough, it's possible your doctor will recommend specific procedures or surgery, The type of procedure or surgery will depend on the type of heart disease and the extent of the damage to your heart. Prevention of heart disease: 1 Don’t smoke or use tobacco, 2 Get moving: Aim for minimum 30 mins of daily activity, 3 Eat heart healthy diet, avoid oily food, 4 Maintain healthy weight, 5 Manage stress, 6 Get regular health screenings."
article.nlp()
corpus=article.text
#print(corpus)

sentence_list=nltk.sent_tokenize(text=article)
#print(sentence_list)

#Greeting
def greeting(text):
    text=text.lower()

    bot_greeting=['hello','hey, how you doing','heya','hola','hi']

    user_greeting=['hello','hey, how you doing','heya','hola','hi','hey']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)

def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))

    x=list_var
    for i in range (length):
        for j in range (length):
            if x[list_index[i]]>x[list_index[j]]:
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    return list_index

def bot_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response+''+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break

    if response_flag==0:
        bot_response=bot_response+''+"Sorry,I don't understand"

    sentence_list.remove(user_input)
    return bot_response

app = Flask(__name__)

#model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get', methods=['GET','POST'])
def chat():
    userinput = request.args.get('msg')
    exit_list = ['bye', 'thanks', 'thank you', 'good bye', 'see you later', 'quit']
    while (True):
        if userinput.lower() in exit_list:
            return "I will miss taking to you!!Bye Bye"
        else:
            ans=''
            if greeting(userinput) != None:
                ans+=greeting(userinput)
            else:
                ans+=bot_response(userinput)
            return ans

'''
    exit_list = ['bye', 'thanks', 'thank you', 'good bye', 'see you later', 'quit']
    while (True):
        data = ''
        if user.lower() in exit_list:
            data+= "I will miss taking to you!!Bye Bye"
            return render_template('chat.html', output=data)
        else:
            if greeting(user) != None:
                data=greeting(user)
                return render_template('chat.html', output=data)
            else:
                data+=bot_response(user)
                return render_template('chat.html', output=data)
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

