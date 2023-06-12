# Made by @WhineyMonkey10

import requests
import colorama

quizID = input(f"{colorama.Fore.GREEN}Enter the game ID: {colorama.Fore.RESET}")

data = requests.get("https://play.kahoot.it/rest/kahoots/"+quizID)

def getQuestionAnswer(questionName):
    try:
        for question in data.json()["questions"]:
            if question["question"] == questionName:
                return [answer["answer"] for answer in question["choices"] if answer["correct"] == True][0]
    except:
        print(f"{colorama.Fore.RED}Error: {colorama.Fore.YELLOW}Either the question doesn't exit or it is not a multiple choice question.{colorama.Fore.RESET}")
        return "Error"

if data.status_code == 200:
    print(f"{colorama.Fore.GREEN}Game found!{colorama.Fore.RESET}")
    print(f"{colorama.Fore.GREEN}Title: {colorama.Fore.RESET}"+data.json()["title"])
    print(f"{colorama.Fore.GREEN}Description: {colorama.Fore.RESET}"+data.json()["description"])
    while True:
        questionName = input(f"{colorama.Fore.GREEN}Question to search for: {colorama.Fore.RESET}")
        answer = getQuestionAnswer(questionName)
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