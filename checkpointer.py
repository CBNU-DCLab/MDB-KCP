from kubernetes import client, config

import ssl
import threading
import requests
import os
import subprocess
import glob
import sys

def checkpoint(period):
    url='curl -X POST "https://nodeIP:10250/checkpoint/default/redis/redis --insecure --cert /var/run/kubernetes/client-admin.crt --key /var/run/kubernetes/client-admin.key"'
    r=requests.post(url)
    pattern="/var/lib/kubelet/checkpoints/checkpoint-redis-default-redis*.tar"
    result=glob.glob(pattern, recursive=True)
    for i in result:
      path=i
    script_path="./tar2image.sh "+path
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    threading.Timer(period, checkpoint).start()

ssl._create_default_https_context = ssl._create_unverified_context

config = client.Configuration()

config.api_key['authorization'] = ''
config.api_key_prefix['authorization'] = ''
config.host = ''
config.verify_ssl=False
execute_code(sys.argv[1])
