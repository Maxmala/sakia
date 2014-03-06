'''
Created on 2 févr. 2014

@author: inso
'''
from cutecoin.gen_resources.accountConfigurationDialog_uic import Ui_AccountConfigurationDialog
from PyQt5.QtWidgets import QDialog
from cutecoin.gui.addCommunityDialog import AddCommunityDialog
from cutecoin.models.account import Account
from cutecoin.models.account.communities import Communities
from cutecoin.models.account.communities.listModel import CommunitiesListModel

import gnupg


class AddAccountDialog(QDialog, Ui_AccountConfigurationDialog):
    '''
    classdocs
    '''


    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        # Set up the user interface from Designer.
        super(AddAccountDialog, self).__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow

        self.buttonBox.accepted.connect(self.mainWindow.actionAddAccount)

        self.setData()

    def setData(self):
        gpg = gnupg.GPG()
        self.combo_keysList.clear()
        availableKeys = gpg.list_keys(True)
        for key in availableKeys:
            self.combo_keysList.addItem(key['uids'][0])

        self.account = Account.create(availableKeys[0]['keyid'], "", Communities())
        self.combo_keysList.setEnabled(True)
        self.combo_keysList.currentIndexChanged[int].connect(self.keyChanged)

    def openAddCommunityDialog(self):
        dialog = AddCommunityDialog(self)
        dialog.setAccount(self.account)
        dialog.exec_()

    def actionAddCommunity(self):
        self.combo_keysList.setEnabled(False)
        self.combo_keysList.disconnect()
        self.list_communities.setModel(CommunitiesListModel(self.account))

    def actionRemoveCommunity(self):
        #TODO:Remove selected community
        pass

    def actionEditCommunity(self):
        #TODO: Edit selected community
        pass

    def keyChanged(self, keyIndex):
        gpg = gnupg.GPG()
        availableKeys = gpg.list_keys(True)
        self.account.keyId = availableKeys[keyIndex]['keyid']

