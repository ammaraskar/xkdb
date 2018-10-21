import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import console


class TestConsole(unittest.TestCase):
    def test_get_string(self):
        # Test to see if we can parse null terminate strings
        test_string = b"Hello\0World!\0This is a null terminated string"

        read_cursor = 0
        string1, length = console.get_string(test_string[read_cursor:])

        self.assertEqual(string1, "Hello")
        self.assertEqual(length, 6)

        read_cursor += length

        string2, length = console.get_string(test_string[read_cursor:])
        
        self.assertEqual(string2, "World!")
        self.assertEqual(length, 7)

        read_cursor += length

        string3, length = console.get_string(test_string[read_cursor:])

        self.assertEqual(string3, "This is a null terminated string")
        self.assertEqual(length, 32)

backends1 = [
    console.Backend('xinu01', 'quark', None, None),
    console.Backend('xinu02', 'galileo', 'anon', '21:30')
]
backends2 = [
    console.Backend('xinu03', 'quark', None, None),
    console.Backend('xinu04', 'quark', None, None)
]
mock_servers = [
    console.BackendServer('server1', 'server1.example.com', backends1),
    console.BackendServer('server2', 'server2.example.com', backends2)
]

@mock.patch('argparse._sys.argv', ['console.py', '--status'])
@mock.patch('console.get_backend_servers')
def test_main_status(get_backend_servers, capsys):
    get_backend_servers.return_value = mock_servers

    console.main()

    captured = capsys.readouterr()

    get_backend_servers.assert_called_once()
    assert 'xinu01' in captured.out
    assert 'xinu04' in captured.out
    assert 'quark' in captured.out
    assert 'galileo' in captured.out
    assert 'anon' in captured.out
    assert '21:30' in captured.out

@mock.patch('argparse._sys.argv', ['console.py', 'xinu02'])
@mock.patch('console.get_backend_servers')
def test_get_specific_backend_in_use(get_backend_servers, capsys):
    get_backend_servers.return_value = mock_servers

    console.main()

    get_backend_servers.assert_called_once()
    captured = capsys.readouterr()
    assert 'Backend xinu02 is in use by anon' in captured.out

@mock.patch('argparse._sys.argv', ['console.py', 'nope'])
@mock.patch('console.get_backend_servers')
def test_get_specific_backend_non_existent(get_backend_servers, capsys):
    get_backend_servers.return_value = mock_servers

    console.main()

    get_backend_servers.assert_called_once()
    captured = capsys.readouterr()
    assert 'Backend nope not found' in captured.out