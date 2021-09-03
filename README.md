# braspkeys
This is not currently working

I don't have much interest in implementing all keyboard capabilities beyond the usual. It probably wouldn't be too hard to add media keys, for instance, but I have no use for it.

takes input file as input to __main__.py, reads each line, and outputs that line to pc

if no input is given, takes input from standard in and writes each line.

```[python]
#!$ 6
# this sleeps for 6 seconds
!!$!!
# this exits
```

---


login script from raspberry pi to desktop

My PC was built with a motherboard from a dell optiplex, and I was unable to get the bios to stop throwing errors at startup. Furthermore, the wifi in my apartment is provided by my university, so I am unable to set up port forwarding.

So, I needed a solution to turn on my computer remotely without entering any commands.

I installed raspian lite onto my pi zero w then followed this tutorial to use the pi as a USB keyboard device: [http://www.isticktoit.net/?p=1383](http://www.isticktoit.net/?p=1383)

My PC bios lets me turn on the computer every morning and turn it on after blackouts, but I needed a way to get past the error screen.

I wrote this script and set it up to run twice every morning with crontab. I also set up VNC Client on the pi so I could run the script whenever I wanted.

## Notes

At one point while setting up the pi as a USB keyboard, I entered one wrong character and had to spend 2 hours finding that error. Beware of typos!

When everything was set up properly, my PC registered the pi as an unrecognized device, so don't be alarmed that the PC doesn't think it's a keyboard

By writing the keyboard press to /dev/hidg0, you are effectively writing to the usb keyboard input stream for the PC.

## How to customize

Best Practices are to write each key press and release separately so that the PC recognizes everthing in the right order and no funny errors occur.

Each key press and release consists of 8 bytes. Third byte is the key press. The first byte is the ctrl, shift, and alt keys.

For different keyboard presses, replace with the third byte with the Usage ID (Dec) number found on page 53 of the USB HID Usage tables pdf found here: [https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf)

A wonderful gist with the corresponding numbers can be found here [https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2](https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2)

For the ctrl, shift, and alt keys, replace the first byte with the number in the above github link.
