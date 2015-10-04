import gtk ,pygtk
from sliderLogic import SliderLogic

class SliderGUI():
	def __init__(self, size, imagefilename):
		self.pixbufs = []
		self.images = []
		self.buttons = []
		self.size = size
		self.readImageFile(imagefilename)
		self.createWindow()
		self.createBtnImages()
		self.createMenu()
		self.createGame()
		self.window.show_all()
		self.logic = SliderLogic(self.size)
		self.updateDisplay()

	def readImageFile(self, imagefilename):
		self.test = gtk.gdk.pixbuf_new_from_file_at_size(imagefilename, 300, 300)
		self.image = gtk.Image()
		#self.image.set_from_file(imagefilename)
		self.image.set_from_pixbuf(self.test)
		#self.full_pixbuf = gtk.Image.get_pixbuf(self.image)
		self.full_pixbuf = self.test
		self.full_width = self.full_pixbuf.get_width()
		self.full_height = self.full_pixbuf.get_height()
		print self.full_width, self.full_height

	def createWindow(self):
		self.window = gtk.Window()
		self.window.set_title("Slider")
		self.window.connect("delete_event", self.delete_handler, None)
		self.window.connect("destroy_event", self.destroy_handler, None)


	def createBtnImages(self):
		self.cell_width = self.full_width / self.size
		self.cell_height = self.full_height / self.size
		for yval in range (0, self.full_height, self.cell_height):
			for xval in range (0, self.full_width, self.cell_width):
					subpixbuf = self.full_pixbuf.subpixbuf(xval, yval, 
						self.cell_width, self.cell_height)
					self.pixbufs.append(subpixbuf)

	def createMenuItem(self, title, handler, num):
		self.menuItem = gtk.MenuItem(title)
		self.menuItem.connect("activate", handler, None)
		self.menu.attach(self.menuItem, 0, 1, num - 1, num)

	def createMenu(self):
		self.main_vbox = gtk.VBox()
		self.menu = gtk.Menu()
		self.createMenuItem("New Game", self.restart_handler, 1)
		self.createMenuItem("Solve", self.solve_handler, 4)
		self.createMenuItem("Quit", self.destroy_handler, 3)
		self.createMenuItem("Choose Image", self.fileChooser, 2)
		self.root_menu = gtk.MenuItem("Game")
		self.root_menu.set_submenu(self.menu)
		self.menuBar = gtk.MenuBar()
		self.menuBar.append(self.root_menu)
		self.main_vbox.pack_start(self.menuBar)
		self.window.add(self.main_vbox)

	def createGame(self):
		self.table = gtk.Table(self.size, self.size, True)
		self.curx = 0
		for ypos in range(self.size):
			for xpos in range(self.size):
				self.button = gtk.Button()
				image = gtk.Image()
				image.set_from_pixbuf(self.pixbufs[self.curx])
				self.button.add(image)
				self.images.append(image)
				self.buttons.append(self.button)
				self.button.connect("clicked", self.clicked_handler, self.curx)
				self.table.attach(self.button, xpos, xpos + 1, ypos, ypos + 1)
				self.curx += 1
		self.main_vbox.pack_start(self.table)

	def delete_handler(self, widget, event, data):
		return False

	def destroy_handler(self, widget, data):
		self.window.destroy()
		gtk.main_quit()

	def restart_handler(self, widget, data):
		self.logic.restart()
		self.logic.shuffle(self.size * 25)
		self.updateDisplay()

	def solve_handler(self, widget, data):
		print "solve"
		self.logic.solveStep()
		print "done"
		self.updateDisplay()


	def clicked_handler(self, widget, data):
		self.logic.takeTurn(data)
		self.updateDisplay()

	def run(self):
		gtk.main()

	def updateDisplay(self):
		holePos = self.logic.holePos
		for i in range(self.size**2):
			if self.logic.list[i] == -1:
				self.buttons[i].hide()
			else:
				self.buttons[i].show()
				temp = self.logic.getCell(i)
				pixbuf = self.pixbufs[temp]
				curImg = self.images[i]
				curImg.set_from_pixbuf(pixbuf)
		count = 0
		for i in self.logic.list:
			if i == count:
				count += 1
			elif count >= self.size**2-1:
				dialog = gtk.Dialog("You Win!!")
				dialog.add_button("Yay!", 1)
				label = gtk.Label("Congratulations!! You beat the game in " + str(self.logic.countMoves) + " moves!!!")
				dialog.vbox.pack_start(label)
				dialog.vbox.show_all()
				dialog.run()
				dialog.destroy()

			else:
				count = 0
				break

	def fileChooser(self, widget, event):
		print "choose"

		dialog = gtk.FileChooserDialog("Open...", None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk. RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))

		dialog.set_default_response(gtk.RESPONSE_OK)
		filter = gtk.FileFilter()
		filter.set_name("Images")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/gif")
		filter.add_mime_type("image/jpeg")
		filter.add_pattern("*.png")
		filter.add_pattern("*.gif")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.jpeg")
		dialog.add_filter(filter)

		self.response = dialog.run()
		if self.response == gtk.RESPONSE_OK:
			print self.response
			self.window.destroy()
			self.__init__(self.size, dialog.get_filename())
		elif self.response == gtk.RESPONSE_CANCEL:
			print "No file chosen!"

		dialog.destroy()

def main():
	size = 5
	s = SliderGUI(size, "smiley.gif")
	s.run()
main()