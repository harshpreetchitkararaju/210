import speech_recognition as sr
import paramiko


PI_IP = "192.168.1.114"   
PI_USER = "pi"           
PI_PASS = "1234"         
AU_PATH = "/home/pi/7.1d/au.py"  
def send_to_pi(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(PI_IP, username=PI_USER, password=PI_PASS)
        cmd = f"python3 {AU_PATH} {command}"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        ssh.close()
    except Exception as e:
        print("SSH Error:", e)

r = sr.Recognizer()


mic = None
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    if "Microphone" in name or "Headset" in name:
        try:
            mic = sr.Microphone(device_index=i, sample_rate=44100, chunk_size=1024)
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=2)
            print(f"Using microphone: {name}")
            break
        except Exception:
            continue

if mic is None:
    print("No working microphone found! Check your mic connection.")
    exit()

print("Say 'on' or 'off' to control LED. Say 'exit' to quit.")

while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=4)

        command = r.recognize_google(audio, language="en-IN").lower()
        print("You said:", command)

        if "on" in command:
            send_to_pi("on")
        elif "off" in command:
            send_to_pi("off")
        elif "exit" in command:
            print("Exiting program.")
            break
        else:
            print("Unknown command, try again")

    except sr.UnknownValueError:
        print("Could not understand, please repeat.")
    except sr.RequestError as e:
        print("Google Speech Recognition error:", e)
    except Exception as e:
        print("Error with microphone:", e)
