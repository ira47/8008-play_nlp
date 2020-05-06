from pyhanlp import *



class word2vec_log:
    N_CLUSTER = 12
    N_SAMPLE = 1000
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
        with open('HDFS_split_1000', 'r') as r:
            with open('string_vector','w') as w:
                for line in r.readlines():
                    vector = line.strip().split(' ')
                    cluster_id = self.sample_belongings[line_count]
                    words_to_delete = self.cluster_words[cluster_id]
                    for word in words_to_delete:
                        vector.remove(word)
                    w.write(str(vector[4:])+'\n')

                    line_count += 1
        print('已输出可供word2vec训练的数据，以数组的形式保存。')

w2v = word2vec_log()
w2v.generate_cluster_information()
w2v.get_string_vector_for_word2vec()