import os
import sys

sys.path.append("/opt/ros/melodic/lib/python2.7/dist-packages")

import rospy
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import hiwonder

chassis = hiwonder.MecanumChassis()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO
)
logger = logging.getLogger(__file__)

app = Flask(__name__)


def forward():
    chassis.set_velocity(60,90,0)
    rospy.sleep(2)
    chassis.set_velocity(0,0,0)

def backward():
    chassis.set_velocity(60,270,0)
    rospy.sleep(2)
    chassis.set_velocity(0,0,0)   

def turn_left():
    chassis.set_velocity(0,0,30)
    rospy.sleep(1)
    chassis.set_velocity(0,0,0)

def turn_right():
    chassis.set_velocity(0,0,-30)
    rospy.sleep(1)
    chassis.set_velocity(0,0,0)

    


def run_car_cmd_api():
    @app.route("/control_command", methods=["POST"])
    def cmd_car():
        logger.info("get cmd")
        cmd = request.json["cmd"]
        logger.info(f"get cmd: {cmd}")
        if cmd == "forward":
            forward()
        elif cmd == "backward":
            backward()
        elif cmd == "left":
            turn_left()
        elif cmd =="right":
            turn_right()
        return {"status": "ok"}

    app.run(host="0.0.0.0", port=933)
