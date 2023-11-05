from locust import HttpUser, task, constant_throughput, events
import requests

TOKEN = None

class HelloWorldUser(HttpUser):
  wait_time = constant_throughput(10)

  def context(self):
    return {"host": self.host}

  def on_start(self):
    global TOKEN
    TOKEN = self.client.get("/tokens").json()

  @task
  def hello_world(self):
    self.client.get("/", headers={"TOKEN": TOKEN})

  @events.request.add_listener
  def on_request(context, response, **kwargs):
    if response.status_code == 403:
      global TOKEN
      TOKEN = requests.get(f"{context['host']}/tokens").json()
