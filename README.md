<h2>Inspiration</h2>
Seeing the power of AI, we wanted to create a robot that can harness the power of it and be self-autonomous. Seeing self-driving cars like the ones made by Elon inspired us to create a more small scale robot that can do things on it own. Although we did not get to automating movement, it was still the beginning inspiration for the project.

<h2>What it does</h2>
The 2AK-Bot drives around using tank drive mechanics, controlled via a Bluetooth connection between a pygame program interpreting controller inputs, and an ESP32 connected to motors inside the rover. An arm attached to the top of the rover can pick up objects by closing via a servo and being assisted by two weak sticky pads. The rover includes three ESP32 cams that output vision to a WiFi domain, which is then read into a python program, this drives the rover approach. Vision also includes some very basic YOLO AI vision detection of objects.

<h2>How we built it</h2>
3D printing parts were designed and printed in advance. every part was tested individually and later assembled together.

<h2>Challenges we ran into</h2>
Many components were fried during the assembly of the robot. This caused many setbacks and delayed our bigger plans to train a vision model that will properly detect our desired objects. We had many issues with connection problems with the ESP32 cams, problems include low frame rate, uploading to WiFi issues, and frequent crashing. Some of our 3D printed parts were also not the correct design, and we needed to modify parts by using various methods, like melting holes with a solder iron. The inside of our robot also did not have enough space to fit all our electronics and we had to resort to putting the battery bank on the outside.

<h2>Accomplishments that we're proud of</h2>
Creating a complete robot with many useful functions. Overcoming many major issues through perseverance and an unwavering will.

<h2>What we learned</h2>
A large scale project like our 2AK-Bot needs more further preparation and planning.

<h2>What's next for 2AK-Bot</h2>
Training AI vision models to properly detect desired objects to track and pick up.
