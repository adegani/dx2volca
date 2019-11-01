import sys
import time

from dx2volca.helpers import logger
from dx2volca.helpers import midi_helper
from dx2volca.helpers import dx7parser

DEV_NAME = "dx2volca"
DEV_NAME_IN = DEV_NAME + " IN"
DEV_NAME_OUT = DEV_NAME + " OUT"

log = logger.Logger()
midi_device = midi_helper.MidiHelper(DEV_NAME)
msg_parser = dx7parser.Dx7Parser()

def main():
    select_midi_ports()
    
    print("Entering main loop. Press Control-C to exit.")
    log.debug("Attaching MIDI input callback handler.")
    midi_device.midiin.set_callback(MidiInputHandler(DEV_NAME_IN, midi_handler))
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    except Exception as e:
        print(e)
    finally:
        print("Exit.")
        midi_device.midiin.close_port()

def midi_handler(msg):
    if msg[0] == 240:
        # If the msg is a sysex, parse it ...
        msg = msg_parser.parse(msg)
    # MIDI thru
    midi_device.send_raw_byte_list(msg)

def select_midi_ports():
    # list of available input ports
    available_ports = midi_device.midiin.get_ports()
        
    selected_port = None
    selection_ok = False
    while(not selection_ok):
        print("")
        print("Available IN ports")
        for portnum, portname in enumerate(available_ports):
            print("%d- %s" % (portnum, portname))
        try:
            input_selection = input("Select an input port (ENTER for new virtual port): ")
            if input_selection == "":
                selection_ok = True
                selected_port = None
            selected_port = int(input_selection)
        except:
            pass
        if selected_port in range(len(available_ports)):
            selection_ok = True

    if selected_port is None:
        # open a virtual port
        midi_device.midiin.open_virtual_port(DEV_NAME_OUT)
        print("Selected port: VIRTUAL (%s)" % DEV_NAME_OUT)
    else:
        # open selected port
        midi_device.midiin.open_port(selected_port)
        print("Selected port: %d (%s)" % (selected_port, available_ports[selected_port]))
    
    # list of available output ports
    available_ports = midi_device.midiout.get_ports()
        
    selected_port = None
    selection_ok = False
    while(not selection_ok):
        print("")
        print("Available OUT ports")
        for portnum, portname in enumerate(available_ports):
            print("%d- %s" % (portnum, portname))
        try:
            input_selection = input("Select an output port (ENTER for new virtual port): ")
            if input_selection == "":
                selection_ok = True
                selected_port = None
            selected_port = int(input_selection)
        except:
            pass
        if selected_port in range(len(available_ports)):
            selection_ok = True

    if selected_port is None:
        # open a virtual port
        midi_device.midiout.open_virtual_port(DEV_NAME_OUT)
        print("Selected port: VIRTUAL (%s)" % DEV_NAME_OUT)
    else:
        # open selected port
        midi_device.midiout.open_port(selected_port)
        print("Selected port: %d (%s)" % (selected_port, available_ports[selected_port]))
    
    midi_device.midiin.ignore_types(sysex=False)
    

class MidiInputHandler(object):
    # MIDI msg handler
    def __init__(self, port, midi_handler):
        self.port = port
        self.midi_handler = midi_handler
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        log.debug("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        self.midi_handler(message)
