import websocket
import time
import json
import subprocess

try:
    import thread
except ImportError:
    import _thread as thread


config = {
    "name": "Sunday",
    "desc": "Very sensitive drive in the living room",
    "scripts": [
        {"name": "Fuck You",
         "desc": "A small visual reminder",
         "cmd": "python fk.py"},
        {"name": "LED blink",
         "desc": "Consider this as a test",
         "cmd": "python blink.py"}
    ]
}


def exec_script(ws, script_nb, *args):
    print("exectuting " + config["scripts"][script_nb]["cmd"])
    try:
        returncode = subprocess.call(config["scripts"][script_nb]["cmd"])
    except OSError:
        returncode = 1
    time.sleep(4)  # simulate time
    ws.send(json.dumps({"scriptNb": script_nb, "returnCode": returncode}))


def on_message(ws, message):
    print(message)
    thread.start_new_thread(exec_script, (ws, int(message)))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        time.sleep(100000)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.0.16:8080/websocket",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header={"type": "device",
                                        "name": config["name"],
                                        "desc": config["desc"],
                                        "scripts": json.dumps(config["scripts"])})
    ws.on_open = on_open
    ws.run_forever()
