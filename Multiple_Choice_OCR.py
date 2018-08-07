#! python3
import os
import io
from google.cloud import vision
from google.cloud.vision import types
import requests, bs4
import re, sys, time, shutil
import os.path
import webbrowser
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Programming\PythonScripts\hqtrivia-3f34ac5d8999.json"



#global variable
words = []              #list of words in the question, along with answer choices
top_question = []
choices = []
onChoices = False
first_choice = []
second_choice = []
third_choice = []
first_choice_points = 0
second_choice_points = 0
third_choice_points = 0






# [START def_detect_text]
def detect_text(path):
    print('reading image...')
    global first_choice 
    global second_choice
    global third_choice 
    last_vertex = 0
    whichChoice = 1
        
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')

    for index, text in enumerate(texts):
        global onChoices
        
        



        words.append(text.description)
        #print('\n"{}"'.format(text.description))

        #Seperate the answers choices into seperate lists 
        if onChoices:
            if abs(last_vertex - text.bounding_poly.vertices[1].y) < 10 or last_vertex == 0:
                if whichChoice == 1:
                    first_choice.append(text.description)
                    last_vertex = text.bounding_poly.vertices[1].y
                elif whichChoice == 2:
                    second_choice.append(text.description)
                    last_vertex = text.bounding_poly.vertices[1].y
                elif whichChoice == 3:
                    third_choice.append(text.description)
                    last_vertex = text.bounding_poly.vertices[1].y
            else:
                whichChoice = whichChoice + 1
                if whichChoice == 2:
                    second_choice.append(text.description)
                    last_vertex = text.bounding_poly.vertices[1].y
                elif whichChoice == 3:
                    third_choice.append(text.description)
                    last_vertex = text.bounding_poly.vertices[1].y
                
                
        else:
            top_question.append(text.description)




        if '?' in text.description and index != 0:
            onChoices = True
        
        
       

        vertices = (['({},{})'.format(vertex.x, vertex.y)

        
                    for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))
    # [END migration_text_detection]
    words.pop(0)
    
# [END def_detect_text]



# Takes the question from the image puts into google
def scrape():
    choice1 = ' '.join(first_choice)
    choice2 = ' '.join(second_choice)
    choice3 = ' '.join(third_choice)
    question = ' '.join(top_question)
    print('Googling...')


    #Google the question
    res = requests.get('http://google.com/search?q=' + question)
    res.raise_for_status()

    webbrowser.open('http://google.com/search?q=' + question)


    #return html for results page
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElems = soup.select('.r a')

    numSearch = min(5, len(linkElems))
    for i in range(numSearch):
        theLink = 'http://google.com' + linkElems[i].get('href')
        scanSite(theLink, i)

       
        
        
        
    



#scans the site for hits on the choices
def scanSite(link, rank):
    choice1 = ' '.join(first_choice)
    choice2 = ' '.join(second_choice)
    choice3 = ' '.join(third_choice)
    choice1 = choice1.lower()
    choice2 = choice2.lower()
    choice3 = choice3.lower()
    global first_choice_points
    global second_choice_points
    global third_choice_points
    
#load the current webpage of the search result
    res = requests.get(link)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('Cant load web page')

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    siteText = soup.get_text()
    siteText = siteText.lower()
    points1 = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(choice1), siteText))
    points2 = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(choice2), siteText))
    points3 = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(choice3), siteText))
    multiplier = (10000 - (rank * 2500))


    first_choice_points = first_choice_points + (points1*multiplier)  
    second_choice_points = second_choice_points + (points2*multiplier)
    third_choice_points = third_choice_points + (points3*multiplier)

    print(choice1 + ':' + str(first_choice_points) + '\n')
    print(choice2 + ':' + str(second_choice_points) + '\n')
    print(choice3 + ':' + str(third_choice_points) + '\n\n\n')

    point_printer(choice1, choice2, choice3, ' '.join(top_question))

    #if first_choice_points > second_choice_points and first_choice_points > third_choice_points:
     #  print(choice1 + ' IS WINNING!!!')
      # print(choice1 + ' IS WINNING!!!')
       #print(choice1 + ' IS WINNING!!!')
    #if second_choice_points > first_choice_points and second_choice_points > third_choice_points:
     #   print(choice2 + ' IS WINNING!!!')
      #  print(choice2 + ' IS WINNING!!!')
       # print(choice2 + ' IS WINNING!!!')
    #if third_choice_points > first_choice_points and third_choice_points > second_choice_points:
     #   print(choice3 + ' IS WINNING!!!')
      #  print(choice3 + ' IS WINNING!!!')
       # print(choice3 + ' IS WINNING!!!')



def point_printer (firstChoice, secondChoice, thirdChoice, question):
    hasNot = False
    
    global first_choice_points
    global second_choice_points
    global third_choice_points
    points = [first_choice_points, second_choice_points, third_choice_points]
    #dictionary to associate the point value with the choice
    answers = {first_choice_points: firstChoice, second_choice_points: secondChoice, third_choice_points: thirdChoice}
    points.sort()
    theQuestion = ' '.join(top_question)
    theQuestion = theQuestion.lower()
    

    if 'not' in theQuestion or 'never' in theQuestion:
        hasNote = True

        if points[0] < points[1]:
            print(answers[points[0]] + ' IS WINNING!!!')
            print(answers[points[0]] + ' IS WINNING!!!')
            print(answers[points[0]] + ' IS WINNING!!!')

        elif points[0] == points[1] and points[0] != points[2]:
            print(answers[points[0]] + ' OR ' + answers[points[1]])
            print(answers[points[0]] + ' OR ' + answers[points[1]])
            print(answers[points[0]] + ' OR ' + answers[points[1]])
        else:
            print('ANY CHOICE... sorry')
            print('ANY CHOICE... sorry')
            print('ANY CHOICE... sorry')

    else:
        print(answers[points[2]] + ' IS WINNING!!!')
        print(answers[points[2]] + ' IS WINNING!!!')
        print(answers[points[2]] + ' IS WINNING!!!')
            
            
            

        
        
        

def run_program():
    while True:
        if os.path.exists('D:\\Pictures\\hqtrivia pictures\\HQtriviafolder\\THEQUESTION.png'):
            detect_text('D:\\Pictures\\hqtrivia pictures\\HQtriviafolder\\THEQUESTION.png')
            scrape()
            shutil.move('D:\\Pictures\\hqtrivia pictures\\HQtriviafolder\\THEQUESTION.png', 'C:\\Users\\Tony\\Pictures\\HQarchive\\' + str(first_choice) + '.png')

            exit()
            
        else:
            print('no picture found')


run_program()


    







    
