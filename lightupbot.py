import asyncio
import os

from viam.robot.client import RobotClient
from viam.components.sensor import Sensor

from viam.components.camera import Camera
from viam.services.vision import VisionClient
from kasa import Discover, SmartBulb

async def connect():
    opts = RobotClient.Options.with_api_key(api_key="lfuhwvnd01prtzs3lq216vh3onosmbqa", api_key_id="53588681-2a79-4776-8202-839093c2d91d")
    return await RobotClient.at_address("rayn-mac-people-detector-main.aj6vb85d5u.viam.cloud", opts)

async def main():
    robot = await connect()
    
    myPeopleDetector = VisionClient.from_robot(robot, "myPeopleDetector")
    my_camera = Camera.from_robot(robot, "camera-1")
    bulb = SmartBulb('192.168.1.182')

    await bulb.update()
    await bulb.turn_off()
    state = "off"


    while True:
        img = await my_camera.get_image(mime_type="image/jpeg")
        detections = await myPeopleDetector.get_detections(img)
        found = False
        for d in detections:
            if d.confidence > 0.5 and d.class_name.lower() == "person":
                print("Person!!")
                found = True
                
        if found:
            #turn on the lightbulb
            await bulb.turn_on()
            await bulb.update()
            print("turning on")
            state = "on"
            await asyncio.sleep(1)
        else:
            print("there's nobody here")
            #turn off the lightbulb
            await bulb.turn_off()
            await bulb.update()
            print("turning off")
            state = "off"
            await asyncio.sleep(1)

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
