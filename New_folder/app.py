import sys 
import os
import time
import datetime
import pipes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from main import Ui_Form as Lwelcome
from backup import Ui_Form as Lbackup
from restore import Ui_Form as Lrestore
from PyQt5.uic import loadUi

class ProgramDB(QDialog):
    def __init__(self):
    	super(ProgramDB,self).__init__()
    	loadUi("main.ui",self)
    	self.backup.clicked.connect(self.gotobackup)
    	self.restore.clicked.connect(self.gotorestore)
		
    def gotobackup(self):
    	createbckp = backuppage()
    	widget.addWidget(createbckp)
    	widget.setCurrentIndex(widget.currentIndex()+1)

    def gotorestore(self):
    	createrstr = restorepage()
    	widget.addWidget(createrstr)
    	widget.setCurrentIndex(widget.currentIndex() + 1)

class backuppage(QDialog):
	def __init__(self):
		super(backuppage,self).__init__()
		loadUi("backup.ui",self)
		self.button_browser.clicked.connect(self.browserfolder)
		self.button_backup.clicked.connect(self.backup)
		self.menu.clicked.connect(self.gotomenu)

	def gotomenu(self):
		createmenu = ProgramDB()
		widget.addWidget(createmenu)
		widget.setCurrentIndex(widget.currentIndex()+1)


	def browserfolder(self):
		# dialog = QFileDialog()
		# dialog.setFileMode(QFileDialog.Directory)
		# dialog.setOption(QFileDialog.ShowDirsOnly)
		# folname = dialog.getExistingDirectory(self, 'Choose Directory', os.path.curdir)
		folname = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.path.setText(folname)

	def backup(self):
		DB_NAME = self.nama_db.text()
		BACKUP_PATH = self.path.text()

		files = BACKUP_PATH.replace("\\", "/")
		DATETIME = time.strftime('%Y%m%d-%H%M%S')
		TODAYBACKUPPATH = files + '/' + DB_NAME + '-' + DATETIME
			
		# Checking if backup folder already exists or not. If not exists will create it.
		try:
			os.stat(TODAYBACKUPPATH)
		except:
			os.mkdir(TODAYBACKUPPATH)
			
		# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
		print ("checking for databases names file.")
		if os.path.exists(DB_NAME):
			file1 = open(DB_NAME)
			multi = 1
			print ("Databases file found...")
			print ("Starting backup of all dbs listed in file " + DB_NAME)
		else:
			print ("Databases file not found...")
			print ("Starting backup of database " + DB_NAME)
			multi = 0
			
		# Starting actual database backup process.
		if multi:
			in_file = open(DB_NAME,"r")
			flength = len(in_file.readlines())
			in_file.close()
			p = 1
			dbfile = open(DB_NAME,"r")
			
			while p <= flength:
				db = dbfile.readline()   # reading database name from file
				db = db[:-1]         # deletes extra line
				dumpcmd = "mysqldump -h localhost -u root " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
				# dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER +" -p " +DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
				os.system(dumpcmd)
				# gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
				# os.system(gzipcmd)
				p = p + 1
			dbfile.close()
		else:

			db = DB_NAME
			print ("Starting backup of database " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql")
			dumpcmd = "mysqldump -h localhost -u root " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
			# dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER  +" -p " +DB_USER_PASSWORD +" " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
			os.system(dumpcmd)
			# gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
			# os.system(gzipcmd)
			
		print ("")
		print ("Backup script completed")
		print ("Your backups have been created in '" + dumpcmd + "' directory")
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Backup script completed \n Your backups have been created in '" + pipes.quote(TODAYBACKUPPATH) + "' directory")
		msgBox.setWindowTitle("Backup Success ")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		# msgBox.buttonClicked.connect(msgButtonClick)

		returnValue = msgBox.exec()
		if returnValue == QMessageBox.Ok:
			createmenu = ProgramDB()
			widget.addWidget(createmenu)
			widget.setCurrentIndex(widget.currentIndex()+1)


class restorepage(QDialog):
	def __init__(self):
		super(restorepage,self).__init__()
		loadUi("restore.ui",self)
		self.button_browser.clicked.connect(self.browserfiles)
		self.button_restore.clicked.connect(self.restore)
		self.menu.clicked.connect(self.gotomenu)

	def gotomenu(self):
		createmenu = ProgramDB()
		widget.addWidget(createmenu)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def browserfiles(self):
		fname=QFileDialog.getOpenFileName(self, 'Open file', os.path.curdir , 'sql (*.sql)')
		self.path.setText(fname[0])

	def restore(self):
		DB_NAME = self.nama_db.text()
		BACKUP_PATH = self.path.text()

		files = BACKUP_PATH.replace("\\", "/")
		print ("checking for databases names file.")
		if os.path.exists(files):
			print ("Databases file found...")
			print("path :"+files)
			print ("Starting restore of database " + DB_NAME)
			db = DB_NAME
			create = 'mysql -h localhost -u root -e "create database '+db+'"' 
			# create = 'mysql -h ' + DB_HOST + ' -u ' + DB_USER  +' -p ' +DB_USER_PASSWORD +' -e "create database '+db+'"' 
			os.system(create)
			dumpcmd = "mysql -h localhost -u root " + db + " < " + files 
			# dumpcmd = "mysql -h " + DB_HOST + " -u " + DB_USER  +" -p " +DB_USER_PASSWORD +" " + db + " < " + files 
			os.system(dumpcmd)

			print ("")
			print ("restore script completed")
			# createmenu = ProgramDB()
			# widget.addWidget(createmenu)
			# widget.setCurrentIndex(widget.currentIndex()+1)

			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Restore Database Berhasil")
			msgBox.setWindowTitle("Restore Success")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			# msgBox.buttonClicked.connect(msgButtonClick)

			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Ok:
				createmenu = ProgramDB()
				widget.addWidget(createmenu)
				widget.setCurrentIndex(widget.currentIndex()+1)

		else:
				msgBox = QMessageBox()
				msgBox.setIcon(QMessageBox.Critical)
				msgBox.setText("Restore Database Gagal \n File Not Found!")
				msgBox.setWindowTitle("Restore Failed!")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				# msgBox.buttonClicked.connect(msgButtonClick)

				returnValue = msgBox.exec()
				if returnValue == QMessageBox.Ok:
					createmenu = ProgramDB()
					widget.addWidget(createmenu)
					widget.setCurrentIndex(widget.currentIndex()+1)



if __name__ == "__main__":
	# app = QtWidgets.QApplication(sys.argv)
	# dialog = QtWidgets.QDialog()

	# prog = ProgramDB(dialog)

	# dialog.show()
	# sys.exit(app.exec_())
	app=QApplication(sys.argv)
	mainwindow=ProgramDB()
	widget=QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.setFixedWidth(280)
	widget.setFixedHeight(400)
	widget.show()
	app.exec_()