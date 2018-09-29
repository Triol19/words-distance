# words = ['a', 'x', 'x', 'x', 'b']
# words = ['b', 'x', 'x', 'x', 'a']
# words = ['a', 'x', 'x', 'x', 'a', 'b']
# words = ['b', 'x', 'x', 'x', 'b', 'a']
# words = ['a', 'x', 'x', 'x', 'b', 'x', 'a']
# words = ['b', 'x', 'x', 'x', 'a', 'x', 'b']
# words = ['a', 'x', 'x', 'x', 'b', 'x', 'b', 'x', 'b', 'a', 'a']
words = ['b', 'x', 'x', 'x', 'a', 'x', 'a', 'x', 'a', 'b', 'b']

if __name__ == '__main__':
    first_word = 'a'
    second_word = 'b'
    first_word_was_last = True
    first_distance_word_index = None
    second_distance_word_index = None
    last_first_word_index = None
    last_second_word_index = None
    for index, word in enumerate(words):
        if word == first_word:
            if first_distance_word_index is None:
                first_distance_word_index = index
                last_first_word_index = index
            elif first_word_was_last:
                last_first_word_index = index
            else:
                if index - last_second_word_index < second_distance_word_index - first_distance_word_index:
                    first_distance_word_index = index
                    last_first_word_index = index
                    second_distance_word_index = last_second_word_index
            first_word_was_last = True
        elif word == second_word:
            if second_distance_word_index is None:
                second_distance_word_index = index
                last_second_word_index = index
            elif not first_word_was_last:
                last_second_word_index = index
            else:
                if index - last_first_word_index < first_distance_word_index - second_distance_word_index:
                    second_distance_word_index = index
                    last_second_word_index = index
                    first_distance_word_index = last_first_word_index
            first_word_was_last = False
    print(abs(second_distance_word_index-first_distance_word_index)-1)
