from tkinter import *
import random

root = Tk()
root.title("Math Quiz")
root.geometry("350x450")
root.config(bg="#dbe9fd")
root.iconbitmap("Icon.ico")

frames = {}
FONT_TITLE = ("Comic Sans MS", 26, "bold")
FONT_TEXT = ("Arial", 14)
FONT_BTN = ("Arial", 12, "bold")

quiz_data = {
    "level": "",
    "low": 1,
    "high": 9,
    "answer": 0,
    "attempts_left": 2,
    "question_count": 0,
    "max_questions": 10,
    "score": 0.0,
    "num1": 0,
    "num2": 0,
    "operation": "+"
}

def show_frame(frame):
    frame.tkraise()

def randomInt():
    return random.randint(quiz_data['low'], quiz_data['high'])

def decideOperation():
    return random.choice(["+", "-"])

def isCorrect(user_answer):
    try:
        return int(user_answer) == quiz_data['answer']
    except:
        return False

def create_button(master, text, bg, fg, command, width=20):
    btn = Button(master, text=text, width=width, font=FONT_BTN, bg=bg, fg=fg,
                 activebackground=fg, activeforeground=bg, relief=RIDGE, bd=3, command=command)
    btn.bind("<Enter>", lambda e: btn.config(bg=fg, fg=bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))
    return btn

def displayMenu():
    menu_frame = Frame(root, bg="#dbe9fd")
    Label(menu_frame, text="Math Quiz", font=FONT_TITLE, bg="#dbe9fd", fg="#1a73e8").pack(pady=40)
    create_button(menu_frame, "Play", "#1a73e8", "white", lambda: show_frame(frames['Play'])).pack(pady=10)
    create_button(menu_frame, "Instructions", "#34a853", "white", lambda: show_frame(frames['Instructions'])).pack(pady=10)
    create_button(menu_frame, "Exit", "#ea4335", "white", root.quit).pack(pady=10)
    menu_frame.grid(row=0, column=0, sticky="nsew")
    frames['Menu'] = menu_frame

def displayInstructions():
    instructions_frame = Frame(root, bg="#fefefe")
    Label(instructions_frame, text="Instructions", font=FONT_TITLE, bg="#fefefe", fg="#1a73e8").pack(pady=20)
    instructions = (
        "1. Choose a difficulty level.\n\n"
        "2. Solve 10 math questions.\n\n"
        "3. You have 2 tries per question.\n\n"
        "+10% if correct on first try.\n"
        "+5% if correct on second try.\n"
        "0% if wrong on both tries.\n\n"
        "Your total score will be shown at the end!"
    )
    Label(instructions_frame, text=instructions, font=FONT_TEXT, bg="#fefefe", justify="left").pack(pady=15)
    create_button(instructions_frame, "Back to Menu", "#5f6368", "white", lambda: show_frame(frames['Menu'])).pack(pady=20)
    instructions_frame.grid(row=0, column=0, sticky="nsew")
    frames['Instructions'] = instructions_frame

def displayPlay():
    play_frame = Frame(root, bg="#eef6fc")
    Label(play_frame, text="Choose Difficulty", font=FONT_TITLE, bg="#eef6fc", fg="#1a73e8").pack(pady=30)
    create_button(play_frame, "Easy (1-digit)", "#81c995", "black", lambda: startQuiz("Easy"), width=25).pack(pady=5)
    create_button(play_frame, "Moderate (2-digit)", "#fbbc04", "black", lambda: startQuiz("Moderate"), width=25).pack(pady=5)
    create_button(play_frame, "Advanced (4-digit)", "#f28b82", "black", lambda: startQuiz("Advanced"), width=25).pack(pady=5)
    create_button(play_frame, "Back to Menu", "#5f6368", "white", lambda: show_frame(frames['Menu'])).pack(pady=20)
    play_frame.grid(row=0, column=0, sticky="nsew")
    frames['Play'] = play_frame

def displayQuiz():
    quiz_frame = Frame(root, bg="#f1f7fe")
    title_label = Label(quiz_frame, text="", font=("Comic Sans MS", 22, "bold"), bg="#f1f7fe", fg="#1a73e8")
    title_label.pack(pady=20)

    question_label = Label(quiz_frame, text="", font=("Arial", 18), bg="#f1f7fe", fg="#202124")
    question_label.pack(pady=10)

    entry = Entry(quiz_frame, font=("Arial", 16), justify="center")
    entry.pack(pady=10)

    result_label = Label(quiz_frame, text="", font=FONT_TEXT, bg="#f1f7fe", fg="#202124")
    result_label.pack(pady=10)

    score_label = Label(quiz_frame, text="Score: 0%", font=("Arial", 14, "bold"), bg="#f1f7fe", fg="#5f6368")
    score_label.pack(pady=5)

    def generateQuestion():
        if quiz_data['question_count'] >= quiz_data['max_questions']:
            displayResults()
            return
        quiz_data['num1'] = randomInt()
        quiz_data['num2'] = randomInt()
        quiz_data['operation'] = decideOperation()
        quiz_data['answer'] = quiz_data['num1'] + quiz_data['num2'] if quiz_data['operation'] == "+" else quiz_data['num1'] - quiz_data['num2']
        quiz_data['attempts_left'] = 2
        quiz_data['first_try'] = True
        quiz_data['question_count'] += 1
        question_label.config(text=f"Q{quiz_data['question_count']}: {quiz_data['num1']} {quiz_data['operation']} {quiz_data['num2']}")
        result_label.config(text=f"You have {quiz_data['attempts_left']} tries.", fg="#202124")
        entry.delete(0, END)

    def checkAnswer():
        user_answer = entry.get()
        if not user_answer.lstrip('-').isdigit():
            result_label.config(text="Please enter a valid number.", fg="#ea4335")
            entry.delete(0, END)
            return
        if isCorrect(user_answer):
            if quiz_data['first_try']:
                quiz_data['score'] += 10
                result_label.config(text="Correct! (+10%)", fg="#34a853")
            else:
                quiz_data['score'] += 5
                result_label.config(text="Correct! (+5%)", fg="#fbbc04")
            score_label.config(text=f"Score: {round(quiz_data['score'], 1)}%")
            entry.delete(0, END)
            quiz_frame.after(1000, generateQuestion)
        else:
            quiz_data['attempts_left'] -= 1
            quiz_data['first_try'] = False
            if quiz_data['attempts_left'] > 0:
                result_label.config(text=f"Wrong! Try again ({quiz_data['attempts_left']} left)", fg="#ea4335")
            else:
                result_label.config(text=f"Out of tries! The answer was {quiz_data['answer']} (+0%)", fg="#ea4335")
                entry.delete(0, END)
                quiz_frame.after(1500, generateQuestion)
            entry.delete(0, END)

    create_button(quiz_frame, "Check Answer", "#1a73e8", "white", checkAnswer).pack(pady=10)
    create_button(quiz_frame, "Back to Menu", "#5f6368", "white", lambda: show_frame(frames['Menu'])).pack(pady=10)

    quiz_frame.grid(row=0, column=0, sticky="nsew")
    frames['Quiz'] = quiz_frame
    frames['QuizWidgets'] = {'title_label': title_label, 'generateQuestion': generateQuestion}

def displayResults():
    results_frame = Frame(root, bg="#dbe9fd")
    Label(results_frame, text="Quiz Results", font=FONT_TITLE, bg="#dbe9fd", fg="#1a73e8").pack(pady=30)

    result_label = Label(results_frame, text="", font=FONT_TEXT, bg="#dbe9fd")
    result_label.pack(pady=10)

    grade_label = Label(results_frame, text="", font=("Arial", 18, "bold"), bg="#dbe9fd")
    grade_label.pack(pady=5)

    create_button(results_frame, "Play Again", "#34a853", "white", lambda: show_frame(frames['Play'])).pack(pady=15)
    create_button(results_frame, "Back to Menu", "#5f6368", "white", lambda: show_frame(frames['Menu'])).pack(pady=5)

    results_frame.grid(row=0, column=0, sticky="nsew")
    frames['Results'] = results_frame
    frames['ResultsWidgets'] = {'result_label': result_label, 'grade_label': grade_label}

    percentage = round(quiz_data['score'], 1)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    frames['ResultsWidgets']['result_label'].config(text=f"Score: {percentage}%")
    frames['ResultsWidgets']['grade_label'].config(text=f"Grade: {grade}")
    show_frame(frames['Results'])

def startQuiz(level):
    quiz_data['level'] = level
    quiz_data['question_count'] = 0
    quiz_data['score'] = 0.0
    if level == "Easy":
        quiz_data['low'], quiz_data['high'] = 1, 9
    elif level == "Moderate":
        quiz_data['low'], quiz_data['high'] = 10, 99
    else:
        quiz_data['low'], quiz_data['high'] = 1000, 9999

    frames['QuizWidgets']['title_label'].config(text=f"{level} Mode")
    show_frame(frames['Quiz'])
    frames['QuizWidgets']['generateQuestion']()

displayMenu()
displayInstructions()
displayPlay()
displayQuiz()
displayResults()
show_frame(frames['Menu'])
root.mainloop()