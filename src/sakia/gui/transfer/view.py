from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QT_TRANSLATE_NOOP, QRegExp
from .transfer_uic import Ui_TransferMoneyDialog
from enum import Enum
from ..widgets import toast
from ..widgets.dialogs import QAsyncMessageBox


class TransferView(QDialog, Ui_TransferMoneyDialog):
    """
    Transfer component view
    """

    class ButtonBoxState(Enum):
        NO_AMOUNT = 0
        OK = 1

    class RecipientMode(Enum):
        CONTACT = 0
        PUBKEY = 1
        SEARCH = 2

    _button_box_values = {
        ButtonBoxState.NO_AMOUNT: (False,
                                   QT_TRANSLATE_NOOP("TransferView", "No amount. Please give the transfer amount")),
        ButtonBoxState.OK: (True, QT_TRANSLATE_NOOP("CertificationView", "&Ok"))
    }

    def __init__(self, parent, search_user_view, user_information_view,
                 communities_names, contacts_names, wallets_names):
        """

        :param parent:
        :param sakia.gui.search_user.view.SearchUserView search_user_view:
        :param sakia.gui.user_information.view.UserInformationView user_information_view:
        :param list[str] communities_names:
        :param list[str] contacts_names:
        :param list[str] wallets_names:
        """
        super().__init__(parent)
        self.setupUi(self)

        self.radio_contact.toggled.connect(lambda c, radio=TransferView.RecipientMode.CONTACT: self.recipient_mode_changed(radio))
        self.radio_pubkey.toggled.connect(lambda c, radio=TransferView.RecipientMode.PUBKEY: self.recipient_mode_changed(radio))
        self.radio_search.toggled.connect(lambda c, radio=TransferView.RecipientMode.SEARCH: self.recipient_mode_changed(radio))

        regexp = QRegExp('^([ a-zA-Z0-9-_:/;*?\[\]\(\)\\\?!^+=@&~#{}|<>%.]{0,255})$')
        validator = QRegExpValidator(regexp)
        self.edit_message.setValidator(validator)

        for name in communities_names:
            self.combo_community.addItem(name)

        for name in sorted(contacts_names):
            self.combo_contact.addItem(name)

        for name in wallets_names:
            self.combo_wallets.addItem(name)

        if len(contacts_names) == 0:
            self.combo_contact.setEnabled(False)
            self.radio_pubkey.setChecked(True)
            self.radio_contact.setEnabled(False)

        self.search_user = search_user_view
        self.user_information_view = user_information_view

    def recipient_mode(self):
        if self.radio_contact.isChecked():
            return TransferView.RecipientMode.CONTACT
        elif self.radio_search.isChecked():
            return TransferView.RecipientMode.SEARCH
        else:
            return TransferView.RecipientMode.PUBKEY

    def selected_contact(self):
        return self.combo_contact.currentText()

    def set_search_user(self, search_user_view):
        """

        :param sakia.gui.search_user.view.SearchUserView search_user_view:
        :return:
        """
        self.search_user = search_user_view
        self.layout_search_user.addWidget(search_user_view)
        self.search_user.button_reset.hide()

    def set_user_information(self, user_information_view):
        self.user_information_view = user_information_view
        self.group_box_recipient.layout().addWidget(user_information_view)

    def recipient_mode_changed(self, radio):
        """
        :param str radio:
        """
        self.edit_pubkey.setEnabled(radio == TransferView.RecipientMode.PUBKEY)
        self.combo_contact.setEnabled(radio == TransferView.RecipientMode.CONTACT)
        self.search_user.setEnabled(radio == TransferView.RecipientMode.SEARCH)

    def change_quantitative_amount(self, amount):
        """
        Change relative amount with signals blocked
        :param amount:
        """
        self.spinbox_amount.blockSignals(True)
        self.spinbox_amount.setValue(amount)
        self.spinbox_amount.blockSignals(False)

    def change_relative_amount(self, relative):
        """
        Change the quantitative amount with signals blocks
        :param relative:
        """
        self.spinbox_relative.blockSignals(True)
        self.spinbox_relative.setValue(relative)
        self.spinbox_relative.blockSignals(False)

    def set_spinboxes_parameters(self, tick_quant, max_quant, max_rel):
        """
        Configure the spinboxes
        It should depend on what the last UD base is
        :param int tick_quant:
        :param int max_quant:
        :param float max_rel:
        """
        self.spinbox_amount.setMaximum(max_quant)
        self.spinbox_relative.setMaximum(max_rel)
        self.spinbox_amount.setSingleStep(tick_quant)

    def refresh_labels(self, total_text, currency):
        """
        Refresh displayed texts
        :param str total_text:
        :param str currency:
        """
        self.label_total.setText("{0}".format(total_text))
        self.spinbox_amount.setSuffix(" " + currency)

    def set_button_box(self, state, **kwargs):
        """
        Set button box state
        :param sakia.gui.transfer.view.TransferView.ButtonBoxState state: the state of te button box
        :param dict kwargs: the values to replace from the text in the state
        :return:
        """
        button_box_state = TransferView._button_box_values[state]
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(button_box_state[0])
        self.button_box.button(QDialogButtonBox.Ok).setText(button_box_state[1].format(**kwargs))

    async def show_success(self, notification, recipient):
        if notification:
            toast.display(self.tr("Transfer"),
                      self.tr("Success sending money to {0}").format(recipient))
        else:
            await QAsyncMessageBox.information(self.widget, self.tr("Transfer"),
                      self.tr("Success sending money to {0}").format(recipient))

    async def show_error(self, notification, error_txt):
        if notification:
            toast.display(self.tr("Transfer"), "Error : {0}".format(error_txt))
        else:
            await QAsyncMessageBox.critical(self.widget, self.tr("Transfer"), error_txt)