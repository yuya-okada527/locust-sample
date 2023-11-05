from locust import HttpUser, task, constant_throughput, events

TOKEN = None

class HelloWorldUser(HttpUser):
  wait_time = constant_throughput(10)

  def on_start(self):
    global TOKEN
    TOKEN = self.client.get("/tokens").json()

  @task
  def hello_world(self):
    self.client.get("/", headers={"TOKEN": TOKEN})

  # @events.request.add_listener
  # def on_request(response):
  #   print(response)
  #   if response.status_code == 403:
  #     self.refresh_token()

  # def get_token(self):
  #   res = self.client.get("/tokens")
  #   return res.text

  # def refresh_token(self):
  #   self.token = self.get_token()
