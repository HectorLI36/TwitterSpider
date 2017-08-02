import re
from collections import Counter


def read_file():
    total = []
    lines = open('tweepy_result_washed_already.csv', 'r').readlines()
    for line in lines:
        if line != '\n' and len(line.split(',')) >= 3:
            tweet_content_raw = line.split(',')[0]
            neat = re.sub(r'http.*|[\,\.\:\;\1]|[\r\n,\n]', '', tweet_content_raw)
            total.extend(neat.split(' '))
    with open('report_final.txt', 'w') as report:
        c = Counter(total)
        for tmp in c.most_common():
            print tmp
            report.write(str(tmp) + '\n')
    pass


def pre_process():
    with open('washed_tweepy.csv', 'w+') as new:
        lines = open('tweepy_result_2.csv', 'rb').read()
        neat = re.sub(r'\r|\n', '', lines)
        new.write(neat)


read_file()