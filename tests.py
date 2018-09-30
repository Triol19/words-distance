from unittest import TestCase, mock

from distance import find_distance


class DistanceSearchScriptTestCase(TestCase):
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find_distance('a', 'b', 'incorrect_file_name')

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_not_found_first_word_case_sensitive(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a x x x b'])
        )

        distance = find_distance('A', 'b')
        self.assertIsNone(distance)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_not_found_second_word_case_sensitive(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a x x x b'])
        )

        distance = find_distance('a', 'B')
        self.assertIsNone(distance)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_success_case_insensitive(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a x x x b'])
        )

        distance = find_distance('A', 'B', ci=True)
        self.assertEqual(distance, 3)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_line_from_task(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(
                ['We do value and reward motivation in our development team. Development is a key skill for a DevOp.']
            )
        )

        distance = find_distance('motivation', 'development')
        self.assertEqual(distance, 2)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_simple_case(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a x x x b x b x a'])
        )

        distance = find_distance('a', 'b')
        self.assertEqual(distance, 1)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_reverted_simplest_case(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a x x x b x b x a'])
        )

        distance = find_distance('b', 'a')
        self.assertEqual(distance, 1)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_simple_case_with_punctuation(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(['a, !x x x b: x .b x   a'])
        )

        distance = find_distance('a', 'b')
        self.assertEqual(distance, 1)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_simple_case_several_lines(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(
                [
                    'a x x',
                    'x b x',
                    'b x a',
                ]
            )
        )

        distance = find_distance('a', 'b')
        self.assertEqual(distance, 1)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_reverted_simple_case_several_lines(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(
                [
                    'b x x',
                    'x a x',
                    'a x b',
                ]
            )
        )

        distance = find_distance('a', 'b')
        self.assertEqual(distance, 1)

    @mock.patch('builtins.open', new_callable=mock.mock_open, create=True)
    def test_simple_case_several_lines_with_punctuation(self, mock_open):
        mock_open.return_value.__enter__ = mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value=iter(
                [
                    'a, !x x',
                    'x b: x',
                    '  .b x   a  ',
                ]
            )
        )

        distance = find_distance('a', 'b')
        self.assertEqual(distance, 1)
