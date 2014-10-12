import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Schedule(QDialog):
	def __init__(self, parent = None, data_file = sys.argv[1]):
		super(Schedule, self).__init__(parent)
		self.courses = {}
		self.data_file = data_file
		self.get_data()
		self.input_hint_label_name = QLabel('<b>课程名：</b>')
		self.input_hint_label_place = QLabel('<b>上课地点：</b>')
		self.input_hint_label_week = QLabel('<b>周目安排：</b>')
		self.input_hint_label_time = QLabel('<b>上课时间：</b>')
		self.lineedit_name = QLineEdit()
		self.lineedit_place = QLineEdit()
		self.lineedit_week = QLineEdit()
		self.lineedit_time = QLineEdit()
		grid = QGridLayout()
		self.buttons = []
		self.funcs = []
		for i in range(14):
			for j in range(7):
				try:
					self.buttons.append(QPushButton(self.courses[j+1, i+1][0]))
				except:
					self.buttons.append(QPushButton(''))
				grid.addWidget(self.buttons[-1], i+1, j+1)
				self.funcs.append(lambda row = i, column = j:self.show_more_info(row, column))
				self.connect(self.buttons[-1], SIGNAL('clicked()'), self.funcs[-1])
		for i in range(7):
			grid.addWidget(QLabel('<b>day %d</b>' % (i+1)), 0, i+1)
		for i in range(14):
			grid.addWidget(QLabel('<b>第%d小节</b>' % (i+1)), i+1, 0)
		grid.addWidget(self.input_hint_label_name, 15, 0)
		grid.addWidget(self.input_hint_label_place, 15, 3)
		grid.addWidget(self.input_hint_label_week, 16, 0)
		grid.addWidget(self.input_hint_label_time, 16, 3)
		grid.addWidget(self.lineedit_name, 15, 1)
		grid.addWidget(self.lineedit_place, 15, 4)
		grid.addWidget(self.lineedit_week, 16, 1)
		grid.addWidget(self.lineedit_time, 16, 4)
		self.save_button = QPushButton('save')
		self.connect(self.save_button, SIGNAL('clicked()'), self.save_data)
		self.cancel_button = QPushButton('cancel')
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.cancel_input)
		grid.addWidget(self.save_button, 15, 6)
		grid.addWidget(self.cancel_button, 16, 6)
		self.error_message_label = QLabel('')
		grid.addWidget(self.error_message_label, 17, 0)
		self.setLayout(grid)
		self.setWindowTitle('Schedule')

	def get_data(self):
		data =  open(self.data_file, 'r')
		lines = data.read().split('\n')
		for line in lines:
			course = line.split(';')
			times = course[1:]
			for time in times:
				self.courses[eval(time)] = eval(course[0])
		data.close()

	def save_data(self):
		name = self.lineedit_name.text()
		time = self.lineedit_time.text()
		place = self.lineedit_place.text()
		week = self.lineedit_week.text()
		try:
			if time == '':
				raise IndexError
			self.courses[eval(time)] = [name, week, place]
			self.buttons[(eval(time)[1]-1) * 7 + eval(time)[0]-1].setText(name)
		except Exception as e:
			self.error_message_label.setText(str(e))
		data = open(self.data_file, 'w')
		new_dict = {}
		for t in self.courses.keys():
			if str(self.courses[t]) not in list(new_dict.keys()):
				new_dict[str(self.courses[t])] = [str(t)[1:-1]]
			else:
				new_dict[str(self.courses[t])].append(str(t)[1:-1])
		for course in new_dict.keys():
			data.write(course + ';' + ';'.join(new_dict[course]) + '\n')
		data.close()

	def cancel_input(self):
		self.lineedit_week.setText('')
		self.lineedit_place.setText('')
		self.lineedit_name.setText('')
		time = self.lineedit_time.text()
		if time == '':
			return
		self.buttons[(eval(time)[1]-1) * 7 + eval(time)[0]-1].setText('')

	def show_more_info(self, i, j):
		try:
			self.lineedit_week.setText(self.courses[j+1, i+1][1])
			self.lineedit_place.setText(self.courses[j+1, i+1][2])
			self.lineedit_name.setText(self.courses[j+1, i+1][0])
			self.lineedit_time.setText(str(j+1) + ',' + str(i+1))
		except:
			self.lineedit_week.setText('')
			self.lineedit_time.setText(str(j+1) + ',' + str(i+1))
			self.lineedit_name.setText('')
			self.lineedit_place.setText('')

app = QApplication(sys.argv)
sch = Schedule()
sch.show()
app.exec_()