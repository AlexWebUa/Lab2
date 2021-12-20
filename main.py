from tkinter.filedialog import askopenfilename
from tkinter import *
import pandas as pd

master = Tk()
master.geometry('320x120')
master.resizable(height=False, width=False)
entry = Entry(master)

entry.place(x=10, y=10, width=300, height=20)
entry.focus_set()
label = Label(text="")
label.place(x=10, y=90)

ham_dic = {}
spam_dic = {}


def algorithm():
    count_spam = 0
    count_ham = 0
    for i in ham_dic.keys():
        count_ham = count_ham + ham_dic.get(i)
    for i in spam_dic.keys():
        count_spam = count_spam + spam_dic.get(i)

    if count_ham == 0 or count_spam == 0:
        label.config(text="Selec tanother file")
    else:
        sentence = ''.join(c for c in entry.get() if c.isalpha() or c == " ").lower()
        words = sentence.split()
        words_not_in_ham = 0
        words_not_in_spam = 0
        p_ham = 1.0
        p_spam = 1.0

        # num of words NOT in dicts
        for s in words:
            if ham_dic.get(s) is None:
                words_not_in_ham += 1
            if spam_dic.get(s) is None:
                words_not_in_spam += 1
        # calculating P(spam) & P(ham) with Bayes theorem
        for s in words:
            if words_not_in_ham != 0:
                if ham_dic.get(s):
                    num_words_in_ham = ham_dic.get(s) + 1
                else:
                    num_words_in_ham = 1
                p_ham = p_ham * (num_words_in_ham / (count_ham + words_not_in_ham))
            else:
                if ham_dic.get(s):
                    num_words_in_ham = ham_dic.get(s)
                p_ham = p_ham * (num_words_in_ham / count_ham)

            if words_not_in_spam != 0:
                if spam_dic.get(s):
                    num_words_in_spam = spam_dic.get(s) + 1
                else:
                    num_words_in_spam = 1
                p_spam = p_spam * (num_words_in_spam / (count_spam + words_not_in_spam))
            else:
                if spam_dic.get(s):
                    num_words_in_spam = spam_dic.get(s)
                p_spam = p_spam * (num_words_in_spam / count_spam)

        is_ham = (count_ham / (count_ham + count_spam)) * p_ham
        is_spam = (count_spam / (count_ham + count_spam)) * p_spam

        print(is_ham, is_spam)
        is_ham_n = is_ham / (is_ham + is_spam) * 100
        is_spam_n = is_spam / (is_spam + is_ham) * 100
        if is_spam > is_ham:
            tmp = "SPAM"
        else:
            if is_spam <= is_ham:
                tmp = "HAM"
        stg = ''.join("Ham: " + str(round(is_ham_n, 2)) + "%\tSpam: " + str(round(is_spam_n, 2)) + "%\tThis is " + tmp)

    label.config(text=stg)


def open_file():
    filename = askopenfilename()
    if filename != "":
        try:
            sample = pd.read_csv(filename)

            all_ham = sample[sample.v1 == "ham"]
            all_spam = sample[sample.v1 == "spam"]

            ham_str = []
            spam_str = []

            # deleting special characters and numbers; converting to lowercase
            for s in all_ham.v2:
                ham_str.append("".join(c for c in s if c.isalpha() or c == " ").lower())
            for s in all_spam.v2:
                spam_str.append("".join(c for c in s if c.isalpha() or c == " ").lower())

            stop_words = ["a", "the", "an", "of", "on", "to", "in"]

            flag = True
            ham = []
            spam = []
            # убираем стоп слова
            for s in spam_str:
                for s2 in s.split():
                    for s3 in stop_words:
                        if s2 == s3: flag = False
                    if flag: spam.append(s2)
                    flag = True

            for s in ham_str:
                for s2 in s.split():
                    for s3 in stop_words:
                        if s2 == s3: flag = False
                    if flag: ham.append(s2)
                    flag = True

            # считаем к-во вхождений каждого слова
            for s in ham:
                if ham_dic.get(s):
                    ham_dic.update({s: ham_dic.get(s) + 1})
                else:
                    ham_dic.setdefault(s, 1)

            for s in spam:
                if spam_dic.get(s):
                    spam_dic.update({s: spam_dic.get(s) + 1})
                else:
                    spam_dic.setdefault(s, 1)
            label.config(text="File uploaded")

            buttonCount.config(state='normal')
        except Exception:
            label.config(text="Choose another file")


buttonCount = Button(master, text="Find", width=10, command=algorithm)
buttonCount.place(x=10, y=50)
buttonCount.config(state='disabled')
buttonOpen = Button(master, text="Open", width=10, command=open_file)
buttonOpen.place(x=230, y=50)
mainloop()
