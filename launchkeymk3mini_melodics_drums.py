import rtmidi
from pynput.keyboard import Controller

def midi2keypress():
    midiIn = rtmidi.RtMidiIn()
    inputPorts = midiIn.getPortCount()
    footDevice = True if midiIn.getPortCount() >= 3 else False

    if inputPorts:
        midiIn.openPort(0)
        if footDevice:
            midiInFoot = rtmidi.RtMidiIn()
            midiInFoot.openPort(2)
    else:
        print("No MIDI input ports available.")
        return

    print("Press Ctrl+C to exit.")

    noteKeyMap = {
        48: 'a', # kick
        50: 'a', # kick
        60: 'd', # snare
        62: 'd', # snare
        63: 'u', # open hihat
        51: 'y', # closed hihat
        65: 'e', # crash
        53: 'j', # ride
        67: 'f', # hi tom
        68: 'g', # mid tom
        70: 'h', # low tom
        55: 't', # foot hi
    }

    keyboard = Controller()

    try:
        while True:
            msg = midiIn.getMessage()
            
            if msg:
                note = msg.getNoteNumber()
                velocity = msg.getVelocity()
                if velocity > 0 and note in noteKeyMap:
                    key = noteKeyMap[note]
                    keyboard.press(key)
                    keyboard.release(key)
                    print(key)
            if footDevice:
                footMsg = midiInFoot.getMessage()
                if footMsg:
                    CCNumber = footMsg.getControllerNumber()
                    CCValue = footMsg.getControllerValue()
                    if CCValue > 0 and CCNumber == 55:
                        keyboard.press('a')
                        keyboard.release('a')

    except KeyboardInterrupt:
        pass

    midiIn.closePort()
    if footDevice:
        midiInFoot.closePort()

midi2keypress()
