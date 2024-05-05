from io import BytesIO
import pygame, sys, bluetooth, time
import cv2
import numpy as np
import urllib.request
import http.client

class PygameGame():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()

        self.joyNum = pygame.joystick.get_count()
        self.font30 = pygame.font.SysFont('Callimathy Demo', 50)

        self.width = 1280
        self.height = 960
        self.bgColor = (0, 0, 0)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load("assets/images/MasseyHacks UI.png")
        self.redlefttrigger = pygame.image.load("assets/images/redlefttrigger.png")
        self.redrighttrigger = pygame.image.load("assets/images/redrighttrigger.png")
        self.camnum = 1
        self.colors = ["red", "blue", "green"]
        self.leftstickrect = pygame.Rect(64, 782, 30, 30)
        self.rightstickrect = pygame.Rect(172, 824, 30, 30)
        self.dpadvert = pygame.Rect(107, 821, 15, 45)
        self.dpadhor = pygame.Rect(92, 836, 45, 15)
        self.lefttriggerrect = pygame.Rect(67, 691, 33, 45)
        self.righttriggerrect = pygame.Rect(200, 691, 33, 45)
        pygame.display.set_caption("2AK-Bot Software")
        pygame.display.set_icon(pygame.image.load("assets/images/2AK-BOT Logo.png"))

        self.setupBluetooth()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.input_threshold = 0.1

        self.turret_angle = 90
        self.turret_velocity = 1
        self.arm_angle = 90
        self.arm_velocity = 1
        self.gripperPos = 90
        self.gripper_velocity = 5

    def run(self):
        pygame.init()
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
            
            self.window.fill("black")
            self.window.blit(self.background_image, (0, 0))

            self.getControllerInput()
            self.checkController()

            pygame.display.flip()

    def checkController(self):
        mx, my = pygame.mouse.get_pos()

        if (self.leftstickrect.collidepoint(mx, my)):
            pygame.draw.circle(self.window, ("red"), (self.leftstickrect.x + 15, self.leftstickrect.y + 15), 15)
            self.drawOverlayRectangles()
            self.write_centered_text(self.window, "Move Left Stick up and down to control left wheels", pygame.Rect(mx, my - 50, 300, 50), "white")
        elif (self.rightstickrect.collidepoint(mx, my)):
            pygame.draw.circle(self.window, ("red"), (self.rightstickrect.x + 15, self.rightstickrect.y + 15), 15)
            self.drawOverlayRectangles()
            self.write_centered_text(self.window, "Move Right Stick up and down to control right wheels", pygame.Rect(mx, my - 50, 300, 50), "white")
        elif (self.dpadvert.collidepoint(mx, my) or self.dpadhor.collidepoint(mx, my)):
            pygame.draw.rect(self.window, ("red"), self.dpadvert)
            pygame.draw.rect(self.window, ("red"), self.dpadhor)
            self.drawOverlayRectangles()
            self.write_centered_text(self.window, "Press D-Pad left and right to rotate arm\nPress D-Pad up and down to move arm up and down", pygame.Rect(mx, my - 50, 300, 50), "white")
        elif (self.lefttriggerrect.collidepoint(mx, my)):
            self.window.blit(self.redlefttrigger, (self.lefttriggerrect.x, self.lefttriggerrect.y))
            self.drawOverlayRectangles()
            self.write_centered_text(self.window, "Press Left Trigger to open the gripper", pygame.Rect(mx, my - 50, 300, 50), "white")
        elif (self.righttriggerrect.collidepoint(mx, my)):
            self.window.blit(self.redrighttrigger, (self.righttriggerrect.x, self.righttriggerrect.y))
            self.drawOverlayRectangles()
            self.write_centered_text(self.window, "Press Right Trigger to close the gripper", pygame.Rect(mx, my - 50, 300, 50), "white")

    def drawOverlayRectangles(self):
        mx, my = pygame.mouse.get_pos()
        pygame.draw.rect(self.window, "white", (mx- 5, my - 55, 310, 60))
        pygame.draw.rect(self.window, "black", (mx, my - 50, 300, 50))
        

    def write_centered_text(self, screen, text, rectangle, colour, cache={}):
        rect_tuple = (rectangle.x, rectangle.y, rectangle.width, rectangle.height) # Convert rect to a tuple
        key = (text, rect_tuple, colour) # Use the tuple as the key
        if key in cache: # If the text has already been rendered, use the cached version
            for text_surface, x, y in cache[key]:
                screen.blit(text_surface, (x, y))
            return

        # Split the text into lines and calculate the size of the text
        lines = text.split("\n")
        font_size = 1
        font_obj = pygame.font.Font(None, font_size)
        line_sizes = [(line, font_obj.size(line)) for line in lines]
        widest_line, widest_size = max(line_sizes, key=lambda item: item[1][0])
        text_height = sum(size[1] for _, size in line_sizes)
        text_width = widest_size[0]

        # binary search for the maximum font size
        low, high = font_size, max(rectangle.width, rectangle.height)
        while low < high:
            mid = (low + high + 1) // 2
            font_obj = pygame.font.Font(None, mid)
            line_sizes = [(line, font_obj.size(line)) for line in lines]
            text_height = sum(size[1] for _, size in line_sizes)
            text_width = max(size[0] for _, size in line_sizes)

            if text_height <= rectangle.height and text_width <= rectangle.width:
                low = mid
            else:
                high = mid - 1

        # Render the text with the maximum font size
        font_size = low
        font_obj = pygame.font.Font(None, font_size)
        line_sizes = [(line, font_obj.size(line)) for line in lines]
        text_height = sum(size[1] for _, size in line_sizes)
        text_width = max(size[0] for _, size in line_sizes)

        cache[key] = []
        y = rectangle.y + (rectangle.height - text_height) // 2
        for i, (line, size) in enumerate(line_sizes): # Render each line of text
            text_surface = font_obj.render(line, True, colour)
            x = rectangle.x + (rectangle.width - size[0]) // 2
            screen.blit(text_surface, (x, y + i * size[1]))

            # Cache the rendered text
            cache[key].append((text_surface, x, y + i * size[1]))

    def setupBluetooth(self):
        target_name = "AFK ESP"
        target_address = None
        nearby_devices = bluetooth.discover_devices()
        # Look for the target device by name
        while target_address is None:
            for bdaddr in nearby_devices:
                if target_name == bluetooth.lookup_name(bdaddr):
                    target_address = bdaddr
                    break
        print(f"Found target Bluetooth device with address {target_address}")
        self.bt_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.bt_socket.connect((target_address, 1))
        data_str = "Hello, ESP32!\n"
        self.bt_socket.send(data_str.encode())  # Send a string to the ESP32

    def getControllerInput(self):
        buttons = []
        for x in range(13):
            buttons.append(self.joystick.get_button(x))
        
        stickL = round(self.joystick.get_axis(0), 3), round(self.joystick.get_axis(1), 3)  # Get the x and y axes values
        stickR = round(self.joystick.get_axis(2), 3), round(self.joystick.get_axis(3), 3)  # Get the x and y axes values

        # get dpad values
        dpad = self.joystick.get_hat(0)

        # get trigger values
        triggerL = self.joystick.get_axis(4)
        triggerR = self.joystick.get_axis(5)

        # Make the trigger values positive and between 0-1
        triggerL = (triggerL + 1) / 2
        triggerR = (triggerR + 1) / 2


        # Calculate the left and right motor speeds
        left_speed, right_speed = self.tankDrive(stickL, stickR)

        # Calculate the angle of the turret
        self.turret_angle = self.calculateTurretAngle(dpad)

        # Calculate the angle of the arm
        self.arm_angle = self.calculateArmAngle(dpad)

        # Calculate the position of the gripper
        self.gripperPos = self.calculateGripperPos(triggerL, triggerR)

        self.displayControllerInfo(left_speed, right_speed)

        # Create a string of the data to send to the ESP32
        # Left motor speed, right motor speed, turret angle, arm angle, gripper state, "\n"        
        data_str = f"{left_speed},{right_speed},{self.turret_angle},{self.arm_angle},{self.gripperPos},\n"

        # Send the data to the ESP32 over Bluetooth
        time.sleep(0.05) 
        self.bt_socket.send(data_str.encode())

    def displayControllerInfo(self, left_speed, right_speed):
        pygame.draw.rect(self.window, "black", (10, 300, 370, 330))
        text = self.font30.render(f"Left Speed: {left_speed:.2f}", True, (255, 255, 255))
        self.window.blit(text, (20, 310))
        text = self.font30.render(f"Right Speed: {right_speed:.2f}", True, (255, 255, 255))
        self.window.blit(text, (20, 378))
        text = self.font30.render(f"Turret Angle: {self.turret_angle}", True, (255, 255, 255))
        self.window.blit(text, (20, 446))
        text = self.font30.render(f"Arm Angle: {self.arm_angle}", True, (255, 255, 255))
        self.window.blit(text, (20, 514))
        text = self.font30.render(f"Gripper Position: {self.gripperPos:.0f}", True, (255, 255, 255))
        self.window.blit(text, (20, 582))

    def tankDrive(self, stickL, stickR):
    # Calculate the left and right motor speeds
    
    # if the stick is within the threshold, set the speed to 0
        if abs(stickL[1]) < self.input_threshold:
            left_speed = 0
        else:
            left_speed = stickL[1] * (-255)

        if abs(stickR[1]) < self.input_threshold:
            right_speed = 0
        else:
            right_speed = stickR[1] * (-255)

        return left_speed, right_speed

    def calculateTurretAngle(self, dpad):
    # Calculate the angle of the turret
        if dpad[0] == 1:
            self.turret_angle += self.turret_velocity
        elif dpad[0] == -1:
            self.turret_angle -= self.turret_velocity

        # Limit the turret angle to 0-180 degrees
        if self.turret_angle < 0:
            self.turret_angle = 0
        elif self.turret_angle > 180:
            self.turret_angle = 180
        
        return self.turret_angle
    
    def calculateArmAngle(self, dpad):
        # Calculate the angle of the arm
        if dpad[1] == 1:
            self.arm_angle += self.arm_velocity
        elif dpad[1] == -1:
            self.arm_angle -= self.arm_velocity

        # Limit the arm angle to 0-90 degrees
        if self.arm_angle < 0:
            self.arm_angle = 0
        elif self.arm_angle > 90:
            self.arm_angle = 90
        return self.arm_angle

    def calculateGripperPos(self, triggerL, triggerR):
        # Calculate the position of the gripper based on the triggers
        if triggerL > 0:
            self.gripperPos -= triggerL * self.gripper_velocity
        if triggerR > 0:
            self.gripperPos += triggerR * self.gripper_velocity

        # Limit the gripper position to 5-95 degrees
        if self.gripperPos < 5:
            self.gripperPos = 5
        elif self.gripperPos > 95:
            self.gripperPos = 95
        
        return self.gripperPos
    
if __name__ == '__main__':
    game = PygameGame()
    game.run()