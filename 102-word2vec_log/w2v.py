from pyhanlp import *


class word2vec_log:
    N_CLUSTER = 26
    N_SAMPLE = 400000
    READIN_FILE = 'HDFS_split'
    STRING_VECTOR_FILE = 'string_vector'
    WORD2VEC_FILE = 'word2vec'
    sample_belongings = [-1 for i in range(N_SAMPLE)]
    cluster_words = [[] for i in range(N_CLUSTER)]

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
                    w.write(str(vector[4:])+'\n')

                    line_count += 1
                    if line_count % 10000 == 0:
                        print(line_count)

        print('已输出可供word2vec训练的数据，以数组的形式保存。')

    def training_word2vec(self):
        # https://github.com/hankcs/HanLP/issues/1060 代码样例
        # WordVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')
        # DocVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        Word2VecTrainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')

        TRAIN_FILE_NAME = self.STRING_VECTOR_FILE
        MODEL_FILE_NAME = self.WORD2VEC_FILE

        trainerBuilder = Word2VecTrainer()
        word2vec = trainerBuilder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)
        # doc2vec = DocVectorModel(word2vec)
        # print(doc2vec)


w2v = word2vec_log()
w2v.generate_cluster_information()
w2v.get_string_vector_for_word2vec()
w2v.training_word2vec()