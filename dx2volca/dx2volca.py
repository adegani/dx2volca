import sys
# import threading
import time

# try:
#     import Queue as queue
# except ImportError:  # Python 3
#     import queue

from dx2volca.helpers import logger
from dx2volca.helpers import midi
from dx2volca.helpers import dx7parser

log = logger.Logger()
midi_device = midi.Midi()
msg_parser = dx7parser.Dx7Parser()

def main():
    # log.info("sono nel main")
    select_midi_out_port()
    
    # print("Entering main loop. Press Control-C to exit.")
    # dispatcher = MidiDispatcher(midi_device.midiin, midi_device.midiout)
    # try:
    #     dispatcher.start()
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     dispatcher.stop()
    #     dispatcher.join()
    #     print('')
    # finally:
    #     print("Exit.")
    
    print("Entering main loop. Press Control-C to exit.")
    # midiin = midi_device.midiin
    log.debug("Attaching MIDI input callback handler.")
    midi_device.midiin.set_callback(MidiInputHandler("dx2volca in", sysex_handler))
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midi_device.midiin.close_port()
        # del midi_device.midiin

    # print("Entering main loop. Press Control-C to exit.")
    # midiin = midi_device.midiin
    # try:
    #     timer = time.time()
    #     while True:
    #         msg = midiin.get_message()

    #         if msg:
    #             message, deltatime = msg
    #             timer += deltatime
    #             print("[%s] @%0.6f %r" % ("port_name", timer, message))

    #         time.sleep(0.01)
    # except KeyboardInterrupt:
    #     print('')
    # finally:
    #     print("Exit.")
    #     midiin.close_port()
    #     del midiin

def sysex_handler(msg):
    msg = msg_parser.parse(msg)
    midi_device.send_raw_byte_list(msg)

def select_midi_out_port():
    available_ports = midi_device.midiout.get_ports()
        
    selected_port = None
    selection_ok = False
    while(not selection_ok):
        print("")
        print("Available OUT ports")
        c = 0
        for port in available_ports:
            print("%d- %s" % (c, port))
            c += 1
        try:
            input_selection = input("Please select an output port (ENTER for creating a virtual port): ")
            if input_selection == "":
                selection_ok = True
                selected_port = None
            selected_port = int(input_selection)
        except:
            pass
        if selected_port in range(len(available_ports)):
            selection_ok = True

    if selected_port is None:
        midi_device.midiout.open_virtual_port("dx2volca out")
        print("Selected port: VIRTUAL (dx2volca out)")
    else:
        midi_device.midiout.open_port(selected_port)
        print("Selected port: %d (%s)" % (selected_port, available_ports[selected_port]))
    
    res = midi_device.midiin.open_virtual_port("dx2volca in")
    midi_device.midiin.ignore_types(sysex=False)
    

class MidiInputHandler(object):
    def __init__(self, port, sysex_handler):
        self.port = port
        self.sysex_handler = sysex_handler
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        log.debug("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        if message[0] == 240:
            # It is a sysex message
            self.sysex_handler(message)

# class MidiDispatcher(threading.Thread):
#     def __init__(self, midiin, midiout):
#         super(MidiDispatcher, self).__init__()
#         self.midiin = midiin
#         self.midiout = midiout
#         self._wallclock = time.time()
#         self.queue = queue.Queue()

#     def __call__(self, event, data=None):
#         message, deltatime = event
#         self._wallclock += deltatime
#         log.debug("IN: @%0.6f %r", self._wallclock, message)
#         self.queue.put((message, self._wallclock))

#     def run(self):
#         log.debug("Attaching MIDI input callback handler.")
#         self.midiin.set_callback(self)

#         while True:
#             event = self.queue.get()

#             if event is None:
#                 break

#             events = [event]

#             for event in events:
#                 log.debug("Out: @%0.6f %r", event[1], event[0])
#                 self.midiout.send_message(event[0])

#     def stop(self):
#         self.queue.put(None)

# if __name__ == "__main__":
#     main()