import csv
'''
bug: 字符串find时候，找不到是-1，不能直接用if not find 来判断找不到。
'''
class boring_out:
    K = 10
    line = 0
    ss = [] # sentences
    boring_words = []
    boring_ss = []
    def load_data(self):
        with open('simplifyweibo_4_moods.csv', encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                self.ss.append(line[1])

        self.boring_ss = [[] for i in range(len(self.ss))]

    def find_all(self, word):
        for s in self.ss:
            if s.find(word) != -1:
                print(s)

    def worth_output(self, i):
        if len(self.boring_ss[i]) == 0:
            return True
        return False

    def output(self):
        count = 0
        for line in range(self.line, len(self.ss)):
            worthy = self.worth_output(line)
            if not worthy:
                continue
            elif count >= self.K:
                return line
            else:
                print(self.ss[line])
                print()
                count += 1

    def process_new_boring_word(self, word):
        boring_index = len(self.boring_words)
        self.boring_words.append(word)

        for line in range(len(self.ss)):
            if self.ss[line].find(word) != -1:
                self.boring_ss[line].append(boring_index)

    def save_data(self):
        with open('boring_words.csv','w', newline='', encoding='utf-8') as ff:
            f = csv.writer(ff)
            for w in self.boring_words:
                f.writerow([w])
        with open('boring_ss.csv','w', newline='', encoding='utf-8') as ff:
            f = csv.writer(ff)
            for ws in self.boring_ss:
                f.writerow(ws)


    def __init__(self):
        self.load_data()
        while 1:
            line = self.output()
            word = input()
            if word == 'exit':
                self.save_data()
                return
            elif word == '1': # 切换下一屏
                self.line = line
            else:
                self.process_new_boring_word(word)

boring_out()