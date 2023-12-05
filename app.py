# import streamlit as st
# import langchain  # Mock library for generating options
# from langchain.llms import OpenAI
# from dotenv import load_dotenv
# import os

# from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     SystemMessagePromptTemplate,
# )
# from langchain.schema import HumanMessage, SystemMessage
# # Set your OpenAI API key
# load_dotenv()
# OpenAI.api_key = os.environ.get("OPENAI_API_KEY")

#     # Mock function for OpenAI API to generate questions
# def generate_question(prompt):
#     llm = OpenAI()
    
#     response = llm.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": "Generate a multiple choice question  on {prompt} and generate 4 answers and show the correct answer"}],
#         temperature=0.5,
#         max_tokens=64,
#         top_p=1
#     )
#     return response

# chat = ChatOpenAI(temperature=0.1)
# messages = [
   
#     HumanMessage(
#         content="say hello"
#     ),
# ]
# chat.invoke(messages)   


# # Streamlit UI

# def display_quiz(questions):
#     # Clear existing widgets with the same key
#     st.session_state.pop("user_answers", None)
    
#     # Display questions and get user answers
#     user_answers = []
#     for i, question in enumerate(questions, start=1):
#         st.subheader(f"Question {i}: {question}")
#         #selected_option = st.radio("Select your answer:", options, key=f"radio_{i}")
#         user_answers.append({"question": question})

#     if st.button("Submit Answers"):
#         st.session_state.user_answers = user_answers
#         return user_answers
#     else:
#         return []

# def calculate_score(questions, user_answers):
#     # Calculate the score based on user answers
#     score = 0
#     for i, question in enumerate(questions):
#         if i < len(user_answers) and user_answers[i]['user_answer'] == question['options'][0]:
#             score += 1
#     return score

# def main():
#     st.title("Dynamic Quiz Generator")

#     # User input
#     topic = st.text_input("Enter the quiz topic:")
#     quiz_questions =[]
#     num_questions = st.number_input("How many questions do you want?", min_value=1, step=1)
#  # Loop to generate each question
#     if st.button("Generate Quiz"):
#         for i in range(1, num_questions + 1):
#             # Construct a prompt for generating quiz questions
           
            
#             # Call OpenAI API to generate quiz question
#             question = generate_question(topic)
            
#             # Append the generated question to the list
#             quiz_questions.append(question)

        
#             # Call a function to fetch dynamic questions using Langchain and OpenAI
    
#             # Display questions and get user answers
#             user_answers = display_quiz(quiz_questions)

#         # Calculate and display the score

#     # if st.button("Submit Answers", on_click="WidgetCallBack"):
#     #     score = calculate_score(quiz_questions, user_answers)
#     #     st.success(f"Your score: {score}/{len(quiz_questions)}")
# if __name__ == "__main__":
#     main()


####################################################################################


import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv  

def generate_questions(topic, num_questions):
    load_dotenv()
    chat= ChatOpenAI(temperature=0.1)
    prompt = f"""generate {num_questions} multiple choice questions on {topic} with 4 options to each question but only one answer from them and give me the  answer,
    And make the Question no matter how long on one line, and the options after them in a line each option"""
    messages = [SystemMessage(content=prompt)]
    questions = chat.invoke(messages)
    # print("++++++++++++++++++++++++++")
    # print(questions.content)
    # print("+++++++++++++++++++++++")
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
        # Call a function to fetch dynamic questions using OpenAI
        questions = generate_questions(topic, num_questions)
        # Display questions and answers
        display_quiz(questions,num_questions)
        


def display_quiz(questions, num_questions):
    # Display questions and get user answers
    with st.form("quiz_form"):
        user_answers = []
        for i in range(1, num_questions + 1):
            st.subheader(f"{questions['generated_questions'][i]}")
            options = questions['options'][i]
            selected_option = st.radio(f"Select your answer for Question {i}:", options)
            user_answers.append(selected_option)

        # Use st.form_submit_button and check if the button text is present in the form submission
        if st.form_submit_button("Submit") in st.session_state:
            print("Inside submit block")
            answers = questions['answers']
            for i in range(len(answers)):
                answers[i + 1] = answers[i + 1].split(") ")[1]
                user_answers[i] = user_answers[i].split(") ")[1]

            score = calculate_score(answers, user_answers)
            st.write(f"Your score: {score}/{num_questions}")


def calculate_score(answers, user_answers):
    # Calculate the score based on user answers
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





