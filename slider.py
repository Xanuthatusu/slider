import gtk
import pygtk

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

	def readImageFile(self, imagefilename):
		self.image = gtk.Image()
		self.image.set_from_file(imagefilename)
		self.full_pixbuf = gtk.Image.get_pixbuf(self.image)
		self.full_width = self.full_pixbuf.get_width()
		self.full_height = self.full_pixbuf.get_height()

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
		self.createMenuItem("Solve", self.solve_handler, 2)
		self.createMenuItem("Quit", self.destroy_handler, 3)
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
				button = gtk.Button()
				image = gtk.Image()
				image.set_from_pixbuf(self.pixbufs[self.curx])
				button.add(image)
				self.buttons.append(button)
				button.connect("clicked", self.clicked_handler, [xpos, ypos])
				self.table.attach(button, xpos, xpos + 1, ypos, ypos + 1)
				self.curx += 1
		self.main_vbox.pack_start(self.table)

	def delete_handler(self, widget, event, data):
		return False

	def destroy_handler(self, widget, data):
		self.window.destroy()
		gtk.main_quit()

	def restart_handler(self, widget, data):
		print "restart"

	def solve_handler(self, widget, data):
		print "solve"

	def clicked_handler(self, widget, data):
		print "clicked"
		print data

	def run(self):
		gtk.main()

def main():
	s = SliderGUI(4, "smiley.gif")
	s.run()
main()