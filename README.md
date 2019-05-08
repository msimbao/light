# Light

A lamp for creating dynamic lighting in hospitals patient rooms to administer chroma-therapy for improving comfort of patients going through chemotherapy or recovering from surgery and being able as care givers to serve them better.

## Personal History

I have always being interested in physiotherapy for patients in hospitals and finding ways to improve their mood and mental health. This is because encouraging patients to have a positive outlook is important for [serving them while they recover](https://www.nytimes.com/2017/03/27/well/live/positive-thinking-may-improve-health-and-extend-life.html). My mom is a physician and I wanted to think of interesting uses of technology to serve caregivers and patients by using light of different wavelengths to create positivie effects in the hospitals.

## Background

The device is a machine that changes the lighting of a room based on what the occupants of the room need. This type of Chromotherapy has been in existence since 2000 BCE when the Egyptians and hemetican Greeks had treatment sanctuaries with rooms of different colors which had different healing qualities [1](https://www.naturalnews.com/036483_light_therapy_health_science.html). Of late, modern studies reported by the New York times and even MIT’s Richard J.Wurtman has shown that individual colors can treat premature babies of jaundice (30,000 children are treated each year instead of having dangerous blood transfusions), prevent black lung disease, improve work ability and even reduce aggression in violent juveniles [2](https://www.naturalnews.com/036483_light_therapy_health_science.html). 

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

These can be located





