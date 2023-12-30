import json
from requests import post
import os


async def UploadQueue():
    headers_send = {
        "Authorization": os.getenv("Zortos_API_Key"),
    }
    with open("QueueInfo.json", "r+") as queueinfo:
        data = json.load(queueinfo)
    try:
        response = post("https://gfnqueueapi.zortos.me/api/setserverqueue", headers=headers_send, json=data)
        print("Send QUEUEINFO to gfnqueueapi.zortos.me")
    except:
        print("Error while sending QUEUEINFO to gfnqueueapi.zortos.me")