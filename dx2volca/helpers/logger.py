import sys
import time

class Logger(object):
    def __init__(self, verbosity=4, use_colors=True, log_file = None):
        super(Logger, self).__init__()
        # STATIC!!
        Logger.verbosity_level = verbosity
        Logger.use_colors = use_colors
        Logger.log_file = log_file
        # ---

        # private
        self.private_verbosity = verbosity
        return

    def error(self, msg):
        caller_str = self._get_caller_name()
        self.write(msg, verbosity=1, caller=caller_str)

    def warning(self, msg):
        caller_str = self._get_caller_name()
        self.write(msg, verbosity=2, caller=caller_str)

    def info(self, msg):
        caller_str = self._get_caller_name()
        self.write(msg, verbosity=3, caller=caller_str)

    def debug(self, msg):
        caller_str = self._get_caller_name()
        self.write(msg, verbosity=4, caller=caller_str)

    def write(self, msg, verbosity=3, caller=None):
        """
        verbosity:
        0: none
        1: errors
        2: warnings
        3: info
        4: debug
        """
        msg = str(msg)
        color = "no"
        msg_type = ""
        if verbosity == 1:
            color = "red"
            msg_type = "[ERROR]"
        elif verbosity == 2:
            color = "yellow"
            msg_type = "[WARNING]"
        elif verbosity == 4:
            color = "blue"
            msg_type = "[DEBUG]"
        
        if not(caller):
            caller = self._get_caller_name()

        log_string = self._get_time() + " [DX2VOLCA:" + caller + "]" + msg_type + " " + msg
        
        if self.log_file:
            f = open(self.log_file, "a+")
            f.write(log_string + "\n")
            f.close()

        if verbosity <= self.verbosity_level:
            if verbosity <= self.private_verbosity:
                log_string = self._set_color(log_string, color)
                print(log_string)
        return

    def _get_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def _get_caller_name(self):
        f = list(sys._current_frames().values())[0]
        caller = (f.f_back.f_back.f_globals['__file__']).split("/")[-1].split(".")[0]
        return caller.upper()

    def _set_color(self, msg, color):
        colors = {"red" : "\033[91m", "green" : "\033[92m", "yellow" : "\033[93m", "blue" : "\033[94m","no" : "\033[0m"}
        if self.use_colors:
            msg = colors[color] + msg + colors["no"]
        return msg
    
    # static method:
    @staticmethod
    def set_verbosity(verbosity):
        if verbosity in range(0, 5):
            Logger.verbosity_level = verbosity
        return
