import json_stream
import json
from sys import getsizeof
import datetime
from functools import reduce
from flask import Flask, request
import sys


class TopAmazonReviews:
    def __init__(self, start, end, limit, min_number_reviews, review_data_path):
        self.start = start
        self.end = end
        self.limit = limit
        self.min_number_reviews = min_number_reviews
        self.review_data_path = review_data_path

    def read(self, string):
        """Converts a line from a new-line delimited json, which is read as a string, to a json object"""
        return json.loads(string)

    def time_filter(self, line):
        """Excludes data outside of the 'start' and 'end' date range"""
        return line['unixReviewTime'] >= self.date_str_to_unix_time(self.start) and line['unixReviewTime'] <= self.date_str_to_unix_time(self.end)

    def date_str_to_unix_time(self, date_string):
        return int(datetime.datetime.strptime(date_string, "%d.%m.%Y").timestamp())

    def review_count_filter(self, static_line):

        def line_scanner(count, moving_line): # potentially add functionality that breaks function as soon as first True occurs
            if type(count) == bool:
                return True
            if count == self.min_number_reviews:
                return True
            if moving_line['asin'] == static_line['asin']:
                if count + 1 == self.min_number_reviews:
                    return True
                return count + 1
            else:
                return count

        if type(reduce(line_scanner, self.get_time_filtered_data(), 0)) == int:
            return False
        else:
            return True

    def calculate_rating_avgs(self, static_line):

        def identity_tester(moving_line):
            if moving_line['asin'] == static_line['asin']:
                return True
            else:
                return False

        def count_overall(a, b):
            return a + 1

        def sum_overall(a, b):
            return a + b['overall']

        return {"asin": static_line['asin'], "average_rating": reduce(sum_overall, filter(identity_tester, self.get_time_and_review_count_filtered_data()), 0) / reduce(count_overall, filter(identity_tester, self.get_time_and_review_count_filtered_data()), 0)}

    def find_top_rated_avgs(self, top_avgs_list, static_line):

        def compare_avgs(highest_avg, current_avg):
            if highest_avg in top_avgs_list: # exclude top avgs already found
                return current_avg
            if current_avg["average_rating"] > highest_avg["average_rating"] and current_avg not in top_avgs_list:
                return current_avg
            else:
                return highest_avg


        if len(top_avgs_list) == self.limit:
            return top_avgs_list
        else:
            return top_avgs_list + [reduce(compare_avgs, self.get_rating_avgs())]


    def get_time_filtered_data(self):
        f = open(self.review_data_path)
        data = map(self.read, f)
        return map(self.pass_line, filter(self.time_filter, data)) # time filtered data

    def get_time_and_review_count_filtered_data(self):
        return map(self.pass_line, filter(self.review_count_filter, self.get_time_filtered_data())) # time and review count filtered data

    def pass_line(self, line):
        return line

    def get_rating_avgs(self):
        return map(self.calculate_rating_avgs, self.get_time_and_review_count_filtered_data()) # rating avg


    def de_dupicate(self, unique_list, moving_line):
        return unique_list + [moving_line] if not moving_line in unique_list else unique_list


app = Flask(__name__)

def main(data):
    start = data['start']
    end = data['end']
    limit = data['limit']
    min_number_reviews = data['min_number_reviews']
    x = TopAmazonReviews(start, end, limit, min_number_reviews, review_data_path)

    return reduce(x.find_top_rated_avgs, x.get_rating_avgs(), [])

@app.route("/amazon/best-rated HTTP/1.1", methods=['POST'])
def best_rated_products_endpoint():
    data = request.get_json()
    return main(data)


if __name__ == '__main__':
    review_data_path = sys.argv[1]

    # data = {"start":"01.01.2010", "end":"31.12.2020", "limit":2, "min_number_reviews":2}
    # main(data)

    app.run(host='0.0.0.0', port=8080)



