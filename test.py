import amazon_reviews
import sys

def test_sorting():
    data = {"start": "01.01.2010", "end": "31.12.2020", "limit": 2, "min_number_reviews": 2}
    try:
        review_data_path = sys.argv[1]
    except IndexError:
        raise IndexError('Please provide a file path directory for the json with the amazon review data')
    results = amazon_reviews.main(data)
    assert results == [{"asin": "B000JQ0JNS", "average_rating":4.5}, {"asin": "B000NI7RW8", "average_rating":3.6666666666666665}], 'Results do not match expected results'


if __name__ == '__main__':
    test_sorting()
    print("All tests passed!")