import os
import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    """
    Read the logs created by the generator and serve them on endpoint /
    """
    file_path_logs = "/tmp/kube/logs.txt"
    file_path_confmap = "/etc/config/information.txt"

    try:
        with open(file_path_confmap, 'r') as confmap:
            confmapfile_content = confmap.read()
    except Exception as e:
        confmapfile_content = f"Error reading config map file: {e}"

    envvar_content = os.environ.get("MESSAGE", "Not Set")

    try:
        with open(file_path_logs, 'r') as logs:
            logs_content = logs.read()
    except Exception as e:
        logs_content = f"Error reading logs file: {e}"

    try:
        response = requests.get(url="http://ping-pong-app-svc/pings", timeout=3)
        response.raise_for_status()
        pongs_content = response.text
    except requests.RequestException as e:
        pongs_content = f"Error fetching ping-pong count: {e}"

    return (
        f"File content: {confmapfile_content} <br>"
        f"Env variable: MESSAGE={envvar_content} <br>"
        f"{logs_content} <br>"
        f"Ping / Pongs: {pongs_content}"
    )


@app.route('/healthz')
def healthz():
    """
    Health check endpoint.
    Simple check returning 200 OK.
    """
    return Response("OK", status=200)


if __name__ == "__main__":
    port = os.environ.get("PORT")
    print(f"The Server started at {port}")
    app.run(host="0.0.0.0", port=int(port), debug=True)
