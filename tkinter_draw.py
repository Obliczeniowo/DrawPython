################################################################################
# Authot: Krzysztof Zajączkowski ###############################################
# Home page: Obliczeniowo.com.pl ###############################################
################################################################################
# Licence: GPL #################################################################
################################################################################
# Wolno rozpowszechniać niniejsze oprogramowanie i je udoskonalać pod ##########
# warunkiem, że: ###############################################################
################################################################################
# 1) nie będziesz rozpowszechniał oprogramowania mego na innej licencji niż ta #
# 2) nie usuniesz nazwiska mego (jako autora lub współautora) ani linku do #####
#    strony mojej! #############################################################
################################################################################

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser as cch
import tkinter.filedialog as fd
import tkinter.messagebox as msb

################################################################################
# function strToDict ###########################################################
################################################################################
def strToDict(string):
	"""
	This function change string to a dictionary. String must be in form:
	key1="value1";key2="value2"
	example:
	string = 'key1="value1";key2="value2"'
	dictionary = strToDict(string) <- this retur dictionary
	{key1: "value1", key2: "value2"}
	"""
	strList = string.split("\";")
	dictionary = {}
	for item in strList:
		l = item.split("=\"", 1)
		dictionary[l[0]] = l[1].strip('\n').strip('"')
	return dictionary
################################################################################
# DrawingObject class ##########################################################
################################################################################
class DrawingObject:
	def __init__(self, id, canvas):
		"""
		Each drawing object class like a Ellipse or Rectangle etc. must have
		this class as a parent. Constructor of this class get two parameters
		id - id of canvas object
		canvas - Canvas class object
		"""
		self.id = id
		self.canvas = canvas
	def remove(self):
		self.canvas.delete(self.id)
	def __eq__(self, other):
		return other == self.id
################################################################################
# Rectangle class ##############################################################
################################################################################
class Rectangle(DrawingObject):
	def __init__(self, x1, y1, x2, y2, canvas, fill = "", outline = "", width = 1):
		"""
		Rectangle calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Rectnagle(x1, y1, x2, y2, canvas, fill, outline, width)
		coordinate arguments:
		x1 - x coordinate of left edge of rectangle
		y1 - y coordinate of top edge of rectangle
		x2 - x coordinate of right edge of rectangle
		y2 - y coordinate of bottom edge of rectangle
		Canvas:
		canvas - object of class Canvas widget
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_rectangle(x1, y1, x2, y2, fill = fill, outline = outline, width = width), canvas)
		self.x = x1
		self.y = y1
	def setEnd(self, x2, y2):
		width = x2 - self.x
		height = y2 - self.y
		self.canvas.coords(self.id, min(x2, self.x), min(y2, self.y), max(x2, self.x), max(y2, self.y))
	def __str__(self):
		coords = self.canvas.coords(self.id)
		config = self.canvas.itemconfig(self.id)
		return "type=\"Rectangle\";x1=\"{x1}\";y1=\"{y1}\";x2=\"{x2}\";y2=\"{y2}\";fill=\"{fill}\";outline=\"{outline}\";width=\"{width}\"".format(x1 = coords[0], y1 = coords[1], x2 = coords[2], y2 = coords[3], fill = config["fill"][4], outline = config["outline"][4], width = config["width"][4])
	@staticmethod
	def GetObject(dictionary, canvas):
		if dictionary["type"] == "Rectangle":
			return Rectangle(float(dictionary["x1"]), float(dictionary["y1"]), float(dictionary["x2"]), float(dictionary["y2"]), canvas, fill = dictionary["fill"], outline = dictionary["outline"], width = float(dictionary["width"]))
		return None
################################################################################
# Ellipse class ################################################################
################################################################################
class Ellipse(DrawingObject):
	def __init__(self, x1, y1, x2, y2, canvas, fill = "", outline = "", width = 1):
		"""
		Ellipse calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Ellipse(x1, y1, x2, y2, canvas, fill, outline, width)
		coordinate arguments:
		x1 - x coordinate of left edge of rectangle in witch ellipse is
		y1 - y coordinate of top edge of rectangle in witch ellipse is
		x2 - x coordinate of right edge of rectangle in witch ellipse is
		y2 - y coordinate of bottom edge of rectangle in witch ellipse is
		Canvas:
		canvas - object of Canvas class
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_oval(x1, y1, x2, y2, fill = fill, outline = outline, width = width), canvas)
	def center(self):
		coords = self.canvas.coords(self.id)
		return ((coords[2] - coords[0]) * .5 + coords[0], (coords[1] - coords[3]) * .5 + coords[3])
	def rays(self, center, x2, y2):
		rx = center[0] - x2
		rx = -rx if rx < 0 else rx;
		ry = center[1] - y2
		ry = -ry if ry < 0 else ry;
		print("rx = {rx}, ry = {ry}".format(rx = rx, ry = ry))
		return ( rx , ry )
	def setEnd(self, x2, y2):
		center = self.center()
		rays = self.rays(center, x2, y2)
		self.canvas.coords(self.id, center[0] - rays[0], center[1] - rays[1], center[0] + rays[0], center[1] + rays[1])
	def __str__(self):
		coords = self.canvas.coords(self.id)
		config = self.canvas.itemconfig(self.id)
		print(config["fill"])
		return "type=\"Ellipse\";x1=\"{x1}\";y1=\"{y1}\";x2=\"{x2}\";y2=\"{y2}\";fill=\"{fill}\";outline=\"{outline}\";width=\"{width}\"".format(x1 = coords[0], y1 = coords[1], x2 = coords[2], y2 = coords[3], fill = config["fill"][4], outline = config["outline"][4], width = config["width"][4])
	@staticmethod
	def GetObject(dictionary, canvas):
		if dictionary["type"] == "Ellipse":
			return Ellipse(float(dictionary["x1"]), float(dictionary["y1"]), float(dictionary["x2"]), float(dictionary["y2"]), canvas, fill = dictionary["fill"], outline = dictionary["outline"], width = float(dictionary["width"]))
		return None
################################################################################
# Line class ###################################################################
################################################################################
class Line(DrawingObject):
	def __init__(self, x1, y1, x2, y2, canvas, outline = "", width = 1):
		"""
		Line calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Line(x1, y1, x2, y2, canvas, outline, width)
		coordinate arguments:
		x1 - x coordinate of first point
		y1 - y coordinate of first point
		x2 - x coordinate of last point
		y2 - y coordinate of last point
		Canvas:
		canvas - class object of Canvas widget
		other settings:
		fill - color of line, example "#ff0000" <- red color
		width - size of line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_line(x1, y1, x2, y2, fill = outline, width = width), canvas)# dash=(20,5) )
	def setEnd(self, x2, y2):
		coords = self.canvas.coords(self.id)
		self.canvas.coords(self.id, coords[0], coords[1], x2, y2)
	def __str__(self):
		coords = self.canvas.coords(self.id)
		config = self.canvas.itemconfig(self.id)
		return "type=\"Line\";x1=\"{x1}\";y1=\"{y1}\";x2=\"{x2}\";y2=\"{y2}\";fill=\"{fill}\";width=\"{width}\"".format(x1 = coords[0], y1 = coords[1], x2 = coords[2], y2 = coords[3], fill = config["fill"][4], width = config["width"][4])
	@staticmethod
	def GetObject(dictionary, canvas):
		if dictionary["type"] == "Line":
			return Line(float(dictionary["x1"]), float(dictionary["y1"]), float(dictionary["x2"]), float(dictionary["y2"]), canvas, outline = dictionary["fill"], width = float(dictionary["width"]))
		return None
################################################################################
# Polygon class ################################################################
################################################################################
class Polygon(DrawingObject):
	def __init__(self, coords, canvas, outline = "", fill = "", width = 1):
		"""
		Polygon calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Polygon(coords, canvas, outline, fill, width)
		coordinate arguments:
		coords - tuple or list of points [1, 3, 10, 5, 8, 6]
		Canvas:
		canvas - object of class Canvas
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_polygon(coords, fill = fill, outline = outline, width = width), canvas)
	def setEnd(self, x2, y2):
		coords = self.canvas.coords(self.id)
		coords += x2, y2
		self.canvas.coords(self.id, tuple(coords))
	def __str__(self):
		coords = self.canvas.coords(self.id)
		str_coords = ""
		for i in coords:
			str_coords += "{i},".format(i = i)
		str_coords = str_coords.strip(",")
		config = self.canvas.itemconfig(self.id)
		return "type=\"Polygon\";coords=\"{coords}\";fill=\"{fill}\";outline=\"{outline}\";width=\"{width}\"".format(coords = str_coords, fill = config['fill'][4], outline = config['outline'][4], width = float(config['width'][4]))
	def GetObject(dictionary, canvas):
		if dictionary["type"] == "Polygon":
			coords = dictionary["coords"].strip(",").split(",")
			if len(coords) == 0 or len(coords) % 2:
				return None
			for i in range(len(coords)):
				coords[i] = float(coords[i])
			return Polygon(coords, canvas, fill = dictionary["fill"], outline = dictionary["outline"], width = float(dictionary["width"]))
		return None
################################################################################
# Toolbar class ################################################################
################################################################################
class Toolbar(tk.Frame):
	def __init__(self, parent):
		"""
		Create toolbar control witch have inside togle buttons to control action of
		program
		Toolbar(parent)
		arguments:
		parent - parent widget.
		"""
		self.button_size = 25
		
		tk.Frame.__init__(self, parent)
		tk.Frame.place(self, in_ = parent, x = 0, y = 0, relwidth = 1., height = self.button_size)
		
		self.valueset = tk.StringVar()
		self.images = []
		
		self.buttons = []
	def add_button(self, title, image = ""):
		
		if len(self.buttons) == 0:
			self.valueset.set(title)
		button = tk.Radiobutton(self, text = title, indicatoron = 0, variable = self.valueset, value = title)
		button.place(x = self.button_size * len(self.buttons), y = 0, width = self.button_size, relheight = 1.)
		self.buttons.extend([button])
		if len(image):
			self.images += [tk.PhotoImage(file = image)]
			button.config(image = self.images[-1])
	@property
	def height(self):
		return self.button_size
	@property
	def getvalueset(self):
		return self.valueset.get()
################################################################################
# Application class ############################################################
################################################################################
class Application:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Drawing on Canvas by Krzysztof Zajączkowski (obliczeniowo.com.pl)")
		
		self.menu = tk.Menu(self.window)
		
		menu_file = tk.Menu(self.menu, tearoff = 0)
		menu_file.add_command(label = "Zapisz", command = self.menu_save_to_file)
		menu_file.add_command(label = "Otwórz", command = self.menu_open_file)
		
		self.menu.add_cascade(label = "Plik", menu = menu_file)
		
		menu_about = tk.Menu(self.menu, tearoff = 0)
		menu_about.add_command(label = "Autor programu", comman = self.menu_author)
		menu_about.add_command(label = "Licencja", command = self.menu_licence)
		
		self.menu.add_cascade(label = "O programie", menu = menu_about)
		
		self.window.config(menu = self.menu)
		
		self.toolbar = Toolbar(self.window)
		self.toolbar.add_button("L", image = "buttons/line.gif")
		self.toolbar.add_button("O", image = "buttons/ellipse.gif")
		self.toolbar.add_button("P", image = "buttons/rectangle.gif")
		self.toolbar.add_button("Pol", image = "buttons/polygon.gif")
		self.toolbar.add_button("M", image = "buttons/select.gif")
		self.toolbar.place(x = self.toolbar.height * 4)
		
		self.fillcolor = "#ffffff"
		self.fillcolorbutton = tk.Button(self.window, background = self.fillcolor, command = self.on_color_fill)
		self.fillcolorbutton.place(in_ = self.window, x = self.toolbar.height * 2, y = 0, width = self.toolbar.height, height = self.toolbar.height)
		
		self.strokecolor = "#000000"
		self.strokecolorbutton = tk.Button(self.window, background = self.strokecolor, command = self.on_color_stroke)
		self.strokecolorbutton.place(in_ = self.window, x = self.toolbar.height * 3, y = 0, width = self.toolbar.height, height = self.toolbar.height)
		
		self.canvas = tk.Canvas(self.window, background = "#ffffff", cursor = "tcross")
		self.canvas.place(x = 0, y = self.toolbar.height, relwidth = 1., relheight = 1., height = - self.toolbar.height * 2)
		
		self.strokewidth = tk.IntVar()
		self.strokewidth.set(1)
		self.strokewidthspin = tk.Spinbox(self.window, from_ = 0, to = 10, textvariable = self.strokewidth, command = self.on_width_changed)
		self.strokewidthspin.place(in_ = self.window, x = 0, y = 0, width = self.toolbar.height * 2, height = self.toolbar.height)
		
		self.mouse_position_on_canvas = tk.StringVar()
		self.lb_mouse_position_on_canvas = tk.Label(self.window, textvariable = self.mouse_position_on_canvas)
		self.lb_mouse_position_on_canvas.place( x = 5, y = -25, rely = 1.)
		
		self.draw_object = []
		
		self.selected = None
		
		self.mousepointclicked = [0,0]
		
		self.canvas.bind("<B1-Motion>", self.on_mousemoveb1)
		self.canvas.bind("<Motion>", self.on_mousemove)
		self.canvas.bind("<Button-1>", self.on_lbc)
		self.canvas.bind("<ButtonRelease-1>", self.on_lbr)
		
		self.canvas.bind("<Button-3>", self.on_rbc)
		self.canvas.bind("<Delete>", self.on_delete)
		
		self.drConstructors = [Rectangle.GetObject, Ellipse.GetObject, Line.GetObject, Polygon.GetObject]
		
		self.window.mainloop()
	def on_mousemoveb1(self, event):
		if self.toolbar.getvalueset == "P" or self.toolbar.getvalueset == "O" or self.toolbar.getvalueset == "L" or self.toolbar.getvalueset == "Pol":
			self.draw_object[-1].setEnd(event.x, event.y)
		elif self.toolbar.getvalueset == "M":
			self.canvas.move(self.selected, event.x - self.mousepointclicked[0],event.y - self.mousepointclicked[1])
			self.mousepointclicked = [event.x, event.y]
	def on_mousemove(self, event):
		self.mouse_position_on_canvas.set("x = {x}, y = {y}".format(x = event.x, y = event.y))
	def on_lbc(self, event):
		self.canvas.focus_set()
		if self.toolbar.getvalueset == "P":
			self.draw_object.extend([Rectangle(event.x, event.y, event.x, event.y, self.canvas, fill = self.fillcolor, outline = self.strokecolor, width = self.strokewidth.get())])
		elif self.toolbar.getvalueset == "O":
			self.draw_object.extend([Ellipse(event.x, event.y, event.x, event.y, self.canvas, fill = self.fillcolor, outline = self.strokecolor, width = self.strokewidth.get())])
		elif self.toolbar.getvalueset == "L":
			self.draw_object.extend([Line(event.x, event.y, event.x, event.y, self.canvas, outline = self.strokecolor, width = self.strokewidth.get())])
		elif self.toolbar.getvalueset == "Pol":
			self.draw_object.extend([Polygon([event.x, event.y], self.canvas, fill = self.fillcolor, outline = self.strokecolor, width = self.strokewidth.get())])
		elif self.toolbar.getvalueset == "M":
			self.selected = self.canvas.find_closest(event.x, event.y)
			if self.selected:
				config = self.canvas.itemconfig(self.selected);
				self.strokewidth.set(float(config["width"][4]))
				self.fillcolor = config["fill"][4]
				self.fillcolorbutton.config(background = self.fillcolor)
				if "outline" in config:
					self.strokecolor = config["outline"][4]
					self.strokecolorbutton.config(background = self.strokecolor)
		self.mousepointclicked = [event.x, event.y]
	def on_lbr(self, event):
		pass
	def on_color_fill(self):
		fc = cch.askcolor()[1]
		self.fillcolor = fc if fc != None else self.fillcolor
		self.fillcolorbutton.config(background = self.fillcolor)
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, fill = fc)
	def on_color_stroke(self):
		fc = cch.askcolor()[1]
		self.strokecolor = fc if fc != None else self.strokecolor
		self.strokecolorbutton.config(background = self.strokecolor)
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, outline = fc)
	def on_rbc(self, events):
		if len(self.draw_object):
			print(str(self.draw_object[-1]))
			self.draw_object[-1].remove()
			del(self.draw_object[-1])
	def on_width_changed(self):
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, width = self.strokewidth.get())
	def on_delete(self, event):
		if self.toolbar.getvalueset == "M" and self.selected != None:
			for i in self.draw_object:
				if i.id == self.selected[0]:
					self.draw_object.remove(i)
			self.canvas.delete(self.selected)
	# for menu methods		
	def menu_save_to_file(self):
		if len(self.draw_object):
			filename = fd.asksaveasfilename(filetypes=[("Plik tekstowy","*.txt")], defaultextension = "*.txt")
			
			if filename:
				newfile = open(filename, "w", -1, "utf-8")
				for i in range(len(self.draw_object)):
					newfile.write(str(self.draw_object[i]))
					if i < len(self.draw_object) - 1:
						newfile.write("\n")
				newfile.close()
	def menu_open_file(self):
		if len(self.draw_object) and msb.askyesno("Pytanie na śniadanie", "Czy zapisać bierzące dane do pliku?"):
			self.menu_save_to_file()
		filename = fd.askopenfilename(filetypes=[("Plik tekstowy","*.txt")], defaultextension = "*.txt")
		
		if filename:
			self.draw_object.clear()
			self.canvas.delete(tk.ALL)
			with open(filename, "r", -1, "utf-8") as openfile:
				lines = openfile.readlines()
				for line in lines:
					dictObj = strToDict(line)
					for constructor in self.drConstructors:
						newobject = constructor(dictObj, self.canvas)
						if newobject != None:
							self.draw_object += [newobject]
							break
	def menu_author(self):
		msb.showinfo("O autorze", "Ten szalenie prosty program napisazy został przez Krzysztofa Zajączkowskiego\nW złudnej skądinąd nadziei, że kogoś rozbawi lub rozweseli")
	def menu_licence(self):
		msb.showinfo("Licencja", "Ten niezwykle zaawansowany technicznie program udostępniam na licencji GPL-3.0")

apl = Application()
