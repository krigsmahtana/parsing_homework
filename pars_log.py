import argparse
import re
import json
from collections import defaultdict
from collections import Counter

parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
args = parser.parse_args()

dict_ip = defaultdict(
    lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0}
)
method_get = 0
method_post = 0
method_put = 0
method_delete = 0
method_head = 0
time_all = []
ip_all = []
req_string = []
with open(args.file) as file:
    idx = 0
    for line in file:
        # if idx > 1000:
        #   break

        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
        if ip_match is not None:
            time = re.search(r"([ ]+(\w+)[ ]+)\B", line)
            if time is not None and time != 0:
                time_f = time.group().strip()
                try:
                    int(time_f)
                    time_all.append(time_f)
                except ValueError:
                    pass
            ip = ip_match.group().strip()
            ip_all.append(ip)
            req_string.append(ip_match.string.split())
            method = re.search(r"\] \"(GET)", line)
            if method is not None:
                method_get += 1
            method = re.search(r"\] \"(POST)", line)
            if method is not None:
                method_post += 1
            method = re.search(r"\] \"(PUT)", line)
            if method is not None:
                method_put += 1
            method = re.search(r"\] \"(DELETE)", line)
            if method is not None:
                method_delete += 1
            method = re.search(r"\] \"(HEAD)", line)
            if method is not None:
                method_delete += 1
            idx += 1
top_ip = Counter(sorted(ip_all, reverse=True)).most_common(3)
temple = sorted(time_all, reverse=True)[:6]
req_1 = [req_string[time_all.index(temple[0])][0] + req_string[time_all.index(temple[0])][5] +
         req_string[time_all.index(temple[0])][6] + req_string[time_all.index(temple[0])][10]]
req_2 = [req_string[time_all.index(temple[1])][0] + req_string[time_all.index(temple[1])][5] +
         req_string[time_all.index(temple[1])][6] + req_string[time_all.index(temple[1])][10]]
req_3 = [req_string[time_all.index(temple[2])][0] + req_string[time_all.index(temple[2])][5] +
         req_string[time_all.index(temple[2])][6] + req_string[time_all.index(temple[2])][10]]
print(json.dumps({'Summ all metods': {'GET': method_get, 'POST': method_post, 'PUT': method_put,
                                      'DELETE': method_delete, 'HEAD': method_head},
                  "top 3 ip": {1: top_ip[0][0], 2: top_ip[1][0], 3: top_ip[2][0]}, 'top 3 so long requests': {
        temple[0]: req_1, temple[1]: req_2, temple[2]: req_3}}, indent=4))
