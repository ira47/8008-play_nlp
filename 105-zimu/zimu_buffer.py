class zimu_buffer:
    BUFFER_SIZE = 100
    CLAUSE_LENGTH = 4
    SELECT_START_INDEX = 218
    GOOD_ZIMU_FILE_NAME = '三好乱弹 – 那些濒临破产的年轻人II.srt'
    BAD_ZIMU_FILE_NAME = 'CHS_三好乱弹+–+那些濒临破产的年轻人II.srt'
    WRITE_FILE_NAME = '那些濒临破产的年轻人II.srt'

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
        while not self.line_to_read_good >= len(self.zimu_good) \
                and self.buffer_length_good < self.BUFFER_SIZE:
            string = self.zimu_good[self.line_to_read_good]
            self.string_good += string
            self.buffer_length_good += len(string)
            for index, value in enumerate(string):
                self.buffer_good.append([self.line_to_read_good, index])
            self.line_to_read_good += 1
        while not self.line_to_read_bad >= len(self.zimu_bad) \
                and self.buffer_length_bad < self.BUFFER_SIZE:
            string = self.zimu_bad[self.line_to_read_bad]
            self.string_bad += string
            self.buffer_length_bad += len(string)
            for index, value in enumerate(string):
                self.buffer_bad.append([self.line_to_read_bad, index])
            self.line_to_read_bad += 1
        return self.line_to_read_good >= len(self.zimu_good) \
               and self.line_to_read_bad >= len(self.zimu_bad)  # 返回是否到字幕的末端

    def clac_copy_start_and_length(self, index_bad, index_good):
        if index_bad == index_good:
            return True, index_bad, 0, 0
        flag_left = flag_right = False
        for i in range(index_bad):
            flag_left = flag_right = False
            word_right = self.string_bad[i]
            word_left = self.string_bad[index_bad - i - 1]

            count_left = self.string_good[:index_good].count(word_left)
            if count_left == 1:
                j = self.string_good[:index_good].index(word_left)
                if i == j:
                    flag_left = True

            count_right = self.string_good[:index_good].count(word_right)
            if count_right == 1:
                j = self.string_good[:index_good].index(word_right)
                if (index_bad - i) == (index_good - j):
                    flag_right = True

            if flag_left or flag_right:
                break
        if flag_left:
            return True, i, 0, 0
        elif flag_right:
            return True, index_bad - i - 1, i + 1, j + 1
        else:
            return False, 0, 0, 0

    def update_words(self, length, bad_start, good_start):
        line_start = self.buffer_bad[bad_start][0]
        line_end = self.buffer_bad[bad_start + length - 1][0] + 1
        lists = []
        for line in range(line_start, line_end):
            lists.append(list(self.zimu_bad[line]))
        for index, word in enumerate(self.string_good[good_start:good_start + length]):
            line = self.buffer_bad[bad_start + index][0] - line_start
            line_index = self.buffer_bad[bad_start + index][1]
            lists[line][line_index] = word
        for line in range(line_start, line_end):
            self.zimu_bad[line] = ''.join(lists[line - line_start])
        return True

    def main(self):
        while 1:
            end = self.update_buffer()
            find = False
            for index_bad in range(self.buffer_length_bad - self.CLAUSE_LENGTH + 1):
                clause = self.string_bad[index_bad:index_bad + self.CLAUSE_LENGTH]
                count = self.string_good.count(clause)
                if count == 0 or count >= 2:
                    continue
                find = True
                index_good = self.string_good.index(clause)
                need_update, length, bad_start, good_start = \
                    self.clac_copy_start_and_length(index_bad, index_good)
                if need_update:
                    self.update_words(length, bad_start, good_start)

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

    def print_compare(self, line):
        old = self.zimu_bad_old[line]
        new = self.zimu_bad[line]
        if line - 1 >= 0:
            old_prefix = self.zimu_bad_old[line - 1]
            new_prefix = self.zimu_bad[line - 1]
        else:
            old_prefix = ''
            new_prefix = ''
        if line + 1 < len(self.zimu_bad):
            old_suffix = self.zimu_bad_old[line + 1]
            new_suffix = self.zimu_bad[line + 1]
        else:
            old_suffix = ''
            new_suffix = ''

        old_output = '1 ' + old_prefix
        new_output = '2 ' + new_prefix

        equal = True
        for s1, s2 in zip(old, new):
            if (s1 == s2 and not equal) or (s1 != s2 and equal):
                equal = not equal
                old_output += '|'
                new_output += '|'
            old_output += s1
            new_output += s2
        if not equal:
            old_output += '|'
            new_output += '|'
        old_output += old_suffix
        new_output += new_suffix
        print(old_output)
        print(new_output)

    def select_and_save(self):
        with open(self.WRITE_FILE_NAME, 'a', encoding='utf-8') as f:
            for line in range(self.SELECT_START_INDEX, len(self.zimu_bad)):
                old = self.zimu_bad_old[line]
                new = self.zimu_bad[line]
                use = new
                if old != new:
                    self.print_compare(line)
                    command = ''
                    while command == '' or command[0] not in ['0', '1', '2']:
                        command = input()
                    if command[0] == '1':
                        use = old
                    elif command[0] == '0':
                        print(line)
                        return
                index = str(line)
                time = self.time[line]
                output = index + '\n' + time + '\n' + use + '\n' + '\n'
                f.write(output)

    def __init__(self):
        self.zimu_good, _ = self.read_file(self.GOOD_ZIMU_FILE_NAME)
        self.zimu_bad_old, _ = self.read_file(self.BAD_ZIMU_FILE_NAME)
        self.zimu_bad, self.time = self.read_file(self.BAD_ZIMU_FILE_NAME)

        self.main()

        self.select_and_save()


zimu_buffer()
