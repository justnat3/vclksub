# all stdlib python, this does not require that you install anything
import random
import uuid 
import threading
import json
import urllib3
from http.client import HTTPSConnection
from typing import Optional

names = [
    "Chung",
    "Chen",
    "Melton",
    "Hill",
    "Puckett",
    "Song",
    "Hamilton",
    "Bender",
    "Wagner",
    "McLaughlin",
    "McNamara",
    "Raynor",
    "Moon",
    "Woodard",
    "Desai",
    "Wallace",
    "Lawrence",
    "Griffin",
    "Dougherty",
    "Powers",
    "May",
    "Steele",
    "Teague",
    "Vick",
    "Gallagher",
    "Solomon",
    "Walsh",
    "Monroe",
    "Connolly",
    "Hawkins",
    "Middleton",
    "Goldstein",
    "Watts",
    "Johnston",
    "Weeks",
    "Wilkerson",
    "Barton",
    "Walton",
    "Hall",
    "Ross",
    "Woods",
    "Mangum",
    "Joseph",
    "Rosenthal",
    "Bowden",
    "Underwood",
    "Jones",
    "Baker",
    "Merritt",
    "Cross",
    "Cooper",
    "Holmes",
    "Sharpe",
    "Morgan",
    "Hoyle",
    "Allen",
    "Rich",
    "Grant",
    "Proctor",
    "Diaz",
    "Graham",
    "Watkins",
    "Hinton",
    "Marsh",
    "Hewitt",
    "Branch",
    "O'Brien",
    "Case",
    "Christensen",
    "Parks",
    "Hardin",
    "Lucas",
    "Eason",
    "Davidson",
    "Whitehead",
    "Rose",
    "Sparks",
    "Moore",
    "Pearson",
    "Rodgers",
    "Graves",
    "Scarborough",
    "Sutton",
    "Sinclair",
    "Bowman",
    "Olsen",
    "Love",
    "McLean",
    "Christian",
    "Lamb",
    "James",
    "Chandler",
    "Stout",
    "Cowan",
    "Golden",
    "Bowling",
    "Beasley",
    "Clapp",
    "Abrams",
    "Tilley",
]

# ssl/http options
HTTP_TIMEOUT = 100.0
HEADERS = {"Content-Type": "application/json", "Connection": "close"}
VOTE_PATH = "/api/campaigns/fab/vote"

# disabling TLS verify warnings
urllib3.disable_warnings()
ACCEPTABLE = [200, 201, 204]


class VoteCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0

    def update(self):
        with self.lock:
            self.value += 1


def _request(method: str, base: str, path: str, data: Optional[str]):
    client = HTTPSConnection("fab.usacnation.com", timeout=HTTP_TIMEOUT)
    acceptable_method = ["PUT", "PATCH", "GET", "DELETE", "POST"]
    if method not in acceptable_method:
        print(f"[ERROR]: HTTP_METHOD_UNACCEPTABLE {method}")

    # Create and put the request in flight
    client.request(method, path, data, HEADERS)

    # return the response
    status = client.getresponse()
    client.close()
    return status


def get(base: str, path: str) -> bool:
    result = _request("GET", base, path, None)
    return True if result.status in ACCEPTABLE else False


def post(data: Optional[str], base: str, path: str) -> bool:
    result = _request("POST", base, path, data)
    result.close()
    return True if result.status in ACCEPTABLE else False


def thread_vote(vc: VoteCounter) -> bool:
    for _ in range(100):
        name = random.sample(names, 2)
        uid = str(uuid.uuid4())
        print(uid)

        payload = json.dumps(
            {
                "name": f"{' '.join(name)}",
                "email": f"{uid}@foobar.com",
                "candidateId": "Kaylee Bryson",
            }
        )
        if post(payload, "fab.usacnation.com", VOTE_PATH):
            vc.update()

    return True


def main():
    vc = VoteCounter()
    threads = list()

    for _ in range(int(input("# of Votes * 100: "))):
        thr = threading.Thread(target=thread_vote, args=(vc,))
        threads.append(thr)
        thr.start()

    for thread in threads:
        thread.join()

    print(f"Voted: {vc.value} times!")

main()
