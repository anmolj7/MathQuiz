import io
import tkinter as tk
import random
import os
import tkinter.messagebox as tkMessageBox


def clear():
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')


def breakline():
    print('-' * 60)


def get_questions():
    with io.open('questions.txt', encoding="utf-8") as f:
        data = f.readlines()
    # Last line is answers.
    Answers = data[-1]
    Answers = Answers.split(', ')
    Answers = [ans.strip('(').strip(')') for ans in Answers]
    data = data[:-1]
    Questions = {}
    for i in range(0, len(data), 5):
        question = data[i].strip('\n')
        Questions[question] = []
        for j in range(i + 1, i + 5):
            Questions[question].append(data[j].strip('\n'))
        Questions[question].append(Answers[i // 5])
    return Questions


def get_random(List, n=10):
    """Returns the N random Items from the list, such that questions never repeat."""
    assert len(List) > n
    temp = []
    while True:
        if len(temp) == n:
            return temp
        x = random.choice(List)
        if x not in temp:
            temp.append(x)


class App:
    def __init__(self, N, n_questions=10):
        self.n_questions = n_questions
        self.score = 0
        self.Groups = {}
        self.Questions = get_questions()
        self.rand_questions = get_random(list(self.Questions.keys()), self.n_questions)
        self.Questions = {question: self.Questions[question] for question in self.rand_questions}

        self.create_groups(N)

        self.app = tk.Tk()
        self.question = tk.StringVar()
        self.curr_ques_str = tk.StringVar()
        self.opt_selected = tk.IntVar()
        self.curr_ques = 0
        # Packing Stuff.
        tk.Label(self.app, text="ss", textvariable=self.question).pack(side=tk.TOP)
        tk.Button(self.app, text="Next", command=self.next_button).pack(side=tk.BOTTOM)
        tk.Label(self.app, text="", textvariable=self.curr_ques_str).pack(side=tk.BOTTOM)
        self.button_texts = [tk.StringVar() for _ in range(4)]

        self.create_options()
        self.start()

        self.app.mainloop()

    def create_groups(self, N):
        breakline()
        print('Assigning Groups letters.')
        breakline()
        for i in range(N):
            print(f'The group letter for group {i + 1}: {chr(65 + i)}')
            self.Groups[chr(65 + i)] = 0
        breakline()

    def next_button(self):
        if self.get_curr_ans() != self.opt_selected.get():
            tkMessageBox.showinfo("Wrong Answer!",
                                  f"The Correct Answer is: {self.Questions[self.rand_questions[self.curr_ques]][self.get_curr_ans() - 1]}")
        else:
            tkMessageBox.showinfo("Correct Answer!", "The Chosen opton is correct.")
            self.score += 1
        self.curr_ques += 1
        self.start()

    def get_curr_ans(self):
        char = self.Questions[self.rand_questions[self.curr_ques]][-1]
        return ord(char) - 64

    def start(self):
        if self.curr_ques == self.n_questions:
            tkMessageBox.showinfo("The Game ended.", f"Your Score is: {self.score}")
            self.app.destroy()
            exit()
        self.curr_ques_str.set(f'{self.curr_ques+1}/{self.n_questions}')
        self.question.set(self.rand_questions[self.curr_ques])
        self.set_options()

    def set_options(self):
        options = self.Questions[self.rand_questions[self.curr_ques]][:-1]
        for index, option in enumerate(options):
            self.button_texts[index].set(option)

    def create_options(self):
        options = self.Questions[self.rand_questions[self.curr_ques]][:-1]
        for index, text in enumerate(options):
            tk.Radiobutton(self.app, textvariable=self.button_texts[index], variable=self.opt_selected,
                           value=index + 1).pack(side=tk.TOP, anchor="w")


def main():
    clear()
    n_groups = int(input('Enter the number of groups: '))
    assert n_groups in range(2, 11), "number of groups can't be bigger than 10 and less than 2"
    print('Starting Game.')
    App(5)


if __name__ == '__main__':
    main()
