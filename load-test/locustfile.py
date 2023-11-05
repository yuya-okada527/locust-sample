import subprocess

from locust import HttpUser, task, constant_throughput, events
import requests

TOKEN = None

class HelloWorldUser(HttpUser):
  wait_time = constant_throughput(10)

  def context(self):
    return {"host": self.host}

  def on_start(self):
    refresh_token(self.host)

  @task
  def hello_world(self):
    self.client.get("/", headers={"TOKEN": TOKEN})

  @events.request.add_listener
  def on_request(context, response, **kwargs):
    if response.status_code == 403:
      refresh_token(context['host'])

def refresh_token(host):
  result = subprocess.run(
    ["curl", f"{host}/tokens"],
    stdout=subprocess.PIPE,
    text=True
  )
  global TOKEN
  print(result.stdout[1:-1])
  TOKEN = result.stdout[1:-1]
