import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

import unittest
from unittest.mock import patch, MagicMock
from Client.src.main.app import App
import socket

class Test_App(unittest.TestCase):
    @patch("socket.socket")
    def test_createSocket(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        test_app = App()
        test_app.createSocket()

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)

    @patch("socket.socket")
    def test_endSocket(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        test_app = App()
        test_app.endSocket(mock_socket)

        mock_socket.close.assert_called_once()

    @patch("socket.socket")
    def test_setupSocket(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        test_app = App()
        test_app.setupSocket(mock_socket, ip:='127.0.0.1', port:=26100)

        mock_socket.bind.asser_called_once_with((ip, port))

    @patch("socket.socket")
    @patch("Client.src.main.app.App.verifySendToServer")
    def test_sendToServerTrue(self, mock_function, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        test_app = App()

        test_app.sendToServer(mock_socket, "Test", 30, True)
        mock_socket.send.assert_called_once_with("Test".encode("utf-8"))
        
        mock_function.assert_called_once_with(mock_socket, "Test", 30)

    @patch("socket.socket")
    @patch("Client.src.main.app.App.verifySendToServer")
    def test_sendToServerFalse(self, mock_function, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        test_app = App()
        test_app.sendToServer(mock_socket, "Test", 30, False)
        mock_socket.send.assert_called_once_with("Test".encode("utf-8"))
        
        mock_function.assert_not_called()

    @patch("socket.socket")
    @patch("Client.src.main.app.App.reciveFromServer")
    def test_verifySendToServer(self, mock_function, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        mock_function.return_value = "Test"
        
        test_app = App()
        test_app.verifySendToServer(mock_socket, "Test", 30)

        mock_function.assert_called_once_with(mock_socket, 30, False)

    @patch("socket.socket")
    @patch("Client.src.main.app.App.sendToServer")
    def test_reciveFromServerTrue(self, mock_function, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        mock_socket.recv.return_value = 'data'.encode('utf-8')

        test_app = App()
        test_app.reciveFromServer(mock_socket, 30, True)
        mock_socket.recv.assert_called_once_with(30)
        
        mock_function.assert_called_once_with(mock_socket, 'data', 30, False)

    @patch("socket.socket")
    @patch("Client.src.main.app.App.sendToServer")
    def test_reciveFromServerFalse(self, mock_function, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        mock_socket.recv.return_value = 'data'.encode('utf-8')

        test_app = App()
        test_app.reciveFromServer(mock_socket, 30, False)
        mock_socket.recv.assert_called_once_with(30)
        
        mock_function.assert_not_called()

if __name__ == "__main__":
    unittest.main()