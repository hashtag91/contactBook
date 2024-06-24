from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QToolButton, QVBoxLayout, QHBoxLayout, QFrame, 
                            QMainWindow, QPushButton, QFileDialog, QMessageBox, QDialog, QScrollArea, QListWidgetItem, QListWidget,
                            QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QCursor
from PyQt5.QtCore import Qt, QEvent
import db_Operation
import sys

class My_Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #383838")
        self.main_layout = QVBoxLayout()
        self.setupUi()
        self.setLayout(self.main_layout)
    def setupUi(self):
        self.edit_list = []
        self.delete_list = []

        title = QLabel(text="Carnet d'adresse")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial Black",18,QFont.Bold))
        title.setStyleSheet("color: #ffffff;")

        self.details = Details()

        #Tool button section
        self.add_btn = ToolButton("icon/plus")
        self.add_btn.setToolTip("Ajouter un contact")
        self.add_btn.clicked.connect(self.add_function)
        self.delete_btn = ToolButton("icon/trash")
        self.delete_btn.setToolTip("Supprimer un contact")
        self.delete_btn.clicked.connect(self.delete_msg)
        self.edit_btn = ToolButton("icon/edit")
        self.edit_btn.setToolTip("Modifier un contact")
        self.edit_btn.clicked.connect(self.edit_function)
        tool_btn_layout = QHBoxLayout()
        tool_btn_layout.addStretch()
        tool_btn_layout.addWidget(self.add_btn)
        tool_btn_layout.addWidget(self.delete_btn)
        tool_btn_layout.addWidget(self.edit_btn)
        #Left Side section
        contact_label = QLabel("Liste de contacts")
        contact_label.setFont(QFont("Arial Black",10,QFont.Bold))
        contact_label.setStyleSheet("color:#ffffff")
        contact_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_list_layout = QVBoxLayout()
        contact_list_layout.addWidget(contact_label)
        #Contaact liste Frame
        contact_list_frame = QFrame()
        contact_list_frame.setFrameShape(QFrame.StyledPanel)
        contact_list_frame.setStyleSheet("background-color: #d9d9d9")
        self.contact_list_Item_layout = QVBoxLayout()
        data = db_Operation.db_trievment()
        if data != False:
            for d in data:
                self.contact_list_Item_layout.addWidget(ContactItem(d[0],d[2],d[-1],self.details,self.edit_list,self.delete_list))
        self.contact_list_Item_layout.addStretch()
        contact_list_frame.setLayout(self.contact_list_Item_layout)
        scrol = QScrollArea()
        scrol.setWidgetResizable(True)
        scrol.setWidget(contact_list_frame)
        scrol.setStyleSheet("background-color: #d9d9d9; border-radius: 15%")
        contact_list_layout.addWidget(scrol)

        details_label = QLabel("Details")
        details_label.setFont(QFont("Arial Black",10,QFont.Bold))
        details_label.setStyleSheet("color:#ffffff")
        details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        details_layout = QVBoxLayout()


        details_layout.addWidget(details_label)
        details_layout.addWidget(self.details)


        middle_layout = QHBoxLayout()
        middle_layout.addLayout(contact_list_layout,1)
        middle_layout.addLayout(details_layout,2)

        self.main_layout.addWidget(title)
        self.main_layout.addLayout(tool_btn_layout)
        self.main_layout.addLayout(middle_layout)
        self.d = QDialog()
        self.d.setContentsMargins(0,0,0,0)
        self.m_d = QDialog()
        self.m_d.setContentsMargins(0,0,0,0)
        
    def add_function(self):
        self.add_win = Add_window(self.d)
        self.add_win.save_btn.clicked.connect(self.add_win_save_function)
        d_layout = QVBoxLayout()
        d_layout.setContentsMargins(0,0,0,0)
        d_layout.addWidget(self.add_win)
        self.d.setLayout(d_layout)
        self.d.exec()
        data = db_Operation.db_trievment()
        if data != False:
            while self.contact_list_Item_layout.count():
                item = self.contact_list_Item_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            for d in data:
                self.contact_list_Item_layout.addWidget(ContactItem(d[0],d[2],d[-1],self.details,self.edit_list,self.delete_list))
        self.contact_list_Item_layout.addStretch()
    def add_win_save_function(self):
        insertion = db_Operation.db_adding(self.add_win.name.text(), self.add_win.phone.text(), self.add_win.email.text(), self.add_win.address.text(), self.add_win.profil_path)
        if insertion == True:
            msg = QMessageBox()
            msg.setText("Contact enregistré avec succès")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.add_win.dialog.close()
        else:
            QMessageBox.warning(self,"Erreur","Erreur lors de l'enregistrement du contact")
    def edit_function(self):
        self.modify_win = Add_window(self.m_d)
        d_layout = QVBoxLayout()
        d_layout.setContentsMargins(0,0,0,0)
        d_layout.addWidget(self.modify_win)
        self.m_d.setLayout(d_layout)
        if len(self.edit_list) >= 1:
            data = db_Operation.selected_retrieve(self.edit_list[0])
            self.modify_win.title.setText("Modifier")
            self.modify_win.name.setText(data[0])
            self.modify_win.phone.setText(data[1])
            self.modify_win.email.setText(data[2])
            self.modify_win.address.setText(data[3])
            pix = QPixmap(data[4]).scaled(100,100, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio,transformMode=Qt.TransformationMode.SmoothTransformation)
            self.modify_win.profil_label.setPixmap(pix)
            self.modify_win.save_btn.clicked.connect(lambda: self.edit_save_btn_function(data[-1]))
            self.m_d.exec()
        else:
            info = QMessageBox.information(self,"Information","Selectionnez un contact à modifier")
        clear_layout(self.m_d.layout())
    def edit_save_btn_function(self,path):
        my_path = None
        if self.modify_win.profil_path == "":
            my_path = path
        else:
            my_path = self.modify_win.profil_path
        data_list = [self.modify_win.name.text(),self.modify_win.phone.text(),self.modify_win.email.text(),self.modify_win.address.text(),my_path,self.edit_list[0]]
        db_Operation.db_update(data_list)
        data = db_Operation.db_trievment()
        if data != False:
            while self.contact_list_Item_layout.count():
                item = self.contact_list_Item_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            for d in data:
                self.contact_list_Item_layout.addWidget(ContactItem(d[0],d[2],d[-1],self.details,self.edit_list,self.delete_list))
        self.contact_list_Item_layout.addStretch()
        self.m_d.close()
    def deletion_function(self):
        for i in self.delete_list:
            db_Operation.db_deletion(i)
        data = db_Operation.db_trievment()
        if data != False:
            while self.contact_list_Item_layout.count():
                item = self.contact_list_Item_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            for d in data:
                self.contact_list_Item_layout.addWidget(ContactItem(d[0],d[2],d[-1],self.details,self.edit_list,self.delete_list))
        self.contact_list_Item_layout.addStretch()
    def delete_msg(self):
        if len(self.delete_list) == 0:
            info = QMessageBox.information(self,"Information","Selectionnez au moins un contact à supprimer")
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Suppression')
            msg_box.setText('Voulez-vous vraiment supprimer ?')
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            reply = msg_box.exec_()
            if reply == QMessageBox.Yes:
                self.deletion_function()
                self.delete_list.clear()
                self.edit_list.clear()
            else:
                pass
        # Appliquer une feuille de style pour changer la couleur de fond
        #msg_box.setStyleSheet("QMessageBox { background-color: lightblue; }"
        #                      "QPushButton { background-color: white; }")

        # Afficher la boîte de dialogue et récupérer la réponse de l'utilisateur
        

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        layout.deleteLater()

class Details(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #d9d9d9;border-radius:15%")
        self.name = DetailsField("Name","icon/user.svg")
        self.phone = DetailsField("Telephone","icon/phone-13.svg")
        self.email = DetailsField("Email","icon/email.svg")
        self.address = DetailsField("Address","icon/location.svg")
        
        self.profil_label = QLabel()
        self.profil_label.setStyleSheet("background:transparent;")
        self.profil_label.setMinimumSize(150,180)
        self.pix = QPixmap("icon/no-image").scaled(150,180,aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.profil_label.setPixmap(self.pix)
        self.second_layout = QVBoxLayout()
        self.second_layout.addWidget(self.profil_label)
        self.second_layout.addStretch()
        self.second_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.third_layout = QVBoxLayout()
        self.third_layout.addWidget(self.name)
        self.third_layout.addWidget(self.phone)
        self.third_layout.addWidget(self.email)
        self.third_layout.addWidget(self.address)
        self.third_layout.addStretch()
        self.third_layout.setSpacing(40)
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(30)
        self.main_layout.addLayout(self.second_layout,1)
        self.main_layout.addLayout(self.third_layout,4)
        self.setLayout(self.main_layout)

class DetailsField(QFrame):
    def __init__(self,placeholder,ico):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setMinimumHeight(60)
        self.setStyleSheet("background-color:#ffffff; border-radius:25%")
        self.placeholder = placeholder
        self.ico = ico
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setMinimumWidth(60)
        icon_pix = QPixmap(self.ico).scaled(45,45,aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(icon_pix)
        icon_label.setStyleSheet("background-color: #c9c9c9; border-top-right-radius:0%; border-bottom-right-radius:0%; ")
        self.line = QLineEdit()
        self.line.setPlaceholderText(self.placeholder)
        self.line.setStyleSheet("background: transparent; border: none")
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(icon_label)
        self.main_layout.addWidget(self.line,1)
        self.setLayout(self.main_layout)

class ContactItem(QFrame):
    def __init__(self,name,email,path,details_entry:QFrame,edit:list,delete:list):
        super().__init__()
        self.name = name
        self.email = email
        self.path = path
        self.details_entry = details_entry
        self.edit = edit
        self.delete = delete
        self.setObjectName("frame")
        self.main_layout = QHBoxLayout()
        self.setupUi()
        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color:#82b0bf;")
        self.setFrameShape(QFrame.StyledPanel)
        self.installEventFilter(self)
    def setupUi(self):
        self.check = QCheckBox()
        self.check.stateChanged.connect(self.check_function)
        profil_label = QLabel()
        profil_label.setFixedSize(60,60)
        pix = QPixmap(self.path).scaled(60,60, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        profil_label.setPixmap(pix)

        self.name_label = QLabel(self.name)
        self.name_label.setObjectName("frame")
        self.name_label.setFont(QFont("Arial Black",10,QFont.Bold))
        self.name_label.setStyleSheet("color:#ffffff")
        self.email_label = QLabel(self.email)
        self.email_label.setObjectName("frame")
        self.email_label.setStyleSheet("color:#ffffff;")
        second_layout = QVBoxLayout()
        second_layout.addWidget(self.name_label)
        second_layout.addWidget(self.email_label)

        self.main_layout.addWidget(self.check)
        self.main_layout.addWidget(profil_label,2)
        self.main_layout.addLayout(second_layout,5)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                data = db_Operation.selected_retrieve(self.email)
                self.details_entry.name.line.setText(data[0])
                self.details_entry.phone.line.setText(data[1])
                self.details_entry.email.line.setText(data[2])
                self.details_entry.address.line.setText(data[3])
                pix = QPixmap(data[4]).scaled(150,180,aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
                self.details_entry.profil_label.setPixmap(pix)
                return True
        return super().eventFilter(obj, event)
    def check_function(self,state):
        if state == 2:
            if len(self.edit) < 1:
                self.edit.append(self.email_label.text())
            self.delete.append(self.email_label.text())
        else:
            try:
                self.edit.remove(self.email_label.text())
                self.delete.remove(self.email_label.text())
            except:
                self.delete.remove(self.email_label.text())
class ToolButton(QToolButton):
    def __init__(self,icon):
        super().__init__()
        self.ico = icon
        self.setIcon(QIcon(self.ico))
        self.setStyleSheet("border: none")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
class Add_window(QFrame):
    def __init__(self,dialog:QDialog):
        super().__init__()
        self.dialog = dialog
        self.setMinimumSize(600,700)
        self.setStyleSheet("background-color: #383838;")
        self.second_layout = QHBoxLayout()
        self.second_layout.setSpacing(30)
        
        self.main_layout = QVBoxLayout()
        self.setupUi()
        self.setLayout(self.main_layout)
    def setupUi(self):
        self.title = QLabel()
        self.title.setText("Ajouter")
        self.title.setFont(QFont("Arial Black",18,QFont.Bold))
        self.title.setStyleSheet("color: #ffffff; background-color: #383838")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title)
        self.profil_label = QLabel()
        self.profil_label.setFixedSize(100,100)
        profil_pix = QPixmap("icon/profil.svg").scaled(100,100, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio,transformMode=Qt.TransformationMode.SmoothTransformation)
        self.profil_label.setPixmap(profil_pix)
        self.profil_label.setStyleSheet("border: 1px solid gray")
        self.profil_loader = QPushButton(text="Edit")
        self.profil_loader.setMaximumWidth(100)
        self.profil_loader.setStyleSheet("background-color: #ffffff;")
        self.profil_loader.clicked.connect(self.openFileNameDialog)
        profil_layout = QVBoxLayout()
        profil_layout.addWidget(self.profil_label)
        profil_layout.addWidget(self.profil_loader)
        profil_layout.addStretch()

        self.name = Info_Field("Name")
        self.phone = Info_Field("Telephone")
        self.email = Info_Field("Email")
        self.address = Info_Field("Adresse")
        self.profil_path = ""
        text_field_layout = QVBoxLayout()
        text_field_layout.setSpacing(30)
        text_field_layout.addWidget(self.name)
        text_field_layout.addWidget(self.phone)
        text_field_layout.addWidget(self.email)
        text_field_layout.addWidget(self.address)
        text_field_layout.addStretch()

        self.save_btn = QPushButton()
        self.save_btn.setText("Enregistrer")
        self.save_btn.setMinimumHeight(50)
        self.save_btn.setFont(QFont("Arial",15,QFont.Bold))
        self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_btn.setStyleSheet("""
                            QPushButton{
                                    background-color: #106491;
                                    color: #ffffff;
                                    }
                            QPushButton:hover{
                                    background-color: #c2a374;
                                    color: rgb(0,0,0);
                                    }
                                    """)
        self.second_layout.addLayout(profil_layout)
        self.second_layout.addLayout(text_field_layout)
        self.main_layout.addLayout(self.second_layout)
        self.main_layout.addWidget(self.save_btn)
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "JPG Files (*.jpg);;JPEG Files (*.jpeg);;PNG Files (*.png)", options=options)
        if fileName:
            pix = QPixmap(fileName).scaled(100,100, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio,transformMode=Qt.TransformationMode.SmoothTransformation)
            self.profil_label.setPixmap(pix)
            self.profil_path = fileName
        else:
            pass
    def filename(self):
        return self.profil_path
    
class Info_Field(QLineEdit):
    def __init__(self, placeHolder:str):
        super().__init__()
        self.placeHolder = placeHolder
        self.setPlaceholderText(self.placeHolder)
        self.setStyleSheet("""
                    QLineEdit{
                           background-color: #e1e3e1;
                           border-radius: 15px;
                           }
                    QLineEdit:hover{
                           background-color: #cfcfcf;
                           border-radius: 15px;}
                        """)
        self.setMinimumHeight(40)
        self.setMaximumHeight(60)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setMinimumSize(900,400)
    win.setStyleSheet("background-color: #383838")
    win.setCentralWidget(My_Interface())
    #ContactItem("Yacouba Camara","camarayacouba91@gmail.com","C:/Users/LENOVO/Pictures/DSC_4683.JPG")
    win.show()
    sys.exit(app.exec())