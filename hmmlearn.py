import time
import json
import sys
from pprint import pprint
import math


class Hmmlearn:

    def parse(self, filename):

        file = open(filename, 'r')
        data = file.read()
        lines = data.split('\n')
        emission_tag_count = {}
        transition_tag_count = {}
        word_tag = {}
        tag_tag = {}
        unique_tags = []
        for line in lines:
            line_count = len(lines)
            if line is not "":  # to avoid tagging empty sentences
                word_tags = line.split(" ")
                count = len(word_tags)
                first_tag = 'START'
                if first_tag not in unique_tags:
                    unique_tags.append(first_tag)  # to add start tag
                i = 0
                for wt in word_tags:
                    terms = wt.rsplit('/', 1)
                    word = terms[0]
                    tag = terms[1]
                    i += 1
                    # adding tag to unique tags list
                    if tag not in unique_tags:
                        unique_tags.append(tag)
                    # count the number of occurrences of a word as a tag
                    if word in word_tag:
                        if tag in word_tag[word]:
                            word_tag[word][tag] += 1
                        else:
                            word_tag[word][tag] = 1
                    else:
                        word_tag[word] = {}
                        word_tag[word][tag] = 1
                    # count the number of occurrences of tag1 followed by tag2
                    if first_tag in tag_tag:
                        if tag in tag_tag[first_tag]:
                            tag_tag[first_tag][tag] += 1
                        else:
                            tag_tag[first_tag][tag] = 1
                    else:
                        tag_tag[first_tag] = {}
                        tag_tag[first_tag][tag] = 1
                    # count the number of occurrences of a tag in full data set for emission and transition(omits last tags)
                    if tag not in emission_tag_count:
                        emission_tag_count[tag] = 1
                        if i != count:
                            if tag not in transition_tag_count:
                                transition_tag_count[tag] = 1
                            else:
                                transition_tag_count[tag] += 1
                    else:
                        emission_tag_count[tag] += 1
                        if i != count:
                            # print(emission_tag_count)
                            if tag in transition_tag_count:
                                transition_tag_count[tag] += 1
                            else:
                                transition_tag_count[tag] = 1
                    first_tag = tag
                tag = 'STOP'
                if tag not in unique_tags:
                    unique_tags.append(tag)  # to append
                transition_tag_count['START'] = line_count
                if first_tag in tag_tag:
                    if tag in tag_tag[first_tag]:
                        tag_tag[first_tag][tag] += 1
                    else:
                        tag_tag[first_tag][tag] = 1

        return transition_tag_count, emission_tag_count, word_tag, tag_tag, unique_tags

    def smoothing(self, tag_tag, transition_tag_count, unique_tags):
        unique_tag_length = len(unique_tags)

        for tag1 in unique_tags:
            if tag1 != 'STOP':  # because stop is the end point
                if tag1 in tag_tag:  # transitions from tag1 already exist
                    for tag2 in unique_tags:
                        if tag2 == 'START':
                            continue
                        if tag1 == 'START' and tag2 == 'STOP':
                            continue
                        if tag2 in tag_tag[tag1]:
                            tag_tag[tag1][tag2] += 1
                        else:
                            tag_tag[tag1][tag2] = 1
                else:
                    tag_tag[tag1] = {}
                    transition_tag_count[tag1] = 0
                    for tag2 in unique_tags:
                        if tag2 == 'START':
                            continue
                        if tag1 == 'START' and tag2 == 'STOP':
                            continue
                        tag_tag[tag1][tag2] = 1
                transition_tag_count[tag1] += 5*unique_tag_length

        return tag_tag, transition_tag_count

    def model_transition(self, tag_tag, transition_tag_count):
        tag_tag_probability = {}
        for tag1 in tag_tag:
            tag_tag_probability[tag1] = {}
            for tag2 in tag_tag[tag1]:
                # tag_tag_probability[tag1][tag2] = [tag_tag[tag1][tag2]/transition_tag_count[tag1], tag_tag[tag1][tag2]]
                tag_tag_probability[tag1][tag2] = [math.log(tag_tag[tag1][tag2]) - math.log(sum(tag_tag[tag1].values())), tag_tag[tag1][tag2]]
            tag_tag_probability[tag1]["transition_count"] = sum(tag_tag[tag1].values())

        return tag_tag_probability

    def model_emission(self, emission_tag_count, word_tag):
        word_tag_probability = {}
        for word in word_tag:
            word_tag_probability[word] = {}
            count = 0
            for tag in word_tag[word]:
                # word_tag_probability[word][tag] = [word_tag[word][tag]/emission_tag_count[tag], word_tag[word][tag]]
                word_tag_probability[word][tag] = [math.log(word_tag[word][tag]) - math.log(emission_tag_count[tag]), word_tag[word][tag]]
                count += word_tag[word][tag]
            word_tag_probability[word]["total_count"] = count
        return word_tag_probability

    def file_write(self, filename, transition_prob, emission_prob, unique_tags):
        super_dict = {}
        super_dict['transition'] = transition_prob
        super_dict['emission'] = emission_prob
        super_dict['unique_tags'] = unique_tags
        with open(filename, 'w') as outfile:
            json.dump(super_dict, outfile, indent=4)
        return


# start time
t1 = time.time()
if __name__ == "__main__":

    model = Hmmlearn()
    filename1 = sys.argv[1]
    # filename1 = "data/zh_train_tagged.txt"
    filename2 = "hmmmodel.txt"
    filename3 = "hmmmodel.json"
    """
    filename1 = "test/en_train_dev_tagged.txt"
    filename2 = "test/results/hmmmodel_en.txt"
    filename3 = "test/results/hmmmodel_en.json"
    """
    transition_tag, emission_tag, word_tag_dict, tag_tag_dict, unique_tag_list = model.parse(filename1)

    tag_tag_counts, transition_tag_counts = model.smoothing(tag_tag_dict, transition_tag, unique_tag_list)
    t_t_prob = model.model_transition(tag_tag_counts, transition_tag_counts)
    w_t_prob = model.model_emission(emission_tag, word_tag_dict)
    model.file_write(filename3, t_t_prob, w_t_prob, unique_tag_list)
    # to count the number of transitions recorded
    count = 0
    for t in t_t_prob:
        k = len(t_t_prob[t].keys())
        count += k
    print(count)

t2 = time.time()
print("Time: "+str(t2 - t1))
