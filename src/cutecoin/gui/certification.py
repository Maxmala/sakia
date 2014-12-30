'''
Created on 24 dec. 2014

@author: inso
'''
from PyQt5.QtWidgets import QDialog, QErrorMessage, QInputDialog, QLineEdit, QMessageBox

from cutecoin.core.person import Person

from cutecoin.gen_resources.certification_uic import Ui_CertificationDialog


class CertificationDialog(QDialog, Ui_CertificationDialog):

    '''
    classdocs
    '''

    def __init__(self, certifier):
        '''
        Constructor
        '''
        super().__init__()
        self.setupUi(self)
        self.certifier = certifier
        self.community = self.certifier.communities[0]

        for community in self.certifier.communities:
            self.combo_community.addItem(community.currency)

        for contact in certifier.contacts:
            self.combo_contact.addItem(contact.name)

    def accept(self):
        if self.radio_contact.isChecked():
            index = self.combo_contact.currentIndex()
            pubkey = self.certifier.contacts[index].pubkey
        else:
            pubkey = self.edit_pubkey.text()

        password = QInputDialog.getText(self, "Account password",
                                        "Please enter your password",
                                        QLineEdit.Password)
        if password[1] is True:
            password = password[0]
        else:
            return

        while not self.certifier.check_password(password):
            password = QInputDialog.getText(self, "Account password",
                                            "Wrong password.\nPlease enter your password",
                                            QLineEdit.Password)
            if password[1] is True:
                password = password[0]
            else:
                return

        try:
            self.certifier.certify(password, self.community, pubkey)
            QMessageBox.information(self, "Certification",
                                 "Success certifying {0} from {1}".format(pubkey,
                                                                          self.community.currency))
        except ValueError as e:
            QMessageBox.critical(self, "Certification",
                                 "Something wrong happened : {0}".format(e),
                                 QMessageBox.Ok)

        self.accepted.emit()
        self.close()

    def change_current_community(self, index):
        self.community = self.certifier.communities[index]

    def recipient_mode_changed(self, pubkey_toggled):
        self.edit_pubkey.setEnabled(pubkey_toggled)
        self.combo_contact.setEnabled(not pubkey_toggled)