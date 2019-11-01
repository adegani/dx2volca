from dx2volca.helpers import logger

log = logger.Logger()

class Dx7Parser(object):
    """DX7 SYSEX parser and transalte

    This class parses the SYSEX messages sent to DX7 and thranslate the 1 Voice bulk data in order
    to behave correctly with Korg Volca FM
    """
    def __init__(self, enable_translation=True):
        """Class constructor
        
        Keyword Arguments:
            enable_translation {bool} -- Enbla real time SYSEX translation (default: {True})
        """
        self.enable_translation = enable_translation
        self.sysex_marker = 240
        self.sysex_id = 67
        self.sysex_end = 247
        return

    def translation_enabled(value=True):
        """Enable/Disable SYSEX transalation
        
        Keyword Arguments:
            value {bool} -- Enable translation if True (default: {True})
        """
        self.enable_translation = value

    def parse(self, msg):
        """Parse the SYSEX messages
        
        Arguments:
            msg {[list]} -- SYSEX message byte list
        
        Returns:
            [list] -- The translated SYSEX message, if applicable
        """
        out_msg = list.copy(msg)

        # Check message type and tke different actions
        msg_type = self._get_msg_type(msg)
        if msg_type == 0:
            # 1 Voice Bulk data
            out_msg = self._translate_and_print(msg)
        elif msg_type == 1:
            # 32 Voice Bulk data
            self._print_32voice_data_info(msg)
        elif msg_type == 2:
            # Parameter Change
            self._print_param_change_info(msg)

        return out_msg

    def _translate_and_print(self, msg):
        """If the SYSEX is a 1 voice bulk data, parse it and translate (if enabled)
        
        Arguments:
            msg {[list]} -- SYSEX message byte list
        
        Returns:
            [list] -- The translated SYSEX message, if applicable
        """
        if msg[-1] != self.sysex_end:
            log.warning("Malformed SYSEX (end: %d)" % msg[-1])
            return msg
        
        channel = (msg[2] & 15) + 1
        byte_count = int(msg[4]) * 128 + int(msg[5])
        voice_name = ''.join(chr(i) for i in msg[150:161])
        checksum = msg[-2]
        # THE FIX: all operator in ON
        # Korg Volca FM interprets the checksum byte as operator ON/OFF command
        msg[-2] = 63
        log.info("FIX: ALL operators are ON")
        log.debug("%s: 1 Voice bulk on ch %d, with %d bytes (CHECK: %s)" % (voice_name, channel, byte_count, checksum))
        return msg

    def _print_32voice_data_info(self, msg):
        pass

    def _print_param_change_info(self, msg):
        pass

    def _get_msg_type(self, msg):
        """Check the type of the DX7 SYSEX message
        
        Arguments:
            msg {[list]} -- SYSEX message byte list
        
        Returns:
            int -- Message type. 0 for 1 Voice bulk, 1 for 32 Voice bulk, 2 for par. change, -1 if not recognized
        """

        if msg[0] != self.sysex_marker:
            log.warning("Message is not a SYSEX (marker %d)" % msg[0])
            return -1
        if msg[1] != self.sysex_id:
            log.warning("Message is not a DX7 SYSEX (id %d)" % msg[1])
            return -1
        if len(msg) == 163:
            log.debug("Message is DX7 1 Voice Bulk data")
            return 0
        if len(msg) == 4104:
            log.debug("Message is DX7 32 Voice Bulk data")
            return 1
        if len(msg) == 7:
            log.debug("Message is DX7 Parameter Change")
            return 2

        log.warning("Message is DX7 SYSEX but not recognized (len=%d)" % len(msg))
        return -1
