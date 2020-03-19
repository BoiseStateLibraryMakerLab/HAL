import random, pygame.mixer, serial, requests, datetime, os
from time import sleep
from sys import exit
from subprocess import call

pygame.mixer.init(44000, -16, 1, 1024)

# Sound Bank
# put all sounds into one folder and pull all the file names into a single list
# make sure new sounds are put in All_Sounds folder
# please keep a copy of sounds added in a separate folder (i.e. Pack 11

song_dir = '/home/pi/HAL/sound/All_Sounds/'
song_list = []
song_list = os.listdir(song_dir)
print(len(song_list))
print(song_list[1])


StartupSound = pygame.mixer.Sound('/home/pi/HAL/sound/Startup.ogg')
Daisy = pygame.mixer.Sound('/home/pi/HAL/sound/Daisy.ogg')
Rainbow = pygame.mixer.Sound('/home/pi/HAL/sound/Rainbow.ogg')
PowerOff = pygame.mixer.Sound('/home/pi/HAL/sound/All_Sounds/XP Off.ogg')
SorryDave = pygame.mixer.Sound('/home/pi/HAL/sound/Sorry Dave.ogg')

# Number of Sound Files (UPDATE THIS WHEN ADDING NEW SOUNDS!)
sounds = len(song_list)

# Serial Connection
print("Establishing Serial Connection...")
arduino = serial.Serial("/dev/ttyACM0",9600)
arduino.flush()
sleep(2)

print("Ready")
arduino.write(b'2')

on = False
cont = False

# Main Loop
while True:
    val = int(arduino.readline())
    print (val)
        
# Wait for Power On
    if on == False:
        if val == 3:
            StartupSound.play()
            arduino.write(b'6')
            on = True
        if val == 4:
            PowerOff.play()
            arduino.write(b'7')
            sleep(2)
            call("sudo shutdown -h now", shell=True)
        continue

# Check for False Power Off
    if val == 3:
        pygame.mixer.stop()
        SorryDave.play()
# Check for Power Off
    if val == 4:
        pygame.mixer.stop()
        Daisy.play()
        arduino.write(b'8')
        on = False
        
# Red Button          
    if val == 1:
        pygame.mixer.stop()
        playNum = random.randint(1,sounds)
        soundBite = pygame.mixer.Sound(song_dir + song_list[playNum])
        soundBite.play()

        #old code
##        current = "sound" + str(playNum)
##        command = current + ".play()"
##        exec(command)

        # Try Posting to HAL Database
##        try:
##            API_ENDPOINT = "https://boisestatecta.com/hal/add"
##            currtime = str(datetime.datetime.now())
##            payload = {'sound':playNum, 'time':currtime}
##            requests.post(url = API_ENDPOINT, data = payload)
##        except:
##            print("No Internet! WRONG!")
        
# Easter Egg
    if val == 2:
        pygame.mixer.stop()
        Rainbow.play()
        arduino.write(b'5')

