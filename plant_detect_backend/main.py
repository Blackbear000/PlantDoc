import multiprocessing
from car_control import run_car_cmd_api
from img_collect_ros import collect_img
from visual_odometry import Localizer

img_url = "http://192.168.149.32:930/test/img"
vo_url = "http://192.168.149.32:930/test/vo"

def main():
    shared_img_str = multiprocessing.Array("c", 10*1024*1024, lock=False)
    localizer = Localizer()
    
    # used to accept car command instruction
    car_cmd_process = multiprocessing.Process(target=run_car_cmd_api)
    
    # used to extract img and send to frontend
    img_collect_process = multiprocessing.Process(target=collect_img, args=(shared_img_str, img_url))
    
    # used to calculate the vo and send to frontend
    localizer_process = multiprocessing.Process(target=localizer.localize, args=(shared_img_str, vo_url))

    # TODO voice control

    car_cmd_process.start()
    img_collect_process.start()
    localizer_process.start()

    car_cmd_process.join()
    img_collect_process.join()
    localizer_process.join()


if  __name__ == "__main__":
    main()
