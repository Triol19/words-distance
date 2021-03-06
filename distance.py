import re
import argparse
from typing import List, Tuple, Optional


def prepare_line_words(line: str, ci: bool) -> List[str]:
    new_line = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', line))
    if ci:
        new_line = new_line.lower()
    return new_line.strip().split(' ')


def calc_abs_current_index(
    prev_line_last_index: int, current_line_index: int
) -> int:
    return prev_line_last_index + current_line_index


def recalculate_indexes(
    this_word: int, another_word: int,
    this_word_last_occur: int, another_word_last_occur: int,
    current: int, this_word_was_last: int
) -> Tuple[int, int, int]:
    if this_word is None:
        this_word = current
        this_word_last_occur = current
    elif this_word_was_last:
        if another_word is None:
            this_word = current
        this_word_last_occur = current
    else:
        if current - another_word_last_occur < another_word - this_word:
            this_word = current
            this_word_last_occur = current
            another_word = another_word_last_occur
    return this_word, another_word, this_word_last_occur


def find_distance(
    first_word: str, second_word: str,
    filename: str = 'file_to_process.txt', ci: bool = False
) -> Optional[int]:
    if ci:
        first_word = first_word.lower()
        second_word = second_word.lower()
    first_word_was_last = True
    first_distance_word_index = None
    second_distance_word_index = None
    last_first_word_index = None
    last_second_word_index = None

    file_last_line_index = 0
    with open(filename) as f:
        for line in f:
            words = prepare_line_words(line, ci)
            for index, word in enumerate(words):
                abs_index = calc_abs_current_index(file_last_line_index, index)
                if word == first_word:
                    (
                        first_distance_word_index,
                        second_distance_word_index,
                        last_first_word_index
                    ) = recalculate_indexes(
                        this_word=first_distance_word_index,
                        another_word=second_distance_word_index,
                        this_word_last_occur=last_first_word_index,
                        another_word_last_occur=last_second_word_index,
                        current=abs_index,
                        this_word_was_last=first_word_was_last
                    )
                    first_word_was_last = True
                elif word == second_word:
                    (
                        second_distance_word_index,
                        first_distance_word_index,
                        last_second_word_index
                    ) = recalculate_indexes(
                        this_word=second_distance_word_index,
                        another_word=first_distance_word_index,
                        this_word_last_occur=last_second_word_index,
                        another_word_last_occur=last_first_word_index,
                        current=abs_index,
                        this_word_was_last=not first_word_was_last
                    )
                    first_word_was_last = False
            file_last_line_index += len(words)
            if (
                first_distance_word_index and
                second_distance_word_index and
                not abs(second_distance_word_index - first_distance_word_index)
            ):
                break
    if first_distance_word_index is None:
        print('Word "{}" was not found'.format(first_word))
    if second_distance_word_index is None:
        print('Word "{}" was not found'.format(second_word))
    if first_distance_word_index is not None and second_distance_word_index is not None:
        return abs(second_distance_word_index - first_distance_word_index) - 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='File to process', default='file_to_process.txt'
    )
    parser.add_argument(
        '-ci', '--case_insensitive', type=bool, help='Either case insensitive', default=False
    )
    parser.add_argument('-w1', '--word1', help='First word', required=True)
    parser.add_argument('-w2', '--word2', help='Second word', required=True)
    args = parser.parse_args()
    assert args.word1 != args.word2, 'Don\'t try to find distance between the same words'

    distance = find_distance(
        args.word1, args.word2, args.file, args.case_insensitive
    )

    if distance is not None:
        print('The shortest distance is {}'.format(distance))


if __name__ == '__main__':
    main()
