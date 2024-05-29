import collections
import itertools
import time


def read_baskets():
    baskets_list = []
    with open("browsing-data.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        baskets_list.append(line.split())
    return baskets_list


def init_L1(baskets_list, min_support=100):
    counter_dict = collections.Counter()
    for basket in baskets_list:
        for item in basket:
            counter_dict[item] += 1
    L1 = {i: counter_dict[i] for i in counter_dict if counter_dict[i] >= min_support}
    return L1


def top_k_sorted_dict(input_dict, k):
    s_dict = list(sorted(input_dict.items(), key=lambda item: (-item[1], item[0])))
    return s_dict[:k]


def generateLK(baskets_list, k, support=100):
    counter_dict = collections.Counter()
    for basket in baskets_list:
        basket = sorted(basket)
        combs_iterator = itertools.combinations(basket, k)
        for combs in combs_iterator:
            counter_dict[combs] += 1
    Lk = {i: counter_dict[i] for i in counter_dict if counter_dict[i] >= support}
    # return top_k_sorted_dict(Lk, k)
    return Lk


def confidenceScore_k(Lk_1, Lk, k, k_top=5):
    temp = {}
    conf_score = collections.Counter()
    if k > 2:
        for x in Lk_1:
            Lk_1[tuple(sorted(x))] = Lk_1[x]
    for x in Lk:
        x = tuple(sorted(x))
        tuple_rotator = collections.deque(x)
        for _ in range(k):
            tpl = tuple(tuple_rotator)
            tpl = tuple(sorted(tpl[:-1])) + (tpl[-1],)
            temp[tpl] = Lk[x]
            tuple_rotator.rotate()
    for elem in temp:
        if k == 2:
            # conf_score[elem] = temp[elem] / float(Lk_1[:-1])
            conf_score[elem] = temp[elem] / float(Lk_1[elem[0]])
        else:
            # conf_score[elem] = temp[elem] / float(Lk_1[:-1])
            conf_score[elem] = temp[elem] / float(Lk_1[elem[:-1]])
    return top_k_sorted_dict(conf_score, k_top)

def output_result(cs2, cs3):
    with open("output.txt", "w") as file:
        file.write("OUTPUT A\n")
        for rule in cs2:
            file.write(str(rule[0][0]) + " -> " + str(rule[0][1]) + " : " + str(rule[1]) + "\n")
        file.write("\nOUTPUT B\n")
        for rule in cs3:
            file.write(str(rule[0][0]) + ", " + str(rule[0][1]) + " -> " + str(rule[0][2]) + " : " + str(rule[1]) + "\n")



def main():
    t1 = time.time()
    baskets = read_baskets()
    L1 = init_L1(baskets)
    L2 = generateLK(baskets, 2)
    L3 = generateLK(baskets, 3)
    cs2 = confidenceScore_k(L1, L2, 2)
    cs3 = confidenceScore_k(L2, L3, 3)
    output_result(cs2, cs3)
    t2 = time.time()
    print("Time taken: ", (t2 - t1) / 60, " minutes")


if __name__ == "__main__":
    main()
