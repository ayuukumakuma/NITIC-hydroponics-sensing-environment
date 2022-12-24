from config.firebase import initialize
from sensing import sensing_data
from push import push
from control import control

if __name__ == "__main__":
  db = initialize()
  data = sensing_data()
  push(data, db)
  print(data)
  # control(data, db)