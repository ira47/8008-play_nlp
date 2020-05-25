class zimu_buffer:
    BUFFER_SIZE = 100
    CLAUSE_LENGTH = 2
    GOOD_ZIMU_FILE_NAME = '三好乱弹 – 那些濒临破产的年轻人II.srt'
    BAD_ZIMU_FILE_NAME = 'CHS_三好乱弹+–+那些濒临破产的年轻人II.srt'

    zimu_bad_old = []
    zimu_bad = []
    zimu_good = []
    time = []

    buffer_length_good = 0
    buffer_length_bad = 0
    buffer_good = []
    buffer_bad = []
    string_good = ''
    string_bad = ''

    line_to_read_good = 0
    line_to_read_bad = 0

    def read_file(self, file_name):
        zimu = []
        time = []
        with open(file_name, 'r', encoding='utf-8') as f:
            for idx, value in enumerate(f.readlines()):
                value = value.strip()
                if idx % 4 == 1:
                    time.append(value)
                elif idx % 4 == 2:
                    zimu.append(value)
        return zimu, time

    def update_buffer(self):
        at_end_good = self.line_to_read_good >= len(self.zimu_good)
        at_end_bad = self.line_to_read_bad >= len(self.zimu_bad)
        while not at_end_good and self.buffer_length_good < self.BUFFER_SIZE:
            string = self.zimu_good[self.line_to_read_good]
            self.string_good += string
            self.buffer_length_good += len(string)
            for index,value in enumerate(string):
                self.buffer_good.append([self.line_to_read_good,index])
            self.line_to_read_good += 1
        while not at_end_bad and self.buffer_length_bad < self.BUFFER_SIZE:
            string = self.zimu_bad[self.line_to_read_bad]
            self.string_bad += string
            self.buffer_length_bad += len(string)
            for index,value in enumerate(string):
                self.buffer_bad.append([self.line_to_read_bad,index])
            self.line_to_read_bad += 1
        return at_end_bad and at_end_good # 返回是否到字幕的末端

    def update_words(self,length):
        line_start = self.buffer_bad[0][0]
        line_end = self.buffer_bad[length-1][0]+1
        lists = []
        for line in range(line_start,line_end):
            lists.append(list(self.zimu_bad[line]))
        for index,word in enumerate(self.string_good[:length]):
            line = self.buffer_bad[index][0]-line_start
            line_index = self.buffer_bad[index][1]
            lists[line][line_index] = word
        for line in range(line_start,line_end):
            self.zimu_bad[line] = ''.join(lists[line-line_start])

    def main(self):
        while 1:
            end = self.update_buffer()
            print('bad',self.string_bad)
            print('good',self.string_good)
            find = False
            for index_bad in range(self.buffer_length_bad-self.CLAUSE_LENGTH+1):
                clause = self.string_good[index_bad:index_bad+self.CLAUSE_LENGTH]
                count = self.string_good.count(clause)
                if count == 0 or count >= 2:
                    continue
                index_good = self.string_good.index(clause)
                if index_bad == index_good:
                    self.update_words(index_good)
                    find = True
                delete_length_good = index_good + self.CLAUSE_LENGTH
                delete_length_bad = index_bad + self.CLAUSE_LENGTH
                self.string_good = self.string_good[delete_length_good:]
                self.string_bad = self.string_bad[delete_length_bad:]
                self.buffer_good = self.buffer_good[delete_length_good:]
                self.buffer_bad = self.buffer_bad[delete_length_bad:]
                self.buffer_length_good -= delete_length_good
                self.buffer_length_bad -= delete_length_bad
                break
            if not find:
                if end:
                    return
                else:
                    print(self.string_good)
                    print(self.string_bad)
                    print("error")
                    exit(1)

    def __init__(self):
        self.zimu_good,_ = self.read_file(self.GOOD_ZIMU_FILE_NAME)
        self.zimu_bad_old,_ = self.read_file(self.BAD_ZIMU_FILE_NAME)
        self.zimu_bad,self.time = self.read_file(self.BAD_ZIMU_FILE_NAME)

        self.main()
        for old,new in zip(self.zimu_bad_old,self.zimu_bad):
            if old != new:
                print(old,new)


zimu_buffer()