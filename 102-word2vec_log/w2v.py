from pyhanlp import *


class word2vec_log:
    N_CLUSTER = 12
    N_SAMPLE = 1000
    VECTOR_DIMENSION = 10
    READIN_FILE = 'HDFS_split'
    STRING_VECTOR_FILE = 'string_vector'
    WORD2VEC_FILE = 'word2vec'
    SENTENCE_VECTOR_FILE = 'sentence_vec'

    sample_belongings = [-1 for i in range(N_SAMPLE)]
    cluster_words = [[] for i in range(N_CLUSTER)]
    word_vector = {}

    def generate_cluster_information(self):
        for cluster in range(self.N_CLUSTER):
            with open('clusters/'+str(cluster+1),'r') as f:
                line1 = f.readline()
                self.cluster_words[cluster] = line1.strip().split(' ')

                line2 = f.readline()
                cluster_members = line2.strip().split(' ')
                for member in cluster_members:
                    self.sample_belongings[int(member)] = cluster
        print('已生成cluster信息')
        # print(self.sample_belongings[0])
        # print(self.sample_belongings[1])
        # print(self.sample_belongings[2])
        # print(self.cluster_words[0])
        # print(self.cluster_words[1])
        # print(self.cluster_words[2])


    def get_string_vector_for_word2vec(self):
        # 加载
        line_count = 0
        with open(self.READIN_FILE, 'r') as r:
            with open(self.STRING_VECTOR_FILE, 'w') as w:
                for line in r.readlines():
                    vector = line.strip().split(' ')
                    cluster_id = self.sample_belongings[line_count]
                    words_to_delete = self.cluster_words[cluster_id]
                    for word in words_to_delete:
                        vector.remove(word)
                    vector_to_write = vector[:3]+vector[4:]
                    str_to_write = ' '.join(str(i) for i in vector_to_write)
                    w.write(str_to_write+'\n')

                    line_count += 1
                    if line_count % 10000 == 0:
                        print(line_count)

        print('已输出可供word2vec训练的数据，以数组的形式保存。')

    def training_word2vec(self):
        # https://github.com/hankcs/HanLP/issues/1060 代码样例
        # DocVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        Word2VecTrainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')
        # 通过搜索com.hankcs.hanlp.mining.word2vec.Word2VecTrainer 可获得文档信息

        TRAIN_FILE_NAME = self.STRING_VECTOR_FILE
        MODEL_FILE_NAME = self.WORD2VEC_FILE

        trainerBuilder = Word2VecTrainer()
        trainerBuilder.setLayerSize(self.VECTOR_DIMENSION)
        word2vec = trainerBuilder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)

    def load_word_vector(self):
        with open(self.WORD2VEC_FILE, 'r') as r:
            for line in r.readlines():
                list_line = line.split(' ')
                value = list(map(float,list_line[1:]))
                key = list_line[0]
                self.word_vector[key] = value

    def calc_sentence_vector(self,sentence):
        words = sentence.split(' ')
        old_vector = [0.0 for i in range(self.VECTOR_DIMENSION)]
        for word in words:
            # print(word)
            if word not in self.word_vector.keys():
                another_vector = [0.0 for i in range(self.VECTOR_DIMENSION)]
            else:
                another_vector = self.word_vector[word]
            new_vector = []
            for i,j in zip(old_vector,another_vector):
                new_vector.append(i+j)
            old_vector = new_vector

        word_count = len(words)
        for idx,value in enumerate(old_vector):
            old_vector[idx] = value/word_count
        vector_str = list(map(str, old_vector))
        output = ','.join(vector_str)
        return output

    def sentence_vector_main(self):
        # https://blog.csdn.net/asialee_bird/article/details/100124565
        with open(self.STRING_VECTOR_FILE, 'r') as r:
            with open(self.SENTENCE_VECTOR_FILE, 'w') as w:
                for line in r.readlines():
                    sentence_vector = self.calc_sentence_vector(line)
                    w.write(sentence_vector+'\n')

w2v = word2vec_log()
# w2v.generate_cluster_information()
# w2v.get_string_vector_for_word2vec()
# w2v.training_word2vec()
w2v.load_word_vector()
w2v.sentence_vector_main()