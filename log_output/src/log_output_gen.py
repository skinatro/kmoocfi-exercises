"""Log Generator"""

import datetime
import random
import string
import time


def generate_random_log():
    """
    Generate a random string and print it to stdout and to a file 
    """
    file_path = "/tmp/kube/logs.txt"

    while True:
        rstr = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                       for _ in range(32))
        timestamp = datetime.datetime.now()
        hash_string = f"{timestamp} {rstr}"
        with open(file_path, 'w') as file:
            file.write(hash_string + '\n')
        print(hash_string)
        time.sleep(5)

generate_random_log()
