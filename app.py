import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv  

def generate_questions(topic, num_questions):
    load_dotenv() # load variables present in .env file
    chat = ChatOpenAI(temperature=0.1) # connect to the openai api key with the default variable name to be "OPENAI_API_KEY" , and temprature means creativity in making the questions
    prompt = f"""generate {num_questions} multiple choice questions on {topic} with 4 options to each question but only one answer from them and give me the  answer,
    And make the Question no matter how long on one line, and the options after them in a line each option"""
    messages = [SystemMessage(content=prompt)]
    questions = chat.invoke(messages)
 
    generated_information = questions.content
    y = generated_information.split("\n")
    while('' in y):
        i = y.index('')
        y.pop(i)
    generated_question = {}
    options = {}
    answers = {}
    
    j=1

    for i in range (0,len(y),6):
        generated_question[j] = y[i]
        j+=1

    j=1
   
    for i in range (1,len(y),6):
        options[j] = [y[i],y[i+1],y[i+2],y[i+3]]
        j+=1
        
    j=1

    for i in range (5,len(y),6):
        answers[j] = y[i]
        j+=1

    return {"generated_questions" : generated_question ,"options": options,"answers":answers }

def main():
    st.title("Dynamic Quiz Generator")

    # User input
    topic = st.text_input("Enter the quiz topic:")
    num_questions = st.number_input("How many questions do you want?", min_value=1, step=1)
    if st.button("Generate Quiz"):
        questions = generate_questions(topic, num_questions)
        display_quiz(questions,num_questions)


def display_quiz(questions, num_questions):
    with st.form("quiz_form"):
        user_answers = []
        for i in range(1, num_questions + 1):
            st.subheader(f"{questions['generated_questions'][i]}")
            options = questions['options'][i]
            selected_option = st.radio(f"Select your answer for Question {i}:", options)
            user_answers.append(selected_option)

        if st.form_submit_button("Submit"):
            print("Inside submit block")
            answers = questions['answers']
            for i in range(len(answers)):
                answers[i + 1] = answers[i + 1].split(") ")[1]
                user_answers[i] = user_answers[i].split(") ")[1]

            score = calculate_score(answers, user_answers)
            st.write(f"Your score: {score}/{num_questions}")

def calculate_score(answers, user_answers):
    score = 0
    for i in range(len(answers)):
        if answers[i+1] ==user_answers[i]:
            score+=1
    return score

if __name__ == "__main__":
    main()
####################################################################################
 
#  {
#      'generated_questions': 
#      {
#         1: '1. What is the value of x in the equation 3x + 5 = 20?',
#         2: '2. Which of the following is a prime number?', 
#         3: '3. What is the square root of 144?', 
#         4: '4. If a triangle has angles measuring 30°, 60°, and 90°, what type of triangle is it?', 
#         5: '5. What is the value of π (pi) rounded to two decimal places?'
#         }, 
#     'options': 
#     {
#         1: ['a) 5', 'b) 7', 'c) 8', 'd) 15'], 
#         2: ['a) 12', 'b) 17', 'c) 20', 'd) 25'], 
#         3: ['a) 9', 'b) 12', 'c) 16', 'd) 18'], 
#         4: ['a) Equilateral triangle', 'b) Isosceles triangle', 'c) Scalene triangle', 'd) Right triangle'], 
#         5: ['a) 3.14', 'b) 3.16', 'c) 3.18', 'd) 3.20']
#         },
#     'answers': 
#     {
#         1: 'Answer: c) 8', 
#         2: 'Answer: b) 17', 
#         3: 'Answer: b) 12', 
#         4: 'Answer: d) Right triangle', 
#         5: 'Answer: a) 3.14'
#         }
#     }
