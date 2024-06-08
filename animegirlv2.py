from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap
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
		self.setPixmap(QPixmap("animegirl.png"))
		self.setGeometry(0,0,100,100)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setScaledContents(True)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.movement)
		self.timer.start(10)

	def move_right(self):
		self.move(self.x() + 3, self.y())

	def move_left(self):
		self.move(self.x() - 3, self.y())

	def move_down(self):
		self.move(self.x(), self.y() + 3)

	def move_up(self):
		self.move(self.x(), self.y() - 3)

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

	def movement(self):
		if not self.is_at_x_right_edge() and self.is_at_y_up_edge():
			self.move_right()
		elif not self.is_at_y_bottom_edge() and self.is_at_x_right_edge():
			self.move_down()
		elif not self.is_at_x_left_edge() and self.is_at_y_bottom_edge():
			self.move_left()
		elif self.is_at_x_left_edge() and not self.is_at_y_up_edge():
			self.move_up()

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
