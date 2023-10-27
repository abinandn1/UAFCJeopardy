from bs4 import BeautifulSoup # Import Webscraping Package
import requests # for https requests
import re # for expression assessing, to match the pattern we are looking for for the correct answers portion


### Issue: Not all questions and choices are being pulled, because website is formatted differently in some sections? ###
def scrape_questions():

    #Generate request and parse webpage
    questions_dict = dict() #Using a dictionary for questions, where the Question is the Key, and the possible answers (as a list) is the value
    url = "https://thoughtcatalog.com/january-nelson/2020/04/multiple-choice-trivia-questions-and-answers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the section in the webpage that contains the questions and possible answers 
    questions = soup.find_all('p', {'class': 'p1'})

    # empty string used to help differentiate between question portion and possible answers portion of a question section
    current_question = ""
    
    for question in questions:
        # check and see if the data we scraped is an actual question, if it is, set the current_question to it
        if question.text.endswith("?"):
            current_question = question.text
            questions_dict[current_question] = []
        else:
            if current_question: # aka if the current question isnt a trivia question, then it is the possible answers for the current question
                questions_dict[current_question].append(question.text.strip())

    return questions_dict

def scrape_answers():
    answers_list = []

    # Generate request and parse webpage
    url = "https://thoughtcatalog.com/january-nelson/2020/04/multiple-choice-trivia-questions-and-answers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the section in the webpage that contains the correct answers
    answers = soup.find_all('p', text=re.compile(r'^\d+\.'))  # Using a regular expression to match entries starting with numbers and a period

    for answer in answers:
        answer_text = answer.text.strip()
        if "Trivia Question:" in answer_text:  # Remove trivia questions
            continue
        else:
            # Remove numbers and the period at the end using regular expressions
            cleaned_answer = re.sub(r'^\d+\.\s*', '', answer_text)
            answers_list.append(cleaned_answer)

    return answers_list

def main():
    #Call the functions and save the return data into variables
    questions = scrape_questions()
    answers = scrape_answers()

    # Print out the data we scraped
    #print(str(questions) + "\n")
    #print(answers)


main()