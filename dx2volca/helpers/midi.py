import time
import rtmidi

class Midi():

    def __init__(self, name=None):
        self.name = name
        if self.name == None:
            self.midiout = rtmidi.MidiOut(name="dx2volca")
            self.midiin = rtmidi.MidiIn(name="dx2volca")
        else:
            self.midiout = rtmidi.MidiOut(name="dx2volca " + self.name)
            self.midiin = rtmidi.MidiIn(name="dx2volca " + self.name)
        
        return

    def __del__(self):
        del self.midiout
        del self.midiin

    def send_note_on(self, note, velocity, channel=0):
        channel = int(max(min(channel, 15),0))
        if isinstance(note,list):
            note = note[0]
        note = int(max(min(note,127),0))
        velocity = int(max(min(velocity,127),0))
        msg = [144 + channel, note, velocity]
        self.midiout.send_message(msg)
        return

    def send_note_off(self, note, channel=0):
        channel = int(max(min(channel, 15),0))
        note = int(max(min(note,127),0))
        msg = [128 + channel, note, 0]
        self.midiout.send_message(msg)
        return

    def send_control_change(self, cc, val, channel=0):
        channel = int(max(min(channel, 15),0))
        cc = int(max(min(cc,127),0))
        val = int(max(min(val,127),0))
        msg = [128 + channel, cc, val]
        self.midiout.send_message(msg)
        return
    
    def send_pitch_bend(self, val, channel=0):
        # center: 0 -> 8192
        channel = int(max(min(channel, 15),0))
        val = val + 8192
        val = int(max(min(val,16383),0))
        lsb = val & 128
        msb = (val/2) & 128
        msg = [128 + channel, lsb, msb]
        self.midiout.send_message(msg)
        return

    def send_program_change(self, program, channel=0):
        channel = int(max(min(channel, 15),0))
        program = int(max(min(program,127),0))
        msg = [192 + channel, program]
        self.midiout.send_message(msg)
        return

    def send_all_note_off(self, channel=None):
        if channel == None:
            for ch in range(16):
                msg = [176 + ch, 123, 0]
                self.midiout.send_message(msg)
        else:
            channel = int(max(min(channel, 15),0))
            msg = [176 + channel, 123, 0]
            self.midiout.send_message(msg)
        return
    
    def send_raw_byte_list(self, byte_list):
        # print(byte_list)
        msg = []
        for b in list(byte_list):
            # uint8 casting
            msg.append(int(b) & 255)

        self.midiout.send_message(msg)
        return