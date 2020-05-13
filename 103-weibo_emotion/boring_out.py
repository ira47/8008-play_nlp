import csv
'''
bug: 字符串find时候，找不到是-1，不能直接用if not find 来判断找不到。
'''
class boring_out:
    STRING_PER_LINE_TO_SHOW = 50
    TOTAL_LINE_TO_SHOW = 19

    line = 105
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
                    int_line = list(map(int, line))
                    self.boring_ss.append(int_line)
            with open('good_words.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    self.good_words.append(line[0])
            with open('good_ss.csv', encoding='utf-8') as f:
                lines = csv.reader(f)
                for line in lines:
                    int_line = list(map(int, line))
                    self.good_ss.append(int_line)

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
        print('已保存所有数据。')

    def show_boring_words(self):
        for index,word in enumerate(self.boring_words):
            print(index,word)

    def show_good_words(self):
        for index,word in enumerate(self.good_words):
            print(index,word)

    def delete_boring_word(self,index):
        self.boring_words.pop(index)
        for s_idx,s in enumerate(self.boring_ss):
            wrong_index = -1
            for i_idx,i in enumerate(s):
                if i > index:
                    self.boring_ss[s_idx][i_idx] -= 1
                elif i == index:
                    wrong_index = i_idx
            if wrong_index != -1:
                self.boring_ss[s_idx].pop(wrong_index)

    def delete_good_word(self,index):
        self.good_words.pop(index)
        for s_idx,s in enumerate(self.good_ss):
            wrong_index = -1
            for i_idx,i in enumerate(s):
                if i > index:
                    self.boring_ss[s_idx][i_idx] -= 1
                elif i == index:
                    wrong_index = i_idx
            if wrong_index != -1:
                self.good_ss[s_idx].pop(wrong_index)

    def __init__(self):
        self.load_data()
        need_output = True
        while 1:
            command = ''
            if need_output:
                line = self.output_msgs()
            while command == '':
                command = input()

            if len(command) == 1:
                if command[0] == '0':
                    self.save_data()
                    print(self.line)
                    return
                elif command[0] == ' ': # 切换下一屏
                    self.line = line
                elif command[0] == '`':
                    need_output = not need_output
                elif command[0] == '3':
                    self.show_boring_words()
                elif command[0] == '4':
                    self.show_good_words()
                elif command[0] == '5':
                    self.save_data()

            elif command[0] == '1':
                self.process_new_boring_word(command[1:])
            elif command[0] == '2':
                self.process_new_good_word(command[1:])
            elif command[0] == '3':
                if len(command) > 2 and command[1] == ' ':
                    word_idx = int(command[1:])
                    word = self.boring_words[word_idx]
                    self.delete_boring_word(word_idx)
                    output = '已经删除序号为{}的boring词，名称为：{}'
                    print(output.format(word_idx,word))
            elif command[0] == '4':
                if len(command) > 2 and command[1] == ' ':
                    word_idx = int(command[2:])
                    word = self.good_words[word_idx]
                    self.delete_good_word(word_idx)
                    output = '已经删除序号为{}的good词，名称为：{}'
                    print(output.format(word_idx,word))


boring_out()