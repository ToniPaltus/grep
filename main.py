import sys
import argparse

# -invert -ignore_case -count -line_number -context=7 -before_context=8 -after_context=3 -request="Hello hell" -file="information.txt"
def parse_args(args):
    result = {}
    parser = argparse.ArgumentParser(description='This is a simple grep on Python')

    # adding arguments
    parser.add_argument(
        '-invert',
        default=False,
        action='store_true',
        dest='invert',
        help="Print all lines without a request."
    )
    parser.add_argument(
        '-ignore_case',
        default=False,
        action='store_true',
        dest='ignore_case',
        help='Ignore the request case.'
    )
    parser.add_argument(
        '-count',
        default=False,
        action='store_true',
        dest='count',
        help='Print number of lines satisfying the request.'
    )
    parser.add_argument(
        '-line_number',
        default=False,
        action='store_true',
        dest='line_number',
        help="Before the line, print it's number."
    )
    parser.add_argument(
        '-context',
        default=0,
        action='store',
        dest='context',
        type=int,
        help='Print N lines before and N lines after the request.'
    )
    parser.add_argument(
        '-before_context',
        default=0,
        action='store',
        dest='before_context',
        type=int,
        help='Print N lines before the request.'
    )
    parser.add_argument(
        '-after_context',
        default=0,
        action='store',
        dest='after_context',
        type=int,
        help='Print N lines after the request.'
    )
    parser.add_argument(
        '-request',
        default='',
        action='store',
        dest='REQUEST',
        type=str,
        required=True,
        help='Add your request.'
    )
    parser.add_argument(
        '-file',
        default='',
        action='store',
        dest='FILE',
        type=str,
        required=True,
        help='Add your file.'
    )

    # args
    args = parser.parse_args()
    # print('Args:', args, type(args), end='\n\n')

    # update dictionary
    words = ['invert', 'ignore_case', 'count', 'line_number', 'context',\
             'before_context', 'after_context', 'REQUEST', 'FILE']

    for word in words:
        work = 'args' + '.' + word
        # print('Work', work)
        # print(word, ':', eval(work), type(eval(work)))
        if str(eval(work))[0] == '-':
            print('Error!', word, '=', str(eval(work)), 'is negative...')
            flag = bool(input('--> Correct negative number to 0? (No --> SKIP): '))
            if flag:
                result.update({word: 0})
                continue
            else:
                exit(990)
        result.update({word: eval(work)})

    return result

def calculate_strings_in_file(file_name):
    with open(file_name, 'r') as file_in:
        return sum(1 for line in file_in)
def get_str_nums_context(str_count, str_with_request, context):
    result = []
    for item in str_with_request:
        start = item - context
        if start < 1:
            start = 1

        end = item + context
        if end > str_count:
            end = str_count

        for i in range(start, end + 1):
            if i == item:
                continue
            result.append(i)
    result = set(result)
    return list(result)
def get_str_nums_before_context(str_with_request, before_context):
    result = []
    for item in str_with_request:
        start = item - before_context
        if start < 1:
            start = 1
        end = item - 1
        for i in range(start, end+1):
            result.append(i)
    result = set(result)
    return list(result)
def get_str_nums_after_context(str_count, str_with_request, after_context):
    result = []
    for item in str_with_request:
        start = item + 1
        if start > str_count:
            start = str_count
        end = item + after_context
        if end > str_count:
            end = str_count
        for i in range(start, end+1):
            result.append(i)
    result = set(result)
    return list(result)

def grep(params):
    invert = params['invert']
    ignore_case = params['ignore_case']
    count = params['count']
    line_number = params['line_number']
    context = params['context']
    before_context = params['before_context']
    after_context = params['after_context']
    request = params['REQUEST']
    file_name = params['FILE']

    str_count = calculate_strings_in_file(file_name)
    print('str_count', str_count)

    good_count = 0
    line_counter = 1
    str_with_request = []

    # not context
    with open(file_name, 'r') as file_in:
        for line in file_in:
            if ignore_case:
                request = str(request).lower()
                work_line = line[:].lower().split(' ')

                if invert:
                    if request not in work_line:
                        good_count += 1
                        if line_number:
                            str_with_request.append(line_counter)
                            print(line_counter, '. ', line, sep='', end='')
                        else:
                            print(line, end='')
                else:
                    if request in work_line:
                        good_count += 1
                        if line_number:
                            str_with_request.append(line_counter)
                            print(line_counter, '. ', line, sep='', end='')
                        else:
                            print(line, end='')
            else:
                if invert:
                    if request not in line.split(' '):
                        good_count += 1
                        if line_number:
                            str_with_request.append(line_counter)
                            print(line_counter, '. ', line, sep='', end='')
                        else:
                            print(line, end='')
                else:
                    if request in line.split(' '):
                        good_count += 1
                        if line_number:
                            str_with_request.append(line_counter)
                            print(line_counter, '. ', line, sep='', end='')
                        else:
                            print(line, end='')
            line_counter += 1

        if count:
            print('\nStrings with request:', good_count)
        print('str_with_request', str_with_request)

    # context
    str_context = get_str_nums_context(str_count, str_with_request, context)
    print('str_context', str_context)

    str_before_context = get_str_nums_before_context(str_with_request, before_context)
    print('str_before_context', str_before_context)

    str_after_context = get_str_nums_after_context(str_count, str_with_request, after_context)
    print('str_after_context', str_after_context)

    with open(file_name, 'r') as file_in:
        line_counter = 1
        for line in file_in:
            # context
            if context != 0 and before_context == 0 and after_context == 0:
                if line_counter in str_context:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # before_context
            elif context == 0 and before_context != 0 and after_context == 0:
                if line_counter in str_before_context:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # after_context
            elif context == 0 and before_context == 0 and after_context != 0:
                if line_counter in str_after_context:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # context and before_context
            elif context != 0 and before_context != 0 and after_context == 0:
                general = sorted(list(set(str_context + str_before_context)))
                if line_counter in general:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # context and after_context
            elif context != 0 and before_context == 0 and after_context != 0:
                general = sorted(list(set(str_context + str_after_context)))
                if line_counter in general:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # before_context and after_context
            elif context == 0 and before_context != 0 and after_context != 0:
                general = sorted(list(set(str_before_context + str_after_context)))
                if line_counter in general:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            # before_context and context and after_context
            elif context != 0 and before_context != 0 and after_context != 0:
                general = sorted(list(set(str_before_context + str_context + str_after_context)))
                if line_counter in general:
                    if line_number:
                        print(line_counter, '. ', line, sep='', end='')
                    else:
                        print(line, end='')
            else:
                break
            line_counter += 1

def main():
    params = parse_args(sys.argv[1:0])
    print('Params:', params, type(params))
    grep(params)

if __name__ == '__main__':
    main()