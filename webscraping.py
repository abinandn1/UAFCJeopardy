from bs4 import BeautifulSoup
import requests
import re

def scrape_questions_and_answers():
    questions_dict = {}  # Using a dictionary for questions and answers
    url = "https://thoughtcatalog.com/january-nelson/2020/04/multiple-choice-trivia-questions-and-answers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    questions = soup.find_all('p', {'class': 'p1'})
    answers = soup.find_all('p', text=re.compile(r'^\d+\.'))

    current_question = None
    cleaned_answers = []
    trivia_question = False  # flag trivia questions

    for answer in answers:
        answer_text = answer.text.strip()
        if "Trivia Question:" in answer_text:
            trivia_question = True
            current_question = None  # resets current question
        else:
            cleaned_answer = re.sub(r'^\d+\.\s*', '', answer_text)
            cleaned_answers.append(cleaned_answer)
            trivia_question = False

    for question in questions:
        question_text = question.text.strip()
        if question_text.endswith("?") and not trivia_question:
            current_question = question_text
            questions_dict[current_question] = [[], []]
        elif current_question and not trivia_question:
            if len(questions_dict[current_question][0]) < 4:
                question_text= re.sub(r'^[a-d]\) ', '', question_text)
                questions_dict[current_question][0].append(question_text)
                if cleaned_answers:
                    for cleaned_answer in cleaned_answers:
                        if current_question == '12. Trivia Question: In Pirates of the Caribbean, what was Captain Jack Sparrow’s ship’s name?': # hardcode fix :(
                            cleaned_answer = 'The Black Pearl'
                        if cleaned_answer == "Nixon": # hardcode fix :(
                            cleaned_answer = 'Richard Nixon'
                        if cleaned_answer in question_text:
                            questions_dict[current_question][1].append(cleaned_answer)

    return questions_dict

def main():
    data = scrape_questions_and_answers()
    #print(data)

main()
