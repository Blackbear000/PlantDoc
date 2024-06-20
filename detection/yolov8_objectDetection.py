import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO

class ObjectDetection:

    def __init__(self):

        # self.capture_index = capture_index
        self.device = 'mps'
        self.model = self.load_model()

    def load_model(self):
        model = YOLO('E:\\NUS2\\GP1\\html\\detection\\train13\\weights\\best.pt')
        model.fuse()
        return model

    def predict(self, frame):
        results = self.model(frame)
        return results

    def control_car(self, results):
        # 默認行為
        action= '繼續行駛'
        stop_threshold =200

        for result in results:
            class_id = result.cls
            conf = result.conf
            box = result.box
            box_size = (box[2] - box[0]) * (box[3] - box[1])

            if class_id == 2 and conf > 0.5:  # 假设红灯的类别ID为2
                action = "停车"
            elif class_id == 1 and conf > 0.5:  # 假设黄灯的类别ID为1
                if box_size > stop_threshold:
                    action = "加速通过"
                else:
                    action = "减速并停车"
            elif class_id == 3 and conf > 0.5:  # 假设绿灯的类别ID为3
                action = "正常行驶"

        print(f"执行动作: {action}")
        return action

    def plot_bboxes(self, results, frame):

        def plot_bboxes(self, results, frame):
            # 画出所有检测到的框
            for result in results.xyxy[0]:
                cv2.rectangle(frame, (int(result[0]), int(result[1])), (int(result[2]), int(result[3])), (0, 255, 0), 2)
            cv2.imshow('frame', frame)
        # xyxys= []
        # confidences = []
        # class_id = []
        #
        # for result in results:
        #     boxes = result.boxes.cpu().numpy()
        #
        #     xyxys.append(result.xyxy)
        #     confidences.append(result.conf)
        #     class_id.append(result.cls)
        #
        #     # for xyxy in xyxys:
        #         # confidences.append(xyxy[4])
        #         # class_id.append(xyxy[5])
        # # cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0,255,0))
        #
        #
        #
        # return results[0].plot(), xyxys, confidences, class_id

    def __call__(self, *args, **kwargs):
        # # 這邊是獲取的網絡攝像頭，實實獲取到的視頻
        # cap = cv2.VideoCapture(self.capture_index)
        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     results = self.predict(frame)
        #     self.control_car(results)
        #     # 下面是打印出目標的bounding box
        #     # self.plot_bboxes(results, frame)
        #     # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     #     break
        # cap.release()
        # cv2.destroyAllWindows()
        image_path = '/Users/laiweizhi/Desktop/bg-shrubs.jpg'
        # img = cv2.imread(image_path)
        results = self.predict(image_path)
        for result in results:
            class_id = result.cls
            conf = result.conf

            print(f'class is:{class_id}')
            print(f'confidence score is: {conf}')


# model = YOLO('E:\\NUS2\\GP1\\html\\detection\\train13\\weights\\best.pt')

# # results = model('your folder path/image path/mp4/live camera')
# results = model('E:\\NUS2\\GP1\\html\\detection\\plant.jpeg')

# for result in results:
#     boxes = result.boxes
#     name = result.names
#     print(f'class id: {boxes.cls}')
#     print(f'confidence: {boxes.conf}')
#     print(f'class name is: {name[boxes.cls.item()]}')
#     print('----------------------\n')
    # result.show() 顯示照片出來
    # result.save() 保存圖片