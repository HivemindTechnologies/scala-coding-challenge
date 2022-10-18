import json_stream
import json
from sys import getsizeof
import datetime
from functools import reduce


# 5 KB file
review_data_path = r"C:\Users\ianms\repo\scala-coding-challenge\resources\video_game_reviews_example.json"
# 584 KB file
review_data_path_large = r"C:\Users\ianms\repo\scala-coding-challenge\resources\amazon-reviews.json"

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
min_num_reviews = 2
limit = 2


def read(string):
    """Converts a line from a new-line delimited json, which is read as a string, to a json object"""
    return json.loads(string)

def time_filter(line):
    """Excludes data outside of the 'start' and 'end' date range"""
    return line['unixReviewTime'] >= date_str_to_unix_time(start) and line['unixReviewTime'] <= date_str_to_unix_time(end)

def date_str_to_unix_time(date_string):
    return int(datetime.datetime.strptime(date_string, "%d.%m.%Y").timestamp())

def review_count_filter(static_line):

    def line_scanner(count, moving_line): # potentially add functionality that breaks function as soon as first True occurs
        if type(count) == bool:
            return True
        if count == min_num_reviews:
            return True
        if moving_line['asin'] == static_line['asin']:
            if count + 1 == min_num_reviews:
                return True
            return count + 1
        else:
            return count

    if type(reduce(line_scanner, get_time_filtered_data(), 0)) == int:
        return False
    else:
        return True



def calculate_rating_sum(static_line):

    def identity_tester(moving_line):
        if moving_line['asin'] == static_line['asin']:
            return True
        else:
            return False

    def sum_overall(a, b):
        return a['overall'] + b['overall']

    return {static_line['asin']: reduce(sum_overall, filter(identity_tester, get_time_and_review_count_filtered_data()))}

def calculate_rating_avgs(static_line):

    def identity_tester(moving_line):
        if moving_line['asin'] == static_line['asin']:
            return True
        else:
            return False

    def count_overall(a, b):
        return a + 1
    
    def sum_overall(a, b):
        return a + b['overall']
    
    return {static_line['asin']: reduce(sum_overall, filter(identity_tester, get_time_and_review_count_filtered_data()), 0) / reduce(count_overall, filter(identity_tester, get_time_and_review_count_filtered_data()), 0)}

def find_top_rated_avgs(top_avgs_list, static_line):

    def compare_avgs(highest_avg, current_avg):
        if highest_avg in top_avgs_list: # exclude top avgs already found
            return current_avg
        if list(current_avg.values())[0] > list(highest_avg.values())[0] and current_avg not in top_avgs_list:
            return current_avg
        else:
            return highest_avg


    if len(top_avgs_list) == limit:
        return top_avgs_list
    else:
        return top_avgs_list + [reduce(compare_avgs, get_rating_avgs())]

    # return {asin, avg_desc}

def get_time_filtered_data():
    f = open(review_data_path)
    data = map(read, f)
    return map(pass_line, filter(time_filter, data)) # time filtered data

def get_time_and_review_count_filtered_data():
    return map(pass_line, filter(review_count_filter, get_time_filtered_data())) # time and review count filtered data

def pass_line(line):
    return line

def get_rating_avgs():
    return map(calculate_rating_avgs, get_time_and_review_count_filtered_data()) # rating avg


def de_dupicate(unique_list, moving_line):
    return unique_list + [moving_line] if not moving_line in unique_list else unique_list

# def review_count(two_lines):
#     row, line = two_lines
#     if review_total >= min_num_reviews:
#         return True
#     elif line['asin'] == row['asin']:

if __name__ == '__main__':

    b = reduce(find_top_rated_avgs, get_rating_avgs(), [])
