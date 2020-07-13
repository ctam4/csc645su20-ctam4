#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################


class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self, client):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = client

    def set_client(self, client):
        self.client = client

    def get_menu(self):
        """
        Implement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = "****** TCP CHAT ******\n"
        menu += "-----------------------\n"
        menu += "Options Available:\n"
        menu += "1. Get user list\n"
        menu += "2. Send a message\n"
        menu += "3. Get my messages\n"
        menu += "4. Create a new channel\n"
        menu += "5. Chat in a channel with your friends\n"
        menu += "6. Disconnect from server"
        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        # requesting how many user input
        data['params'] = []
        # output message
        data['output'] = "Users in server: "
        return data

    def option2(self, status):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param status BOOLEAN:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        data['option'] = 2
        if not status:
            # requesting how many user input
            data['params'] = range(2)
            data['input'] = []
            # input[0] message
            data['input'].insert(0, "Enter your message: ")
            # input[1] message
            data['input'].insert(1, "Enter recipent id: ")
        else:
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = "Message sent!"
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = range(3)
        # requesting how many user input
        data['params'] = []
        # output message
        data['output'] = "My messages:"
        return data

    def option4(self, status):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option'] = 4
        if not status:
            # requesting how many user input
            data['params'] = range(1)
            data['input'] = []
            # input[0] message
            data['input'].insert(0, "Enter new room id: ")
        else:
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = "Chatroom created!"
        return data

    def option5(self, status=None, room_id=None):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        if status == "enroll":
            # requesting how many user input
            data['params'] = range(1)
            data['input'] = []
            # input[0] message
            data['input'].insert(0, "Enter chat room id to join: ")
        elif status == "welcome":
            # requesting how many user input
            data['params'] = []
        elif status == "i_talk":
            # requesting how many user input
            data['params'] = range(1, 2)
            data['input'] = []
            # input[0] message
            data['input'].insert(0, room_id)
            # input[1] message
            data['input'].insert(1, self.client.id_key + "> ")
        elif status == "u_talk":
            # requesting how many user input
            data['params'] = []
            # output message
        elif status == "i_join":
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = "Joined to chat room."
            data['output'] += "\nType 'bye' to exit this chat room."
            data['output'] += "\nEnter blank to refresh chat room."
        elif status == "i_leave":
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = "Left from chatroom."
        elif status == "u_join":
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = self.client.id_key + " joined."
        elif status == "u_leave":
            # requesting how many user input
            data['params'] = []
            # output message
            data['output'] = self.client.id_key + " left."
        return data

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option'] = 6
        # requesting how many user input
        data['params'] = []
        # output message
        data['output'] = "Goodbye! You are being disconnected from server."
        return data
