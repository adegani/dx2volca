import time
import rtmidi
from rtmidi import midiconstants

class MidiHelper():
    """Midi helper Class
    """

    def __init__(self, dev_name="rtmidi"):
        """MidiHelper contructor
        
        Keyword Arguments:
            dev_name {str} -- MIDI device name (default: {"rtmidi"})
        """
        self.name = dev_name

        self.midiout = rtmidi.MidiOut(name=dev_name)
        self.midiin = rtmidi.MidiIn(name=dev_name)
        
        return

    def __del__(self):
        del self.midiout
        del self.midiin

    def send_note_on(self, note, velocity, channel=0):
        """Send a MIDI NOTE_ON message
        
        Arguments:
            note {int} -- MIDI note to be sent
            velocity {int} -- Velocity
        
        Keyword Arguments:
            channel {int} -- MIDI channel (default: {0})
        """
        channel = int(max(min(channel, 15),0))
        if isinstance(note,list):
            note = note[0]
        note = int(max(min(note,127),0))
        velocity = int(max(min(velocity,127),0))
        msg = [NOTE_ON + channel, note, velocity]
        self.midiout.send_message(msg)
        return

    def send_note_off(self, note, channel=0):
        """Send a MIDI NOTE_OFF message
        
        Arguments:
            note {int} -- MIDI note to be sent
        
        Keyword Arguments:
            channel {int} -- MIDI channel (default: {0})
        """
        channel = int(max(min(channel, 15),0))
        note = int(max(min(note,127),0))
        msg = [NOTE_OFF + channel, note, 0]
        self.midiout.send_message(msg)
        return

    def send_control_change(self, cc, val, channel=0):
        """Send a MIDI Control Change message
        
        Arguments:
            cc {int} -- Control change parameter number
            val {int} -- Value of the parameter
        
        Keyword Arguments:
            channel {int} -- MIDI channel (default: {0})
        """
        channel = int(max(min(channel, 15),0))
        cc = int(max(min(cc,127),0))
        val = int(max(min(val,127),0))
        msg = [CONTROL_CHANGE + channel, cc, val]
        self.midiout.send_message(msg)
        return
    
    def send_pitch_bend(self, val, channel=0):
        """Send a MIDI Pitch Bend signal
        
        Arguments:
            val {int} -- Pitch bend value from 0 to near 16000
        
        Keyword Arguments:
            channel {int} -- MIDI channel (default: {0})
        """
        # center: 0 -> 8192
        channel = int(max(min(channel, 15),0))
        val = val + 8192
        val = int(max(min(val,16383),0))
        lsb = val & 128
        msb = (val/2) & 128
        msg = [PITCH_BEND + channel, lsb, msb]
        self.midiout.send_message(msg)
        return

    def send_program_change(self, program, channel=0):
        """Send MIDI Program Change
        
        Arguments:
            program {int} -- MIDI program index
        
        Keyword Arguments:
            channel {int} -- MIDI channel (default: {0})
        """
        channel = int(max(min(channel, 15),0))
        program = int(max(min(program,127),0))
        msg = [PROGRAM_CHANGE + channel, program]
        self.midiout.send_message(msg)
        return

    def send_all_note_off(self, channel=None):
        """Send a MIDI ALL_NOTE_OFF message
        
        Keyword Arguments:
            channel {int} -- MIDI Channel, if None send to all channels (default: {None})
        """
        if channel == None:
            for ch in range(16):
                msg = [CONTROL_CHANGE + ch, ALL_NOTES_OFF, 0]
                self.midiout.send_message(msg)
        else:
            channel = int(max(min(channel, 15),0))
            msg = [CONTROL_CHANGE + channel, ALL_NOTES_OFF, 0]
            self.midiout.send_message(msg)
        return

    def send_panic(self, channel=None):
        """MIDI PANIC! message
        
        Keyword Arguments:
            channel {int} -- MIDI channel, if None sent to all channels (default: {None})
        """
        if channel == None:
            for ch in range(16):
                msg_all_off = [CONTROL_CHANGE + ch, ALL_SOUND_OFF, 0]
                msg_reset_all = [CONTROL_CHANGE + ch, RESET_ALL_CONTROLLERS, 0]
                self.midiout.send_message(msg_all_off)
                self.midiout.send_message(msg_reset_all)
                time.sleep(0.05)
        else:
            channel = int(max(min(channel, 15),0))
            msg_all_off = [CONTROL_CHANGE + channel, ALL_SOUND_OFF, 0]
            msg_reset_all = [CONTROL_CHANGE + channel, RESET_ALL_CONTROLLERS, 0]
            self.midiout.send_message(msg_all_off)
            self.midiout.send_message(msg_reset_all)
            time.sleep(0.05)

        time.sleep(0.1)
    
    def send_raw_byte_list(self, byte_list):
        """Send raw byte list to MIDI
        
        Arguments:
            byte_list {[list]} -- List of bytes to be sent
        """
        msg = []
        for b in list(byte_list):
            # uint8 casting
            msg.append(int(b) & 255)

        self.midiout.send_message(msg)
        return
