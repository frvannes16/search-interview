import json
import random
import argparse
import requests
import sys

from ratelimit import limits, sleep_and_retry

parser = argparse.ArgumentParser(
    description="Generate random businesses and send them to a file or an API."
)
parser.add_argument(
    "num_businesses",
    metavar="N",
    type=int,
    help="the number of businesses to generate",
)
parser.add_argument("-f", "--file", dest="outfile", action="store")
parser.add_argument("-a", "--api", dest="api_url", action="store")

states = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]
word_file = "/usr/share/dict/words"
cities = [word.title() for word in open(word_file).read().splitlines() if len(word) > 4]

chains = [
    "McDonalds",
    "Wendy's",
    "Chipotle",
    "7-11",
    "Capital One",
    "Costa Coffee",
    "Starbucks",
]


# 50 businesses per call sent to API at 10 calls per second
BATCH_SIZE = 50
API_CALLS_PER_PERIOD = 10
PERIOD_LENGTH = 1


def main():
    args = parser.parse_args()

    if args.outfile:
        write_businesses_to_file(args.outfile, args.num_businesses)
    elif args.api_url:
        write_businesses_to_api(args.api_url, args.num_businesses)


def write_businesses_to_file(filename, num_businesses):
    businesses = [b for b in business_generator(num_businesses)]
    data = {"businesses": businesses}
    print(f"Writing locations to {filename}")
    with open(filename, "w") as f:
        json.dump(data, f)


def write_businesses_to_api(url, num_businesses):
    businesses_to_send = num_businesses
    businesses = []
    generator = business_generator(num_businesses)
    while businesses_to_send > 0:
        for _ in range(BATCH_SIZE):
            businesses += [next(generator)]
            businesses_to_send -= 1

        send_to_api(url, {"businesses": businesses})
        businesses = []


@sleep_and_retry
@limits(calls=API_CALLS_PER_PERIOD, period=PERIOD_LENGTH)
def send_to_api(url, results):
    response = requests.post(url, json=results)
    if response.status_code not in [200, 201]:
        print(f"Failed to post businesses to {url}. {response}")
        sys.exit(1)


def business_generator(num_businesses):
    num_cities = int(num_businesses / len(chains) / len(states))
    for counter in range(1, num_businesses + 1):
        city = cities[random.randint(0, num_cities - 1)]
        state = states[random.randint(0, len(states) - 1)]
        chain = chains[random.randint(0, len(chains) - 1)]
        yield {"id": counter, "name": chain, "state": state, "city": city}


if __name__ == "__main__":
    main()
