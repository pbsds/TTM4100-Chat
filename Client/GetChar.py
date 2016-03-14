#non-blocking stdin read for asyncronus input

FILTER = set("abcdefghijklmnopqrstuvwxyz ,;.:-_'*!\"#%&/()=?@${[]}+\0123456789<>|\n\b")

def GetCharFiltered():
	k = GetChar()
	if k.lower() in FILTER:
		return k
	return ""

try:#windows
	import msvcrt
	def GetChar():
		if msvcrt.kbhit():
			k = msvcrt.getch()
			if k == "\r":	
				return "\n"
			return k
		return ""
except ImportError:#unix
	import tty, termios, signal, sys
	
	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch
		return ch
	class timeout:
		error_message = "Timeout"
		def __init__(self, seconds, error_message=None):
			self.seconds = seconds
			if error_message:
				self.error_message = error_message
		def handle_timeout(self, signum, frame):
			raise TimeoutError(self.error_message)
		def __enter__(self):
			signal.signal(signal.SIGALRM, self.handle_timeout)
			signal.alarm(self.seconds)
		def __exit__(self, type, value, traceback):
			signal.alarm(0)
	def GetChar():
		k = ""
		with timeout(0.02):
			k = getch()
		if ord(k) == 3:
			raise KeyboardInterrupt
		elif k == "\r":
			return "\n"
		elif k == "\x7f":
			return "\b"
		return k
