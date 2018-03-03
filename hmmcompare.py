class Hmmcompare:
    def compare(self, filename1, filename2):
        file1 = open(filename1, 'r')  # your tagged file
        file2 = open(filename2, 'r')      # tagged dev data

        """
        file1 = open('test/results/hmmoutput_en.txt', 'r')  # your tagged file
        file2 = open('test/en_test_tagged.txt', 'r')      # tagged dev data
        """
        correct_count = 0
        incorrect_count = 0
        for sentence1, sentence2 in zip(file1, file2):
            i = 0
            words1 = sentence1.split()
            words2 = sentence2.split()
            for pair1, pair2 in zip(words1, words2):
                tag1 = pair1.rsplit("/",1)[1]
                tag2 = pair2.rsplit("/",1)[1]
                word1 = pair1.rsplit("/")[0]
                word2 = pair1.rsplit("/")[0]
                # print(word1+tag1)
                # print(word2+tag2)
                if tag1 == tag2:
                    correct_count += 1
                else:
                    incorrect_count += 1
        print(correct_count)
        print("Accuracy " + str(correct_count/(correct_count+incorrect_count)))


if __name__ == '__main__':
    file1 = 'hmmoutput.txt'
    file2 = 'data/zh_dev_tagged.txt'
    model = Hmmcompare()
    model.compare(file1, file1)
