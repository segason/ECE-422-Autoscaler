from ScalerHttpService import ScalerHttpService
from math import ceil
import os
import time


class AutoScaler:
    def __init__(self):
        self.scalerService = ScalerHttpService()
        self.current_replicas = 1
        self.desired_response_time = 2000000

    def get_current_replicas(self):
        return self.current_replicas

    def set_current_replicas(self, number):
        self.current_replicas = number

    def get_average_response(self):
        self.scalerService.update_response_time('now-30s')
        return self.scalerService.get_response_time()

    def build_scale_command(self):
        return "sudo docker service scale test_web=" + str(self.current_replicas)

    def scale_web_service(self, response_time):
        if response_time is None:
            print("No requests received.")
            return
        print("Received an average response time of " + str(response_time))
        replicas = ceil(self.current_replicas * (response_time / self.desired_response_time))
        if 1 < replicas < 25:
            self.set_current_replicas(replicas)
            print("Scaling to " + str(self.current_replicas))
            # os.system(self.build_scale_command())


scaler = AutoScaler()
while True:
    scaler.scale_web_service(scaler.get_average_response())
    time.sleep(20)

