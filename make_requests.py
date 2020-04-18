from time import monotonic

import requests


root_api_url = "http://localhost:8000/v1/"


def make_requests(root_api_url, endpoint_url):
    session = requests.session()
    total_time = 0
    total_results = 0
    total_requests = 0
    next_url = None

    while True:
        start = monotonic()
        url = next_url if next_url else "{}{}".format(root_api_url, endpoint_url)

        response = session.get(url)
        end = monotonic()

        response_json = response.json()
        if response.status_code != 200:
            print("Error in response (status={}, json={}".format(response.status_code, response_json))
            break

        total_requests += 1
        total_results += len(response_json["results"])
        total_time += end - start

        if not response_json["next"]:
            break

        next_url = response_json["next"]

    print("endpoint={}, next_url={}, requests={}, time={:0.2f}, results={}".format(
        endpoint_url,
        next_url,
        total_requests,
        total_time,
        total_results,
    ))


make_requests(root_api_url, "orders/")
# make_requests(root_api_url, "optimized-orders/?fields=id")
# make_requests(root_api_url, "optimized-orders-2/?fields=id")
# make_requests(root_api_url, "optimized-orders-3/?fields=id")
make_requests(root_api_url, "optimized-orders-4/?fields=id")
# make_requests(root_api_url, "optimized-orders-5/?fields=id")
