#!/usr/bin/env python

# example helloworld2.py

import pygtk
import gtk


class Main:
	def delete_event(self, widget, event, data=None):
		print "delete_event occured!"
		gtk.main_quit()
		return False


	def __init__(self):
		# Create a new window
		self.window = gtk.Window()

		# This is a new call, which just sets the title of our
		# new window to "Hello Buttons!"
		self.window.set_title("Slider")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(400,125)

		# Here we just set a handler for delete_event that immediately
		# exits GTK.
		self.window.connect("delete_event", self.delete_event)

		# Sets the border width of the window.
		self.window.set_border_width(10)

		self.vBox = gtk.VBox()
		self.label = gtk.Label("Test")
		self.vBox.pack_start(self.label)
		self.window.add(self.vBox)
		self.window.show_all()


def main():
	gtk.main()

if __name__ == "__main__":
	hello = Main()
	main()