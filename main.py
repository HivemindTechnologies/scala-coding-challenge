import json_stream
import json
from sys import getsizeof
import datetime

# 5 KB file
review_data_path = r"C:\Users\ianms\repo\scala-coding-challenge\resources\video_game_reviews_example.json"
# 584 KB file
review_data_path_large = r"C:\Users\ianms\repo\scala-coding-challenge\resources\video_game_reviews_example_large.json"

# POST /amazon/best-rated HTTP/1.1
# Host: localhost:8080
# Content-Type: application/json
#
# {
#   "start": "01.01.2010", inclusive? exclusive?
#   "end": "31.12.2020",
#   "limit": 2,
#   "min_number_reviews": 2
# }

start = "01.01.2010"
end = "31.12.2020"


def read(line):
    return json.loads(line)

def time_filter(line):
    return read(line)['unixReviewTime'] >= date_str_to_unix_time(start) and read(line)['unixReviewTime'] <= date_str_to_unix_time(end)


def date_str_to_unix_time(date_string):
    return int(datetime.datetime.strptime(date_string, "%d.%m.%Y").timestamp())

if __name__ == '__main__':
    f = open(review_data_path)
    f_large = open(review_data_path_large)
    data = map(read, filter(time_filter, f))




    data_large = map(read, f_large)
    d = list(data)
    d_large = list(data_large)
    print('DATA LOAD TYPE ANALYSIS')
    print('Size of json loaded as list: ' + str(getsizeof(d)) + ' bytes')
    print('Size of mapped json: ' + str(getsizeof(data)) + ' bytes')
    print('Size of 100x larger json loaded as list: ' + str(getsizeof(d_large)) + ' bytes')
    print('Size of 100x larger mapped json: ' + str(getsizeof(data_large)) + ' bytes')
    print('Conclusion: Experimentally confirmed that using Python map() \n '
          'function can process json data without loading fully into memory, \n '
          'and is a functional programming syle. The map object size is independent \n'
          'of input file size, since map() can load items on demand.')



# NON FUNCTIONAL PROGRAMMING EXAMPLE
# with open(review_data_path) as f:
# ...     for line in f:
# ...         data = json.load(line)