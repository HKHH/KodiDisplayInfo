import sys
import os


class Helper:

	def __init__(self, config_default):
		self.__config_default = config_default

	def get_default_kodilogo(self):
		return self.__config_default['basedirpath']+'img/kodi.png'
	
	def format_to_seconds(self, hours, minutes, seconds):
		try:
			if hours > 0:
				hours = hours * 3600
			if minutes > 0:
				minutes = minutes * 60
			return int(hours + minutes + seconds)
		except ValueError:
			self.printout("[warning]    ", self.__config_default['mesg.red'])
			self.printout('Converting time to seconds has failed!')
			return 0
	
	def format_to_minutes(self, hours, minutes):
		try:
			if hours > 0:
				hours = hours * 60
			return int(hours + minutes)
		except ValueError:
			self.printout("[warning]    ", self.__config_default['mesg.red'])
			self.printout('Converting time to minutes has failed!')
			return 0
		
	def format_to_string(self, hours, minutes, seconds, modus = "long"):
		try:
			if modus=="long":
				return str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)
			elif modus=="short":
				return str(self.format_to_minutes(hours, minutes)).zfill(2)+":"+str(seconds).zfill(2)
		except ValueError:
			self.printout("[warning]    ", self.__config_default['mesg.red'])
			self.printout('Padding time with zeroes has failed!')
			return ""
		
	# following from http://code.activestate.com/recipes/475186/
	@staticmethod
	def has_colours(stream):
		try:
			if not hasattr(stream, "isatty"):
				return False
			if not stream.isatty():
				return False  # auto color only on TTYs

			import curses
			curses.setupterm()
			return curses.tigetnum("colors") > 2
		except (Exception,):
			# guess false in case of error
			return False
	
	def printout(self, text, colour=""):
		if not colour:
			colour=self.__config_default['mesg.white']
		if self.has_colours(sys.stdout):
			seq = "\x1b[1;%dm" % colour + text + "\x1b[0m"
			sys.stdout.write(seq)
		else:
			sys.stdout.write(text+"\n")
			
	# following from http://code.activestate.com/recipes/266466/
	def html_color_to_rgb(self, colorstring):
		try:
			""" convert #RRGGBB to an (R, G, B) tuple """
			colorstring = colorstring.strip()
			if colorstring[0] == '#': colorstring = colorstring[1:]
			if len(colorstring) != 6:
				self.printout("input #"+colorstring+" is not in #RRGGBB format")
			r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
			r, g, b = [int(n, 16) for n in (r, g, b)]
			return r, g, b
		except ValueError as text:
			self.printout("[error]   ", self.__config_default['mesg.red'])
			self.printout("Color Error RGB! " + str(text))
			exit()
			
	# following from http://pygame.org/wiki/TextWrapping
	@staticmethod
	def truncline(text, font, maxwidth):
		real=len(text)	   
		stext=text		   
		l=font.size(text)[0]
		cut=0
		a=0				  
		done=1
		while l > maxwidth:
			a=a+1
			n=text.rsplit(None, a)[0]
			if stext == n:
				cut += 1
				stext= n[:-cut]
			else:
				stext = n
			l=font.size(stext)[0]
			real=len(stext)			   
			done=0						
		return real, done, stext			 
		
	def wrapline(self, text, font, maxwidth): 
		done=0					  
		wrapped=[]
		while not done:			 
			nl, done, stext=self.truncline(text, font, maxwidth) 
			wrapped.append(stext.strip())				  
			text=text[nl:]								 
		return wrapped

	@staticmethod
	def disk_usage(path, what =""):
		st = os.statvfs(path)
		free = st.f_bavail * st.f_frsize
		total = st.f_blocks * st.f_frsize
		used = (st.f_blocks - st.f_bfree) * st.f_frsize
		percent = round(100 - ( 1. * free/total ) * 100, 2)

		if what == "":
			return total, used, free, percent
		elif what == "percent":
			return percent

	@staticmethod
	def check_file(file):
		return os.path.isfile(file)