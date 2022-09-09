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


def start_end(string):
    Splited = string.split(',')
    return [float(s) for s in Splited[1].split(':')], [float(s) for s in Splited[2].split(':')]


def add(start, end, Delta):
    new_start = (start[0] * 60 + start[1]) * 60 + start[2] + (Delta[0] * 60 + Delta[1]) * 60 + Delta[2]
    new_end = (end[0] * 60 + end[1]) * 60 + end[2] + (Delta[0] * 60 + Delta[1]) * 60 + Delta[2]

    new_start, sec_start = divmod(new_start, 60)
    new_end, sec_end = divmod(new_end, 60)

    hr_start, min_start = divmod(new_start, 60)
    hr_end, min_end = divmod(new_end, 60)

    return "%d:%02d:%02.2f" % (hr_start, min_start, sec_start), "%d:%02d:%02.2f" % (hr_end, min_end, sec_end)



h, m, s = arguments.start_point
h, m, s = int(h), int(m), int(s)
start_point = f"{h%10}:{m:02d}:{s:02d}"


flag = False
with open(arguments.output + ".ass","w+") as w:
    with open(arguments.input, 'r') as r:
        for line in r.readlines():
            if (start_point in line) or flag:
                if find_dialogue(line):
                    start, end = start_end(line)
                    new_start, new_end = add(start, end, arguments.delay)
                    new_line = line.split(',')
                    new_line[1] = new_start
                    new_line[2] = new_end
                    new_line = ",".join(new_line)
                    w.write(new_line)
                    flag = True
            else:
                w.write(line)