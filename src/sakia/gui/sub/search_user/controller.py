from PyQt5.QtCore import pyqtSignal, QObject

from sakia.data.entities import Identity
from sakia.decorators import asyncify
from .model import SearchUserModel
from .view import SearchUserView


class SearchUserController(QObject):
    """
    The navigation panel
    """
    search_started = pyqtSignal()
    search_ended = pyqtSignal()
    identity_selected = pyqtSignal(Identity)

    def __init__(self, parent, view, model):
        """
        :param sakia.gui.agent.controller.AgentController parent: the parent
        :param sakia.gui.search_user.view.SearchUserView view:
        :param sakia.gui.search_user.model.SearchUserModel model:
        """
        super().__init__(parent)
        self.view = view
        self.model = model
        self.view.search_requested.connect(self.search)
        self.view.node_selected.connect(self.select_node)

    @classmethod
    def create(cls, parent, app, currency):
        view = SearchUserView(parent.view)
        model = SearchUserModel(parent, app, currency)
        search_user = cls(parent, view, model)
        model.setParent(search_user)
        return search_user

    @asyncify
    async def search(self, text):
        """
        Search for a user
        :param text:
        :return:
        """
        if len(text) > 2:
            await self.model.find_user(text)
        user_nodes = self.model.user_nodes()
        self.view.set_search_result(text, user_nodes)

    def current_identity(self):
        """

        :rtype: sakia.core.registry.Identity
        """
        return self.model.identity()

    def select_node(self, index):
        """
        Select node in graph when item is selected in combobox
        """
        self.model.select_identity(index)
        self.identity_selected.emit(self.model.identity())

    def set_currency(self, currency):
        self.model.currency = currency
