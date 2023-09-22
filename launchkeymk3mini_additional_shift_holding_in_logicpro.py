import rtmidi

def midiPassthrough():
    midiIn = rtmidi.RtMidiIn()
    midiOut = rtmidi.RtMidiOut()

    inputPorts = midiIn.getPortCount()
    if inputPorts:
        midiIn.openPort(1)
    else:
        print("No MIDI input ports available.")
        return

    outputPorts = midiOut.getPortCount()
    if outputPorts:
        midiOut.openPort(0)
    else:
        print("No MIDI output ports available.")
        return

    midiOut.openVirtualPort("MyVirtualDevice")
    print("Press Ctrl+C to exit.")
    holdCondition = False

    try:
        while True:
            msg = midiIn.getMessage()
            if msg:
                if msg.isController():
                    channel = msg.getChannel()
                    CCNumber = msg.getControllerNumber()
                    CCValue = msg.getControllerValue()

                    if channel == 1 and CCNumber == 108:
                        if CCValue == 127:
                            holdCondition = True
                        else:
                            holdCondition = False

                    knobs = range(21,29)
                    if holdCondition and channel == 16 and CCNumber in knobs:
                        new_msg = rtmidi.MidiMessage.controllerEvent(16, CCNumber+30, CCValue)
                        msg = new_msg
                        print(new_msg)

                    upDownButtons = range(104, 106)
                    if holdCondition and channel == 1 and CCNumber in upDownButtons:
                        new_msg = rtmidi.MidiMessage.controllerEvent(16, CCNumber+2, CCValue)
                        msg = new_msg
                        print(new_msg)

                    playRecordButtons = range(115, 118)
                    if holdCondition and channel == 16 and CCNumber in playRecordButtons:
                        new_msg = rtmidi.MidiMessage.controllerEvent(16, CCNumber+1, CCValue)
                        msg = new_msg
                        print(new_msg)
                print(msg)
                midiOut.sendMessage(msg)
                

    except KeyboardInterrupt:
        pass

    midiIn.closePort()
    midiOut.closePort()


midiPassthrough()
