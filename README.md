<p align="center"><img src="http://app.shopsline.ru/img-pic/kf/Hf3e4eb92d8c64b29bbdbb7538dbdf9c6I/DIY-Ambilight-RGB-5050.jpg_q50.jpg" width="50%" /></p>

# Ambilight for Mac OS

This part of software is a part for your Mac. It works only with Arduino UNO. See [Amilight Arduino part](https://github.com/sergeich5/Ambilight-Arduino-part)

# Instruction

- [Setup your Arduino UNO before use.](https://github.com/sergeich5/Ambilight-Arduino-part)
- Connect Arduino UNO to your Mac
- Run ambilight via python 2.7

# Check your python version

Run this command

```sh
$ python -v
Python 2.7.16 (default, Jul  5 2020, 02:24:03)
```

Required version is 2.7.x

# Configuration

edit `config.py` to your needs

# Run ambilight.py

```sh
python /path/to/ambilight.py
```

# Troubleshooting connection

In `Arduino.py` check this line

```python
            if 'tty.usbmodem' in port:
```

and change it regarding to your connected device. (For example Arduino on Mac is called `dev/tty.usbmodem143241101` so it will be detected, you don't have to change anything). Older models can be called `wchusbserial14`, then you have to change them accordingly.
