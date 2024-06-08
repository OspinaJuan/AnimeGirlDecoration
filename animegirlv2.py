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

	def movement(self):
		if self.x() < self.screen.width() - 100 and self.y() == 25:
			self.move(self.x() + 3, 0)
		elif self.y() < self.screen.height() - 100 and self.x() > 100:
			self.move(self.x(), self.y() + 3)
		else:
			if self.x() > 0:
				self.move(self.x() - 3, self.y())
			else:
				self.move(self.x(), self.y() - 3)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			my_sound = pygame.mixer.Sound('/home/pony/Documents/coding/animegirlsound.wav')
			my_sound.play()
			self.hide()
			time.sleep(1)
			QApplication.instance().quit()


if __name__ == '__main__':
	app = QApplication(sys.argv)

	movingImage = movingImage()
	movingImage.show()

	sys.exit(app.exec_())
