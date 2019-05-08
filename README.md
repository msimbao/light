# Light

A Simple Wall lamp for creating dynamic lighting in hospitals patient rooms to administer chroma-therapy for improving comfort of patients going through chemotherapy or recovering from surgery and being able as care givers to serve them better.

![Full Wall Light Prototype. Emits light from the top](https://photos.app.goo.gl/oiSVbiHgZpHfvMgY8)

## Personal History

I have always being interested in physiotherapy for patients in hospitals and finding ways to improve their mood and mental health. This is because encouraging patients to have a positive outlook is important for [serving them while they recover](https://www.nytimes.com/2017/03/27/well/live/positive-thinking-may-improve-health-and-extend-life.html). My mom is a physician and I wanted to think of interesting uses of technology to serve caregivers and patients by using light of different wavelengths to create positivie effects in the hospitals.

## Background

The device is a machine that changes the lighting of a room based on what the occupants of the room need. This type of Chromotherapy has been in existence since 2000 BCE when the Egyptians and hemetican Greeks had treatment sanctuaries with rooms of different colors which had different healing qualities [1](https://www.naturalnews.com/036483_light_therapy_health_science.html). Of late, modern studies reported by the New York times and even MIT’s Richard J.Wurtman has shown that individual colors can treat premature babies of jaundice (30,000 children are treated each year instead of having dangerous blood transfusions), prevent black lung disease, improve work ability and even reduce aggression in violent juveniles [2](https://www.naturalnews.com/036483_light_therapy_health_science.html). 

## Design Side Note

The lamp was made using a wooden box painted white with a 3D printed geometric dog I designed. The lamp was meant to be minimalist but aesthetically pleasing and the 3D image can be anything depending on the preference of the user. IT just creates something nice to look at.

## Prerequisites

To Run the device, you will need a [Raspberry Pi](https://www.amazon.com/Raspberry-Pi-MS-004-00000024-Model-Board/dp/B01LPLPBS8) and [Sunfounder Sensor Kit](https://www.sunfounder.com/rpi2-sensorv2.html). 

From the sensor kit, we will only use the:
* RGB LED module
* LCD Display
* Relay Module

Additionally, you will need a [UV lamp](https://www.amazon.com/Sterilization-Waterproof-Control-7-inch-Ultraviolet/dp/B07KVM9LSB/ref=sr_1_1_sspa?keywords=uvc+lamp+sunny+smell&qid=1557287755&s=gateway&sr=8-1-spell-spons&psc=1)

## Installing and importing software

For Software, you will need the python raspberry pi gpio modules, sensor kit modules and tutorials that can be found on [sunfounder's website](https://www.sunfounder.com/learn/category/sensor-kit-v2-0-for-raspberry-pi-b-plus.html) and tkinter

Open your raspberry pi terminal then type the following:

**Update First**

```
sudo apt-get update
```

**Install Tkinter for Python3**

```
sudo add-apt-repository ppa:deadsnakes
sudo apt-get update
sudo apt-get install python3.5 python3.5-tk
```
**Install gpio**

```
sudo apt-get install rpi.gpio
```

**Finding Sunfounder modules**

These can be located on the (sunfounder tutorial website)[https://www.sunfounder.com/learn/category/sensor-kit-v2-0-for-raspberry-pi-b-plus.html]. Download the (sensor kit zip file)[https://www.sunfounder.com/learn/download/U2Vuc29yX0tpdF9WMi4wX2Zvcl9CX19SUGkyX2FuZF9SUGkzXy56aXA=/dispa] that has example python scripts and modules for running any important components incase you are interested.

I only used the LCD1602 module and you can find this in my src file and can copy and paste it to wherever you need to use it.

## Running without hardware:

If you simply want to run the script without the hardware and see the GUI and the tkinter widgets, you can comment out the import modules at the top of the script relating to the GPIO and LCD1602 modules.

```
#import RPi.GPIO as GPIO  - comment out using a hashtag

#import LCD1602 - comment out using a hashtag
```

The full GUI should look like this:




