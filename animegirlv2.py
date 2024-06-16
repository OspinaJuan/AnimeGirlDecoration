from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QCursor, QMovie
from PyQt5.QtMultimedia import QSound
import sys
import time
import pygame

pygame.init()
class movingImage(QLabel):
	def __init__(self):
		super().__init__()
		self.screen = QDesktopWidget().screenGeometry()
		self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
		self.movie = QMovie("padoru.gif")
		self.setMovie(self.movie)
		self.movie.start()
		self.setGeometry(0,0,80,80)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setScaledContents(True)

		self.checkProximityTimer = QTimer(self)
		self.checkProximityTimer.timeout.connect(self.checkFrontalProximity)
		self.checkProximityTimer.start(100)

		self.movementClockwiseTimer = QTimer(self)
		self.movementClockwiseTimer.timeout.connect(self.movement_clockwise)
		self.movementClockwiseTimer.start(10)

		self.movementCounterclockwiseTimer = QTimer(self)
		self.movementCounterclockwiseTimer.timeout.connect(self.movement_counterclockwise)

	def reverseMovementToCounter(self):
		self.movementClockwiseTimer.stop()
		self.movementCounterclockwiseTimer.start(10)

	def reverseMovementToClockwise(self):
		self.movementCounterclockwiseTimer.stop()
		self.movementClockwiseTimer.start(10)

	def checkFrontalProximity(self):
		pos = QCursor.pos()
		center_x = self.x() + self.size().width() / 2
		center_y = self.y() + self.size().height() / 2

		if abs(center_x - pos.x()) < 100 and abs(center_y - pos.y()) < 50:
			if center_x - pos.x() > 0:
				if self.movementClockwiseTimer.isActive() and self.is_at_y_bottom_edge():	
					self.reverseMovementToCounter()
				elif self.movementCounterclockwiseTimer.isActive() and self.is_at_y_up_edge():
					self.reverseMovementToClockwise()
			elif center_x - pos.x() < 0:
				if self.movementClockwiseTimer.isActive() and self.is_at_y_up_edge():
					self.reverseMovementToCounter()
				elif self.movementCounterclockwiseTimer.isActive() and self.is_at_y_bottom_edge():
					self.reverseMovementToClockwise()
		if abs(center_x - pos.x()) < 50 and abs(center_y - pos.y()) < 100:
			if center_y - pos.y() > 0:
				if self.movementClockwiseTimer.isActive() and self.is_at_x_left_edge():
					self.reverseMovementToCounter()
				elif self.movementCounterclockwiseTimer.isActive() and self.is_at_x_right_edge():
					self.reverseMovementToClockwise()
			elif center_y - pos.y() < 0:
				if self.movementClockwiseTimer.isActive() and self.is_at_x_right_edge():
					self.reverseMovementToCounter()
				elif self.movementCounterclockwiseTimer.isActive() and self.is_at_x_left_edge():
					self.reverseMovementToClockwise()
	
	def checkBackProximity(self):
		pos = QCursor.pos()
		center_x = self.x() + self.size().width() / 2
		center_y = self.y() + self.size().height() / 2
		proximity = max(abs(center_x - pos.x()), abs(center_y - pos.y()))

		if (((abs(center_x - pos.x()) < 200 and abs(center_y - pos.y()) < 60) and
		   ((center_x - pos.x() > 0 and 
		   ((self.movementClockwiseTimer.isActive() and 
		   self.is_at_y_up_edge()) or 
		   (self.movementCounterclockwiseTimer.isActive() and 
		   self.is_at_y_bottom_edge()))) or 
		   (center_x - pos.x() < 0 and 
		   ((self.movementClockwiseTimer.isActive() and 
		   self.is_at_y_bottom_edge()) or 
		   (self.movementCounterclockwiseTimer.isActive() and 
		   self.is_at_y_up_edge()))))) or
		   ((abs(center_x - pos.x()) < 60 and abs(center_y - pos.y()) < 200) and
		   ((center_y - pos.y() > 0 and 
		   ((self.movementClockwiseTimer.isActive() and 
		   self.is_at_x_right_edge()) or 
		   (self.movementCounterclockwiseTimer.isActive() and self.is_at_x_left_edge()))) or 
		   (center_y - pos.y() < 0 and 
		   ((self.movementClockwiseTimer.isActive() and 
		   self.is_at_x_left_edge()) or 
		   (self.movementCounterclockwiseTimer.isActive() and 
		   self.is_at_x_right_edge())))))):
				if 50 < proximity < 200:
					return  round(-(1/50) * proximity + 8)
				elif proximity < 50:
					return 10
		return 3

	def move_right(self, speed):
		self.move(self.x() + speed, self.y())

	def move_left(self, speed):
		self.move(self.x() - speed, self.y())

	def move_down(self, speed):
		self.move(self.x(), self.y() + speed)

	def move_up(self, speed):
		self.move(self.x(), self.y() - speed)

	def is_at_x_right_edge(self):
		if self.x() >= 1266:
			return True
		return False

	def is_at_y_up_edge(self):
		if self.y() <= 25:
			return True
		return False

	def is_at_y_bottom_edge(self):
		if self.y() > 668:
			return True
		return False

	def is_at_x_left_edge(self):
		if self.x() <= 0:
			return True
		return False

	def movement_clockwise(self):
		speed = self.checkBackProximity()
		if not self.is_at_x_right_edge() and self.is_at_y_up_edge():
			self.move_right(speed)
		elif not self.is_at_y_bottom_edge() and self.is_at_x_right_edge():
			self.move_down(speed)
		elif not self.is_at_x_left_edge() and self.is_at_y_bottom_edge():
			self.move_left(speed)
		elif self.is_at_x_left_edge() and not self.is_at_y_up_edge():
			self.move_up(speed)

	def movement_counterclockwise(self):
		speed = self.checkBackProximity()
		if not self.is_at_x_left_edge() and self.is_at_y_up_edge():
			self.move_left(speed)
		elif not self.is_at_y_up_edge() and self.is_at_x_right_edge():
			self.move_up(speed)
		elif not self.is_at_x_right_edge() and self.is_at_y_bottom_edge():
			self.move_right(speed)
		elif self.is_at_x_left_edge() and not self.is_at_y_bottom_edge():
			self.move_down(speed)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			my_sound = pygame.mixer.Sound('animegirlsound.wav')
			my_sound.play()
			self.hide()
			time.sleep(1)
			QApplication.instance().quit()


if __name__ == '__main__':
	app = QApplication(sys.argv)

	movingImage = movingImage()
	movingImage.show()

	sys.exit(app.exec_())
