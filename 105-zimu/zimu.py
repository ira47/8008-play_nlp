class zimu:
    WINDOW_SIZE = 5
    GOOD_ZIMU_FILE_NAME = '三好乱弹 – 那些濒临破产的年轻人II.srt'
    BAD_ZIMU_FILE_NAME = 'CHS_三好乱弹+–+那些濒临破产的年轻人II.srt'

    good_zimu = []
    bad_zimu = []
    bad_time = []
    bad_line = 0
    scan_start_line = 0

    def read_file(self, file_name):
        zimu = [] # sentences
        time = []
        with open(file_name, 'r', encoding='utf-8') as f:
            for idx,value in enumerate(f.readlines()):
                value = value.strip()
                if idx % 4 == 1:
                    time.append(value)
                elif idx % 4 == 2:
                    zimu.append(value)
        return zimu,time

    def search(self, word):
        find_list = []
        for additional_line in range(self.WINDOW_SIZE):
            line = self.scan_start_line + additional_line
            string_start_index = 0
            while 1:
                try:
                    index = self.good_zimu[line].index(word,string_start_index)
                    find_list.append([line,index])
                    string_start_index = index + 1
                except:
                    break
        return find_list

    def strategy_first_same_length(self):
        word = self.bad_zimu[self.bad_line][0]
        search_results = self.search(word)
        for [good_line, index] in search_results:
            if index == 0:
                bad_line_length = len(self.bad_zimu[self.bad_line])
                good_line_length = len(self.good_zimu[good_line])
                same_length = good_line_length == bad_line_length
                if same_length:
                    good_sentence = self.good_zimu[good_line]
                    return good_line, good_sentence
        return -1, ''

    def update_line(self, sentence):
        old_sentence = self.bad_zimu[self.bad_line]
        self.bad_zimu[self.bad_line] = sentence
        print(old_sentence, sentence)

    def __init__(self):
        self.good_zimu,_ = self.read_file(self.GOOD_ZIMU_FILE_NAME)
        self.bad_zimu,self.bad_time = self.read_file(self.BAD_ZIMU_FILE_NAME)

        # for i in range(5):
        #     print(self.good_zimu[i],self.bad_zimu[i],self.bad_time[i])

        for bad_line in range(len(self.bad_zimu)):
            self.bad_line = bad_line
            good_line, good_sentence = self.strategy_first_same_length()
            if good_line != -1:
                self.scan_start_line = good_line
                self.update_line(good_sentence)

zimu_processing()