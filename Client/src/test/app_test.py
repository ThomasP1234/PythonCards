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

if __name__ == "__main__":
    unittest.main()