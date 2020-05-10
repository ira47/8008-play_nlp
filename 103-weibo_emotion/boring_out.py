import csv
'''
bug: 字符串find时候，找不到是-1，不能直接用if not find 来判断找不到。
'''
class boring_out:
    STRING_PER_LINE_TO_SHOW = 50
    TOTAL_LINE_TO_SHOW = 19

    line = 0
    ss = [] # sentences
    boring_words = []
    boring_ss = []
    good_words = []
    good_ss = []
    def load_data(self):
        with open('simplifyweibo_4_moods.csv', encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                self.ss.append(line[1])
        try:
            with open('boring_words.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    self.boring_words.append(line[0])
            with open('boring_ss.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    self.boring_ss.append(line)
            with open('good_words.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    self.good_words.append(line[0])
            with open('good_ss.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    self.good_ss.append(line)
        except IOError:
            self.boring_ss = [[] for i in range(len(self.ss))]
            self.good_ss = [[] for i in range(len(self.ss))]

        

    def find_all(self, word):
        for s in self.ss:
            if s.find(word) != -1:
                print(s)

    def worth_output(self, i):
        if len(self.boring_ss[i]) == 0 and len(self.good_ss[i]) == 0:
        # if len(self.boring_ss[i]) == 0:
            return True
        return False

    def my_output(self,msg_index,remain_line):
        msg = self.ss[msg_index]
        width = self.STRING_PER_LINE_TO_SHOW
        for start in range(0,len(msg),width):
            if remain_line <= 0:
                return -1 # 代表这一个语句没有输出完
            print(msg[start:start+width])
            remain_line -= 1

        return remain_line

    def output_msgs(self):
        line_remain = self.TOTAL_LINE_TO_SHOW
        for line in range(self.line, len(self.ss)):
            worthy = self.worth_output(line)
            if worthy:
                line_remain = self.my_output(line,line_remain)
                if line_remain == -1:
                    return line
                elif line_remain == 0:
                    return line+1 # 刚好用完，返回下一条

    def process_new_good_word(self, word):
        good_index = len(self.good_words)
        self.good_words.append(word)

        for line in range(len(self.ss)):
            if self.ss[line].find(word) != -1:
                self.good_ss[line].append(good_index)

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
        with open('good_words.csv','w', newline='', encoding='utf-8') as ff:
            f = csv.writer(ff)
            for w in self.good_words:
                f.writerow([w])
        with open('good_ss.csv','w', newline='', encoding='utf-8') as ff:
            f = csv.writer(ff)
            for ws in self.good_ss:
                f.writerow(ws)


    def __init__(self):
        self.load_data()
        while 1:
            command = ''

            line = self.output_msgs()
            while command == '':
                command = input()

            if command[0] == '0':
                self.save_data()
                return
            elif command[0] == '1': # 切换下一屏
                self.line = line
            elif command[0] == ' ':
                self.process_new_good_word(command[1:])
            else:
                self.process_new_boring_word(command)

boring_out()