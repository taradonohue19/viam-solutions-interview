import asyncio
import yagmail

from viam.robot.client import RobotClient
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.media.utils.pil import viam_to_pil_image

api_key = 'API KEY'
api_key_id = 'API KEY ID'
address = 'ADDRESS'

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key=api_key,
        api_key_id=api_key_id
    )
    return await RobotClient.at_address(address, opts)

async def main():
    machine = await connect()

    myPeopleDetector = VisionClient.from_robot(machine, "myPeopleDetector")
    my_camera = Camera.from_robot(machine, "rayn-webcam")

    while True:
        img = await my_camera.get_image(mime_type="image/jpeg")
        detections = await myPeopleDetector.get_detections(img)

        found = False
        for d in detections:
            if d.confidence > 0.8 and d.class_name.lower() == "person":
                print("This is a person!")
                found = True

        if found:
            print("sending a message")
            pil_image = viam_to_pil_image(img)
            pil_image.save('/Users/raynschnell/Desktop/foundyou.jpeg')

            yag = yagmail.SMTP('EMAIL', 'APP PASSWORD')
            contents = ['There is someone at your desk - beware',
                        '/Users/raynschnell/Desktop/foundyou.jpeg']
            try:
                yag.send('2039426302@tmomail.net', 'subject', contents)
                print("Message sent!")
            except Exception as e:
                print(f"Failed to send message: {e}")


            await asyncio.sleep(60)
        else:
            print("There's nobody here, don't send a message")
            await asyncio.sleep(10)

    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
