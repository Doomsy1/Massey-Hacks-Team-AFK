import cv2
import numpy as np
import urllib.request
import http.client
import pygame

pygame.init()
pygame.font.init()
# pygame.joystick.init()
# joyNum = pygame.joystick.get_count()
# print(joyNum)
screen = pygame.display.set_mode((1000, 800))
font30 = pygame.font.SysFont('Callimathy Demo', 30)

url1 = 'http://192.168.1.128/cam-lo.jpg'
url2 = 'http://192.168.1.112/cam-lo.jpg'
# url3 = 'http://192.168.1.112/cam-lo.jpg'

cap1 = cv2.VideoCapture(url1)
cap2 = cv2.VideoCapture(url2)
# cap3 = cv2.VideoCapture(url3)
whT=320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile='coco.names'
classNames=[]
with open(classesfile,'rt') as f:
    classNames=f.read().rstrip('\n').split('\n')


modelConfig = 'yolov3.cfg'
modelWeights= 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
def findObject(outputs,img):
    hT,wT,cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                if wT == 0 or hT == 0 or len(classIds) > 30:
                    continue
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)

    if(len(classIds) < 30):
        for i in indices:
            i = i
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)
 
       

def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)


import threading

def fetch_frame(url, cap, net, window_name):
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)
            blob = cv2.dnn.blobFromImage(im, 1/255, (whT, whT), [0,0,0], 1, crop=False)
            net.setInput(blob)
            layer_names = net.getLayerNames()
            output_names = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
            outputs = net.forward(output_names)
            findObject(outputs, im)
            cv2.imshow(window_name, im)
            cv2.imwrite('image.png', im)
            screen.blit(pygame.image.load('image.png'), (0,0))
            pygame.display.flip()

            cv2.waitKey(1)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except http.client.IncompleteRead:
            print("IncompleteRead caught, skipping frame")
            continue

    cap.release()

thread1 = threading.Thread(target=fetch_frame, args=(url1, cap1, net, 'Image 1'))
thread2 = threading.Thread(target=fetch_frame, args=(url2, cap2, net, 'Image 2'))
# thread3 = threading.Thread(target=fetch_frame, args=(url3, cap3, net, 'Image 3'))

thread1.start()
thread2.start()
# thread3.start()

thread1.join()
thread2.join()
# thread3.join()

cv2.destroyAllWindows()

pygame.quit()
