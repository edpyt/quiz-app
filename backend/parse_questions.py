import re
from bs4 import BeautifulSoup
from quiz.models import Quiz, QuizAnswers


with open('parse.html', 'r', encoding='UTF-8') as html_parser_file:
    soup = BeautifulSoup(html_parser_file, 'html.parser')
    
    questions = soup.find_all('b')
    answers = soup.find_all('ul')
    
    new_questions = (q_text for question in questions
                     if '?' in (q_text:=question.text))

    with open('answers.txt', 'r', encoding='UTF-8') as question_answer:
        q_answer_file = question_answer.read()
        q_answer_list = (q_answer[3:] for q_answer in q_answer_file.split('\n'))
    
    for question, answer, q_answer in zip(new_questions, answers, q_answer_list):
        parsed_question = re.findall(r'\d*[\.\:]?\s?(.+\?)', question)
        print(parsed_question[0])
        parsed_answer = list(j.strip() for j in re.findall(r'\)(.+)', answer.text))
        
        real_answer = None
        
        quiz_model = Quiz.objects.create(question=parsed_question[0])
        
        for p_answer in parsed_answer:
            QuizAnswers.objects.create(answer=p_answer,
                                       quiz_fk=quiz_model)
            if q_answer.lower() in p_answer.lower():
                real_answer = p_answer
        
        if real_answer is None:
            real_answer = q_answer
            
        quiz_model.answer = real_answer
        
        quiz_model.save()