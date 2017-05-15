first_timing = '00:02:09,54 --> 00:02:12,56'
second_timing = '00:02:12,77 --> 00:02:16,23'

# Later than 1:50
rule1 = 60*1 + 50

def timingstr2second(timing):
    def str2second(t):
        h, m, s = t.strip().split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
    first_start, first_end = map(str.strip, timing.split('-->'))
    first_start, first_end = first_start.split(',')[0], first_end.split(',')[0]
    first_start, first_end = map(str2second, [first_start, first_end])
    return first_start, first_end

def func(first_timing, second_timing):
    first_start, first_end = timingstr2second(first_timing)
    second_start, second_end = timingstr2second(second_timing)
    print first_start, first_end
    print second_start, second_end

    if first_start < rule1:
        return False

    if not (0 <= second_start - first_end <= 2):
        return False

    if not (0 <= first_end - first_start <= 5):
        return False
    return True

print func(first_timing, second_timing)
