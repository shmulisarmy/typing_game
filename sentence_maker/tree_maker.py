from collections import Counter
from .resources import sentences, words

"""its just a different kind of search algorithm"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    @staticmethod
    def returns_best_letter(user_letters: list, branch: dict):
        """status: pure
        this function returns a letter for the calling 
        function to use to go down a path in the tree 
        structure that replicates what the users most 
        common letters look like
        """
        return next((letter for letter in user_letters.lower() if letter in branch), next(iter(branch.keys())))

    def insert(self, word):
        """goes down the tree structure in the path
        of the word thats passed in and creates
        new trees if they dont exist and marks
        the end of the word"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def find_best_word(self, user_letters: list):
        node = self.root
        word_being_made = []
        while not node.is_end_of_word:
            best_letter = Trie.returns_best_letter(user_letters=user_letters, branch=node.children)
            word_being_made.append(best_letter)
            node = node.children[best_letter]
        return ''.join(word_being_made)
    
    @staticmethod
    def make_tree(lst):
        """non decorating wrapper function"""
        tree = Trie()
        for word in lst:
            tree.insert(word)
        return tree


    @staticmethod
    def turn_into_reverse_hash_dictionary(lst):
        #example: [(l, 3), (a, 2)] -> 'la'
        turns_counter_list_tuple_into_string = lambda counter_list: ''.join(i[0] for i in counter_list)
        return {turns_counter_list_tuple_into_string(Counter(i).most_common(5)): i for i in lst}
        # apple => pale
        #return_example {'pale': 'apple'}
                
def get_best_sentence(users_reverse_hash):
    """after generating the sentence the function
    looks through ever word and tries to determine 
    if there's a better word that can replace said word"""
    uses_better_word_if_available = lambda word: replacment_word_trees[word].find_best_word(users_reverse_hash) if word in replacment_word_trees else word
    return ' '.join(map(uses_better_word_if_available, sentence_hash_dictionary[sentence_tree.find_best_word(users_reverse_hash)].split(' ')))

# words_dictionary =  {key: turn_into_reverse_hash_dictionary(lst) for key, lst in words.replacement_words.items()}             
# print(words_dictionary)

sentence_hash_dictionary = Trie.turn_into_reverse_hash_dictionary(sentences.sentences)

sentence_tree = Trie.make_tree(sentence_hash_dictionary.keys())

replacment_word_trees = {word_list_key: Trie.make_tree(word_list) for word_list_key, word_list in words.replacement_words.items()}


print(get_best_sentence("skbc"))