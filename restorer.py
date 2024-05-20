from kubernetes import client, config
import ssl
import threading
import requests
import os
import subprocess
import glob
import sys

ssl._create_default_https_context = ssl._create_unverified_context


def restore(v1,period):
    pod_list = v1.list_namespaced_pod('default')
    pod=pod_list[0]
    state=pod.status.phase
    if state == 'Error':
       api_response = v1.delete_namespaced_pod('redis', 'default')
       pod_manifest= {
          "apiVersion": "v1",
          "kind": "Pod",
          "spec": {
          "containers": [
            {
            "name": "redis",
            "image": "localhost/redis:latest"
            }
          ]
        }
        }
       api_response = v1.create_namespaced_pod(body=pod_manifest, namespace='default')
       threading.Timer(period, restore).start()

config = client.Configuration()

config.api_key['authorization'] = ''
config.api_key_prefix['authorization'] = ''
config.host = ''
config.verify_ssl=False

config.load_kube_config()
v1 = client.CoreV1Api()
period=sys.argv[1]
restore(v1,period)