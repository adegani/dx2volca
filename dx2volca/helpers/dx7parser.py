from dx2volca.helpers import logger

log = logger.Logger()

class Dx7Parser(object):
    def __init__(self, enable_translation=True):
        self.enable_translation = enable_translation
        self.sysex_marker = 240
        self.sysex_id = 67
        pass

    def translation_enabled(value=True):
        self.enable_translation = value

    def parse(self, msg):
        out_msg = list.copy(msg)

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
        if not self.enable_translation:
            return msg
        return msg

    def _print_32voice_data_info(self, msg):
        pass

    def _print_param_change_info(self, msg):
        pass

    def _get_msg_type(self, msg):

        if msg[0] != self.sysex_marker:
            log.warning("Message is not a SYSEX (marker %d)" % msg[0])
            return -1
        if msg[1] != self.sysex_id:
            log.warning("Message is not a SYSEX for Tamaha DX7 (id %d)" % msg[1])
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
        
