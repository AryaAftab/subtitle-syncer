#!/usr/bin/env python
import argparse


# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=False, default='input.ass', type=str)
parser.add_argument('-o', '--output', required=False, default='output', type=str)
parser.add_argument('-d', '--delay', nargs='+', required=True, type=float)
parser.add_argument('-s', '--start_point', nargs='+', required=True, type=float)

arguments = parser.parse_args()



def find_dialogue(string):
    return 'Dialogue' in string.split(',')[0]


def find_start_end(string):
    Splited = string.split(',')
    return [float(s) for s in Splited[1].split(':')], [float(s) for s in Splited[2].split(':')]


def time_to_second(h_m_s):
    return (h_m_s[0] * 60 + h_m_s[1]) * 60 + h_m_s[2]


def second_to_time(second):
    second, Sec = divmod(second, 60)
    Hr, Min = divmod(second, 60)
    return [Hr, Min, round(Sec, 2)]


def to_format(h, m, s):
    return "%d:%02d:%02.2f" % (h, m, s)


def add_time(start, end, Delta):
    new_start = time_to_second(start) + time_to_second(Delta)
    new_end = time_to_second(end) + time_to_second(Delta)

    hr_start, min_start, sec_start = second_to_time(new_start)
    hr_end, min_end, sec_end = second_to_time(new_end)

    return to_format(hr_start, min_start, sec_start), to_format(hr_end, min_end, sec_end)


def correct_line(line, delay):
    start, end = find_start_end(line)
    new_start, new_end = add_time(start, end, delay)
    new_line = line.split(',')
    new_line[1] = new_start
    new_line[2] = new_end
    new_line = ",".join(new_line)

    return new_line


def start_point_correction(arguments):

    start_point = time_to_second(arguments.start_point)

    with open(arguments.input, 'r') as r:
        all_dialogue = []
        for line in r.readlines():
            if find_dialogue(line):
                start, _ = find_start_end(line)
                start = time_to_second(start)
                all_dialogue.append(start)

    for counter in range(len(all_dialogue) - 1):
        if all_dialogue[counter] > all_dialogue[counter+1]:
            all_dialogue = all_dialogue[:counter+1]
            break

    diff_dialogue = [abs(dialogue - start_point) for dialogue in all_dialogue]
    best_index = min(range(len(diff_dialogue)), key=lambda x : diff_dialogue[x])
    start_point = second_to_time(all_dialogue[best_index])

    return to_format(*start_point)





start_point = start_point_correction(arguments)


find_flag = False
with open(arguments.output + ".ass","w+") as w:
    with open(arguments.input, 'r') as r:
        for line in r.readlines():
            if (start_point in line) or find_flag:
                if find_dialogue(line):
                    new_line = correct_line(line, arguments.delay)
                    w.write(new_line)
                    find_flag = True
            else:
                w.write(line)