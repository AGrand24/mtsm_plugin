












# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MTSMDialog
								 A QGIS plugin
 MT survey manager
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
							 -------------------
		begin                : 2025-04-04
		git sha              : $Format:%H$
		copyright            : (C) 2025 by Adam Grand
		email                : adam.grand@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""



from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject

import os
import subprocess
import sys

def change_dir(folder):
	dir_qgis=QgsProject.instance().homePath()
	dir_project=dir_qgis.replace("MTSM_qgis","").replace("/","\\")
	dir_scripts=(dir_qgis+'/scripts/').replace("/","\\")
	if folder=='qgis':
		os.chdir(dir_qgis)
	elif folder=='project':
		os.chdir(dir_project)
	elif folder=='scripts':
		os.chdir(dir_scripts)
	
	return [dir_project,dir_qgis,dir_scripts]
	# print(f'Changed CWD to {dir_qgis}\\scripts\\')

def run_script():
	with open("MTSM_qgis/scripts/MTSM_tools.py") as file:
				exec(file.read())
				file.close()





# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'MTSM_dialog_base.ui'))


class MTSMDialog(QtWidgets.QDialog, FORM_CLASS):
	def __init__(self, parent=None):
		"""Constructor."""
		super(MTSMDialog, self).__init__(parent)
		# Set up the user interface from Designer through FORM_CLASS.
		# After self.setupUi() you can access any designer object by doing
		# self.<objectname>, and you can use autoconnect slots - see
		# http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
		# #widgets-and-dialogs-with-auto-connect
		self.setupUi(self)
		dir=change_dir('project')[0]
		
		self.pb_clean_project.clicked.connect(self.clear_project)
		self.pb_import_rec.clicked.connect(self.run_import_rec)
		self.pb_export_backup.clicked.connect(self.export_backups)
		self.pb_qc_sensor_pos.clicked.connect(self.run_qc_sensor_pos)
		self.pb_run_processing.clicked.connect(self.run_processing)
		self.pb_dump_to_csv.clicked.connect(self.run_dump_to_csv)
		
		self.rb_xml_read_full.toggled.connect(self.xml_full_reload)
		self.rb_xml_read_smart.toggled.connect(self.xml_smart_reload)
		
		self.sb_radius_search.valueChanged.connect(self.sb_radius_search_changed)
		with open('search_radius.txt','r') as file:
			self.sb_radius_search.setValue(int(file.read().strip()))

		self.xml_reload_type='smart'
		
		with open('xml_reload_type.txt','w') as file:
			file.write(str(self.xml_reload_type))
		with open('search_radius.txt','w') as file:
			file.write(str(self.search_radius_value))

	def clear_project(self):
		reply= QtWidgets.QMessageBox.question(self,'Clean project','This will delete all Rec and Xml data and reload clean project. Are you sure?',
		QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
		
		if reply== QtWidgets.QMessageBox.Yes:
			dir=change_dir('scripts')[2]
			path=(dir+'run_create_project.py')

			print(f"explorer {path}")
			subprocess.Popen(f"explorer {path}")
		else:
			print('NO')
	


	def run_import_rec(self):
		dir=change_dir('project')[0]
		fpath, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose file', 'MTSM_qgis\\rec_import_export', 'REC data (*.rec)')
		print(fpath)
		if fpath:
			with open('fp_rec.txt','w') as file:
				file.write(fpath)
			dir=change_dir('scripts')[2]
			path=(dir+'run_import_rec.py')
			subprocess.Popen(f"explorer {path}")
			dir=change_dir('project')[0]

	def export_backups(self):
		dir=change_dir('scripts')[2]
		path=(dir+'run_export_backup.py')
		subprocess.Popen(f"explorer {path}")

	def xml_full_reload(self):
		self.xml_reload_type='full'
		print(self.xml_reload_type)

	def xml_smart_reload(self):
		self.xml_reload_type='smart'
		print(self.xml_reload_type)

	def run_processing(self):
		dir=change_dir('project')[0]
		with open('xml_reload_type.txt','w') as file:
			file.write(self.xml_reload_type)
		dir=change_dir('scripts')[2]
		path=(dir+'run_main_proc.py')
		subprocess.Popen(f"explorer {path}")
		dir=change_dir('project')[0]
	
	def sb_radius_search_changed(self):
		dir=change_dir('project')[0]
		self.search_radius_value = self.sb_radius_search.value()
		with open('search_radius.txt','w') as file:
			file.write(str(self.search_radius_value))
	
	def run_qc_sensor_pos(self):
		dir=change_dir('scripts')[2]
		path=(dir+'run_check_sensor_pos.py')
		subprocess.Popen(f"explorer {path}")
		dir=change_dir('project')[0]

	def run_dump_to_csv(self):
		dir=change_dir('scripts')[2]
		path=(dir+'run_dump_csv.py')
		subprocess.Popen(f"explorer {path}")
		dir=change_dir('project')[0]

	