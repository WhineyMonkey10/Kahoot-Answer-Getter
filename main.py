# Made by @WhineyMonkey10

import requests
import colorama

print(f'''{colorama.Fore.YELLOW}
      
      
___________         ____  __.      .__                   __   
\_   _____/_______ |    |/ _|____  |  |__   ____   _____/  |_ 
 |    __)_\___   / |      < \__  \ |  |  \ /  _ \ /  _ \   __/
 |        \/    /  |    |  \ / __ \|   Y  (  <_> |  <_> )  |  
/_______  /_____ \ |____|__ (____  /___|  /\____/ \____/|__|  
        \/      \/         \/    \/     \/                    

      
      {colorama.Fore.RESET}''')


quizID = input(f"{colorama.Fore.MAGENTA}Enter the game ID > {colorama.Fore.RESET}")

data = requests.get("https://play.kahoot.it/rest/kahoots/"+quizID)

def getQuestionAnswer(questionName):
    try:
        for question in data.json()["questions"]:
            if question["question"] == questionName:
                answer = [answer["answer"] for answer in question["choices"] if answer["correct"] == True]
                if type(answer) == list:
                    if input(f"{colorama.Fore.MAGENTA}Multiple answers found. Do you want to see all of them? (y/n) > {colorama.Fore.RESET}") == "y":
                        answer = ", ".join(answer)
                        answer = answer.replace("[", "")
                        print(f"{colorama.Fore.GREEN}Answers: {colorama.Fore.RESET}"+answer)
                        return "MULTIPLE_ANSWERS"
                    else:
                        print(f"{colorama.Fore.GREEN}Giving you the first answer.{colorama.Fore.RESET}")
                        print(answer[0])
                        return "MULTIPLE_ANSWERS"
                        
                
    except:
        print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Either the question doesn't exit or it is not a multiple choice question.{colorama.Fore.RESET}")
        return "Error"

if data.status_code == 200:
    print(f"{colorama.Fore.GREEN}Game found!{colorama.Fore.RESET}")
    print(f"{colorama.Fore.GREEN}Title: {colorama.Fore.RESET}"+data.json()["title"])
    print(f"{colorama.Fore.GREEN}Description: {colorama.Fore.RESET}"+data.json()["description"])
    while True:
        questionName = input(f"{colorama.Fore.MAGENTA}Question to search for > {colorama.Fore.RESET}")
        answer = getQuestionAnswer(questionName)
        if answer == "MULTIPLE_ANSWERS":
            pass
        else:
            try:
                print(f"{colorama.Fore.GREEN}Answer: {colorama.Fore.RESET}"+answer)
            except:
                print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Either the question doesn't exit or it is not a multiple choice question.{colorama.Fore.RESET}")

else:
    if data.json()["error"] == "INVALID_DATA" or data.json()["error"] == "NOT_FOUND":
        print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Game not found.{colorama.Fore.RESET}")
    elif data.json()["errorCode"] == 49:
        print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Game is private.{colorama.Fore.RESET}")
    else:
        print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Unknown error.{colorama.Fore.RESET}")
        if input(f"{colorama.Fore.GREEN}Do you want to see the error? (y/n): {colorama.Fore.RESET}") == "y":
            print(data.json())