#######################################################################
# File:             client_handler.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           client_handler = ClientHandler() # creates object
########################################################################

import sys
import threading
import pickle
import socket
from menu import Menu
from datetime import datetime


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """

    def __init__(self, ready, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.ready = ready
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.unread_messages = []
        # creates the print lock
        self.print_lock = threading.Lock()
        self.server.send_client_id(self.clientsocket, self.client_id)
        # retrieve user info
        client_info = self.server.receive(self.clientsocket)
        self.id_key = client_info['id_key']
        self.menu = Menu(self)
        self.ready.set()

    def run(self):
        """
        Run user prompts
        :return: VOID
        """
        # print client connected message
        print("New client \"" + self.id_key + "\" (#" + str(self.client_id) + ") connected.")
        while True:
            try:
                # handle closed pipe
                if self.clientsocket.fileno() == -1:
                    break
                # send default menu
                self._sendMenu()
                # waiting for user options
                while self.process_options():
                    continue
            except BrokenPipeError:
                # handle broken pipe
                break
            except:
                # handle other exceptions
                print("Failed at running at client thread: ", sys.exc_info()[0])
                raise
        # remove users from server client list
        self.delete_client_data()
        # print client disconnected message
        print("Existing client \"" + self.id_key + "\" (#" + str(self.client_id) + ") disconnected.")

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        data = {'menu': self.menu.get_menu()}
        self.server.send(self.clientsocket, data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return: BOOLEAN
        """
        data = self.server.receive(self.clientsocket)
        # check for disconnected socket
        if not data:
            return None
        # validates a valid option selected
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6:
            option = data['option_selected']
            if option == 1:
                return self._send_user_list()
            elif option == 2:
                return self._send_composer()
            elif option == 3:
                return self._send_messages()
            elif option == 4:
                return self._send_chat_creator()
            elif option == 5:
                return self._send_chat_enroller()
            elif option == 6:
                return self._disconnect_from_server()
        elif 'option' in data.keys() and 1 <= data['option'] <= 6:
            option = data['option']
            if option == 2:
                recipient_id = data['input'][1]
                message = data['input'][0]
                return self._save_message(recipient_id, message)
            elif option == 4:
                room_id = data['input'][0]
                return self._create_chat(room_id)
            elif option == 5:
                if (len(data['input']) == 1):
                    room_id = data['input'][0]
                    return self._join_chat(room_id)
                elif (len(data['input']) == 2):
                    room_id = data['input'][0]
                    message = data['input'][1]
                    return self._chatting(room_id, message)
                else:
                    print("Invalid request")
            else:
                print("Invalid request")
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
        send the list of users (clients ids) that are connected to this server.
        :return: BOOLEAN
        """
        # make users list
        users = []
        for client_id in self.server.clients:
            client = self.server.clients[client_id]
            users.append(client.id_key + ":" + str(client.client_id))
        # prepare and send result message
        data = self.menu.option1()
        data['output'] += ", ".join(users)
        self.server.send(self.clientsocket, data)
        return False

    def _send_composer(self):
        """
        send composer for messaging
        :return: BOOLEAN
        """
        # send composer
        self.server.send(self.clientsocket, self.menu.option2(False))
        return True

    def _save_message(self, recipient_id, message):
        """
        link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: BOOLEAN
        """
        try:
            recipient_id = int(recipient_id)
            # save message to recipient
            if recipient_id in self.server.clients:
                message = str(datetime.now()) + "   " + message + " (from: " + self.id_key + ")"
                self.server.clients[recipient_id].unread_messages.append(message)
            else:
                # handle failure
                print("Failed to find recipient id #" + str(recipient_id) + " for message \"" + message + "\".")
            # send result message
            self.server.send(self.clientsocket, self.menu.option2(True))
            return False
        except ValueError:
            # handle validation
            return self._send_composer()

    def _send_messages(self):
        """
        send all the unreaded messages of this client. if non unread messages found, send an empty list.
        make sure to delete the messages from list once the client acknowledges that they were read.
        :return: BOOLEAN
        """
        # prepare and send result message
        data = self.menu.option3()
        # find recipient messages
        if self.unread_messages:
            data['output'] += "\n" + "\n".join(self.unread_messages)
            # clear unread messages
            self.unread_messages = []
        else:
            data['output'] += "\nYour mailbox is empty."
        # send result message
        self.server.send(self.clientsocket, data)
        return False

    def _send_chat_creator(self):
        """
        send chat creator
        :return: BOOLEAN
        """
        # send chat creator
        self.server.send(self.clientsocket, self.menu.option4(False))
        return True

    def _create_chat(self, room_id):
        """
        Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: BOOLEAN
        """
        try:
            room_id = int(room_id)
            # check room id is valid
            if room_id in self.server.chatrooms.keys() or room_id <= 0:
                print("Cannot use existing room id or invalid room id")
                return self._send_chat_creator()
            # add room id to chatroom list
            self.server.chatrooms[room_id] = []
            # send result message
            self.server.send(self.clientsocket, self.menu.option4(True))
            return False
        except ValueError:
            print(sys.exc_info()[0])
            # handle validation
            return self._send_chat_creator()

    def _send_chat_enroller(self):
        """
        send chat enroller
        :return: BOOLEAN
        """
        # send chat enroller
        self.server.send(self.clientsocket, self.menu.option5("enroll"))
        return True

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: BOOLEAN
        """
        try:
            room_id = int(room_id)
            # check room id is valid
            if not room_id in self.server.chatrooms.keys() or room_id <= 0:
                print("Room id does not exist or invalid")
                return self._send_chat_enroller()
            # add client id to chatroom users
            self.server.chatrooms[room_id].append(self.client_id)
            # prepare and send welcome message
            data = self.menu.option5("welcome", room_id)
            data['output'] = "----------------------- Chat Room " + str(room_id) + " ------------------------"
            self.server.send(self.clientsocket, data)
            # prepare and send join message
            self.server.send(self.clientsocket, self.menu.option5("i_join"))
            # send join message for other clients in chatroom
            data = self.menu.option5("u_join")
            for recipient_id in self.server.chatrooms[room_id]:
                if recipient_id != self.client_id:
                    self.server.send(self.server.clients[recipient_id].clientsocket, data)
            # prepare and send talk message for current client
            self.server.send(self.clientsocket, self.menu.option5("i_talk", room_id))
            return True
        except ValueError:
            # handle validation
            return self._send_chat_enroller()

    def _chatting(self, room_id, message):
        """
        Chatting in a existing room
        :param room_id:
        :param message:
        :return: BOOLEAN
        """
        # leave chat if message is 'bye'
        if message == "bye":
            # remove client id from chatroom
            self.server.chatrooms[room_id].remove(self.client_id)
            # send leave message for current client
            self.server.send(self.clientsocket, self.menu.option5("i_leave"))
            # send join message for other clients in chatroom
            data = self.menu.option5("u_leave")
            for recipient_id in self.server.chatrooms[room_id]:
                if recipient_id != self.client_id:
                    self.server.send(self.server.clients[recipient_id].clientsocket, data)
            return False
        # send talk message to all chat recipient if message is not empty
        else:
            if len(message) > 0:
                data = self.menu.option5("u_talk", room_id)
                data['output'] = self.id_key + "> " + message
                for recipient_id in self.server.chatrooms[room_id]:
                    if recipient_id != self.client_id:
                        self.server.send(self.server.clients[recipient_id].clientsocket, data)
            # send talk message to current client
            self.server.send(self.clientsocket, self.menu.option5("i_talk", room_id))
        return True

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        # remove from server current client list
        self.server.clients.pop(self.client_id)

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        # send goodbye message
        self.server.send(self.clientsocket, self.menu.option6())
        self.clientsocket.close()
        return False
