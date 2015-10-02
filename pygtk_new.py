#!/usr/bin/env python

from __future__ import print_function
import pygtk
import gtk
from users import *

users = Users()

class Main:
	def delete_event(self, widget, event, data=None):
		print("delete_event occured!")
		gtk.main_quit()
		return False

	def save(self, widget, data):
		if data and self.firstNameEntry.get_text() != "" and self.lastNameEntry.get_text() != "" and self.phoneNumEntry.get_text() != "" and self.emailEntry.get_text() != "":
			users.add(self.firstNameEntry.get_text(), (self.firstNameEntry.get_text(), self.lastNameEntry.get_text(), self.phoneNumEntry.get_text(), self.emailEntry.get_text()))
			users.save()
			self.initiate()

		elif data:
			dialog = gtk.Dialog("Error")
			dialog.set_position(gtk.WIN_POS_CENTER)
			dialog.set_size_request(200, 100)

			label = gtk.Label("Please fill all the boxes.")
			dialog.vbox.pack_start(label)

			dialog.add_button("Close", 1)

			dialog.vbox.show_all()

			dialog.run()
			dialog.destroy()
			
	def delAnswer(self, widget, data):
		if data == "yes":
			print("Deleting!")
			users.remove(self.list[self.curUser])
			self.initiate()
			users.save()
			self.next(None)
		else:
			print("Not Deleting!")

	def previous(self, widget):
		try:
			self.curUser -= 1
			self.firstNameLabel.set_text(self.list[self.curUser])
		except:
			self.curUser = len(users.lib)-1
			self.firstNameLabel.set_text(self.list[self.curUser])
		self.lastNameLabel.set_text(users.lib[self.list[self.curUser]][1])
		self.phoneNumLabel.set_text(users.lib[self.list[self.curUser]][2])
		self.emailLabel.set_text(users.lib[self.list[self.curUser]][3])

	def delete(self, widget):
		dialog = gtk.Dialog("Are you sure?")
		dialog.set_position(gtk.WIN_POS_CENTER)
		dialog.set_size_request(250, 75)

		label = gtk.Label("Are you sure you want to delete this user?")
		dialog.vbox.pack_start(label)

		button = dialog.add_button("Yes", 1)
		button.connect("clicked", self.delAnswer, "yes")

		button = dialog.add_button("No", 1)
		button.connect("clicked", self.delAnswer, "no")

		dialog.vbox.show_all()

		dialog.run()
		dialog.destroy()



	def add(self, widget):
		dialog = gtk.Dialog("Add User")
		dialog.set_border_width(10)
		dialog.set_size_request(500, 200)
		dialog.set_position(gtk.WIN_POS_CENTER)

		dialog.vbox.set_spacing(5)
		
		hBox = gtk.HBox()    
		box = gtk.VBox(True, 5)

		label = gtk.Label("First Name:")
		box.pack_start(label)

		label = gtk.Label("Last Name:")
		box.pack_start(label)

		label = gtk.Label("Phone Number:")
		box.pack_start(label)

		label = gtk.Label("Email Address:")
		box.pack_start(label)

		hBox.pack_start(box)
		box = gtk.VBox(True, 5)

		self.firstNameEntry = gtk.Entry()
		box.pack_start(self.firstNameEntry)

		self.lastNameEntry = gtk.Entry()
		box.pack_start(self.lastNameEntry)

		self.phoneNumEntry = gtk.Entry()
		box.pack_start(self.phoneNumEntry)

		self.emailEntry = gtk.Entry()
		box.pack_start(self.emailEntry)

		hBox.pack_start(box)
		dialog.vbox.pack_start(hBox)

		button = dialog.add_button("Cancel", 1)
		button.connect("clicked", self.save, False)

		test = dialog.add_button("Sign Up!", 1)
		test.connect("clicked", self.save, True)

		dialog.vbox.show_all()

		dialog.run()
		dialog.destroy()

	def next(self, widget):
		try:
			self.curUser += 1
			self.firstNameLabel.set_text(self.list[self.curUser])
		except:
			self.curUser = 0
			self.firstNameLabel.set_text(self.list[self.curUser])
		self.lastNameLabel.set_text(users.lib[self.list[self.curUser]][1])
		self.phoneNumLabel.set_text(users.lib[self.list[self.curUser]][2])
		self.emailLabel.set_text(users.lib[self.list[self.curUser]][3])

	def initiate(self):
		self.list = []
		for i in users.lib:
			self.list.append(i)


	def __init__(self):
		# Create a new window
		self.initiate()
		self.curUser = 0
		self.window = gtk.Window()

		# This is a new call, which just sets the title of our
		# new window to "Hello Buttons!"
		self.window.set_title("Dictionary")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(400,125)
		#self.window.set_opacity(0.9)

		# Here we just set a handler for delete_event that immediately
		# exits GTK.
		self.window.connect("delete_event", self.delete_event)

		# Sets the border width of the window.
		self.window.set_border_width(10)

		self.vBox = gtk.VBox()

		self.hBox = gtk.HBox(True, 0)

		self.box = gtk.VBox(True, 5)

		self.label = gtk.Label("First Name:")
		self.box.pack_start(self.label)

		self.label = gtk.Label("Last Name:")
		self.box.pack_start(self.label)

		self.label = gtk.Label("Phone Number:")
		self.box.pack_start(self.label)

		self.label = gtk.Label("Email:")
		self.box.pack_start(self.label)

		self.hBox.pack_start(self.box)
		self.vBox.pack_start(self.hBox)
		self.box = gtk.VBox()

		self.firstNameLabel = gtk.Label(users.lib[self.list[self.curUser]][0])
		self.box.pack_start(self.firstNameLabel)

		self.lastNameLabel = gtk.Label(users.lib[self.list[self.curUser]][1])
		self.box.pack_start(self.lastNameLabel)

		self.phoneNumLabel = gtk.Label(users.lib[self.list[self.curUser]][2])
		self.box.pack_start(self.phoneNumLabel)

		self.emailLabel = gtk.Label(users.lib[self.list[self.curUser]][3])
		self.box.pack_start(self.emailLabel)

		self.hBox.pack_start(self.box)

		self.box = gtk.HBox(True, 5)

		self.button = gtk.Button("<< Previous")
		self.button.connect("clicked", self.previous)
		self.box.pack_start(self.button)

		self.button = gtk.Button("Delete")
		self.button.connect("clicked", self.delete)
		self.box.pack_start(self.button)

		self.button = gtk.Button("Add")
		self.button.connect("clicked", self.add)
		self.box.pack_start(self.button)

		self.button = gtk.Button("Next >>")
		self.button.connect("clicked", self.next)
		self.box.pack_start(self.button)

		self.vBox.pack_start(self.box)
		
		self.window.add(self.vBox)
		self.window.show_all()


def main():
	gtk.main()

if __name__ == "__main__":
	hello = Main()
	main()
