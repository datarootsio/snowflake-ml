import os
import re

from snowflake_ml._vendor import inflection

BADWORDS = ['@$$',
 'AssMonkey',
 'Assface',
 'Biatch',
 'BlowJob',
 'CarpetMuncher',
 'Clit',
 'Cock',
 'CockSucker',
 'Ekrem',
 'Ekto',
 'Felcher',
 'Flikker',
 'Fotze',
 'Fu',
 'FudgePacker',
 'Fukah',
 'Fuken',
 'Fukin',
 'Fukk',
 'Fukkah',
 'Fukken',
 'Fukker',
 'Fukkin',
 'Goddamned',
 'Huevon',
 'Kurac',
 'Lesbian',
 'Lezzian',
 'Lipshits',
 'Lipshitz',
 'MothaFucker',
 'MothaFuker',
 'MothaFukkah',
 'MothaFukker',
 'MotherFucker',
 'MotherFukah',
 'MotherFuker',
 'MotherFukkah',
 'MotherFukker',
 'MuthaFucker',
 'MuthaFukah',
 'MuthaFuker',
 'MuthaFukkah',
 'MuthaFukker',
 'Phuc',
 'Phuck',
 'Phuk',
 'Phuker',
 'Phukker',
 'Poonani',
 'Shitty',
 'Shity',
 'Sht',
 'Shyt',
 'Shyte',
 'Shytty',
 'Skanky',
 'Slutty',
 'ahole',
 'amcik',
 'andskota',
 'anus',
 'arschloch',
 'arse',
 'ash0le',
 'ash0les',
 'asholes',
 'ass',
 'assh0le',
 'assh0lez',
 'asshole',
 'assholes',
 'assholz',
 'assrammer',
 'asswipe',
 'ayir',
 'azzhole',
 'b00bs',
 'b17ch',
 'b1tch',
 'bassterds',
 'bastard',
 'bastards',
 'bastardz',
 'basterds',
 'basterdz',
 'bch',
 'bi7ch',
 'bich',
 'bitch',
 'bitches',
 'blowjob',
 'boffing',
 'boiolas',
 'bollock',
 'boobs',
 'breasts',
 'btch',
 'buceta',
 'bullshit',
 'butthole',
 'buttpirate',
 'buttwipe',
 'c0ck',
 'c0cks',
 'c0k',
 'cabron',
 'cawk',
 'cawks',
 'cazzo',
 'chink',
 'chraa',
 'chuj',
 'cipa',
 'clit',
 'clits',
 'cnts',
 'cntz',
 'cock',
 'cockhead',
 'cocks',
 'cocksucker',
 'crap',
 'cum',
 'cunt',
 'cunts',
 'cuntz',
 'd4mn',
 'damn',
 'daygo',
 'dego',
 'dick',
 'dike',
 'dild0',
 'dild0s',
 'dildo',
 'dildos',
 'dilld0',
 'dilld0s',
 'dirsa',
 'dominatricks',
 'dominatrics',
 'dominatrix',
 'dupa',
 'dyke',
 'dziwka',
 'ejackulate',
 'ejakulate',
 'enculer',
 'enema',
 'faen',
 'fag',
 'fag1t',
 'faget',
 'fagg1t',
 'faggit',
 'faggot',
 'fagit',
 'fags',
 'fagz',
 'faig',
 'faigs',
 'fanculo',
 'fanny',
 'fart',
 'fatass',
 'fcuk',
 'feces',
 'feg',
 'ficken',
 'fitt',
 'flipping',
 'foreskin',
 'fuchah',
 'fuck',
 'fucka',
 'fucker',
 'fuckin',
 'fucking',
 'fucks',
 'fuk',
 'fukah',
 'fuker',
 'fukka',
 'fukkah',
 'fukker',
 'futkretzn',
 'fux0r',
 'g00k',
 'gay',
 'gaybor',
 'gayboy',
 'gaygirl',
 'gays',
 'gayz',
 'gook',
 'guiena',
 'h00r',
 'h0ar',
 'h0r',
 'h0re',
 'h4x0r',
 'hell',
 'hells',
 'helvete',
 'hoar',
 'hoer',
 'honkey',
 'hoor',
 'hoore',
 'hore',
 'hui',
 'injun',
 'jackoff',
 'jap',
 'japs',
 'jerkoff',
 'jisim',
 'jism',
 'jiss',
 'jizm',
 'jizz',
 'kanker',
 'kawk',
 'kike',
 'klootzak',
 'knob',
 'knobs',
 'knobz',
 'knulle',
 'kraut',
 'kuk',
 'kuksuger',
 'kunt',
 'kunts',
 'kuntz',
 'kurwa',
 'kusi',
 'kyrpa',
 'l3i+ch',
 'l3itch',
 'lesbian',
 'lesbo',
 'mamhoon',
 'masochist',
 'masokist',
 'massterbait',
 'masstrbait',
 'masstrbate',
 'masterbaiter',
 'masterbat',
 'masterbat3',
 'masterbate',
 'masterbates',
 'masturbat',
 'masturbate',
 'merd',
 'mibun',
 'mofo',
 'monkleigh',
 'motha',
 'motherfucker',
 'mouliewop',
 'muie',
 'mulkku',
 'muschi',
 'mutha',
 'n1gr',
 'nastt',
 'nasty',
 'nazi',
 'nazis',
 'nepesaurio',
 'nigga',
 'niggas',
 'nigger',
 'nigur',
 'niiger',
 'niigr',
 'nutsack',
 'orafis',
 'orgasim',
 'orgasm',
 'orgasum',
 'oriface',
 'orifice',
 'orifiss',
 'orospu',
 'p0rn',
 'packi',
 'packie',
 'packy',
 'paki',
 'pakie',
 'paky',
 'paska',
 'pecker',
 'peeenus',
 'peeenusss',
 'peenus',
 'peinus',
 'pen1s',
 'penas',
 'penis',
 'penisbreath',
 'penus',
 'penuus',
 'perse',
 'phuck',
 'picka',
 'pierdol',
 'pillu',
 'pimmel',
 'pimpis',
 'piss',
 'pizda',
 'polac',
 'polack',
 'polak',
 'poontsee',
 'poop',
 'porn',
 'pr0n',
 'pr1c',
 'pr1ck',
 'pr1k',
 'preteen',
 'pula',
 'pule',
 'pusse',
 'pussee',
 'pussy',
 'puta',
 'puto',
 'puuke',
 'puuker',
 'qahbeh',
 'queef',
 'queer',
 'queers',
 'queerz',
 'qweers',
 'qweerz',
 'qweir',
 'rautenberg',
 'recktum',
 'rectum',
 'retard',
 's.o.b.',
 'sadist',
 'scank',
 'schaffer',
 'scheiss',
 'schlampe',
 'schlong',
 'schmuck',
 'screw',
 'screwing',
 'scrotum',
 'semen',
 'sex',
 'sexx',
 'sexxx',
 'sexy',
 'sh1t',
 'sh1ter',
 'sh1ts',
 'sh1tter',
 'sh1tz',
 'sharmuta',
 'sharmute',
 'shemale',
 'shi+',
 'shipal',
 'shit',
 'shits',
 'shitt',
 'shitter',
 'shitz',
 'shiz',
 'skanck',
 'skank',
 'skankee',
 'skankey',
 'skanks',
 'skrib',
 'slut',
 'sluts',
 'slutz',
 'smut',
 'sonofabitch',
 'sx',
 'teets',
 'teez',
 'testical',
 'testicle',
 'tit',
 'tits',
 'titt',
 'turd',
 'va1jina',
 'vag1na',
 'vagiina',
 'vagina',
 'vaj1na',
 'vajina',
 'vullva',
 'vulva',
 'w00se',
 'w0p',
 'wank',
 'wh00r',
 'wh0re',
 'whoar',
 'whore',
 'xrated',
 'xxx']

class ProfanityFilter:
    def __init__(self, **kwargs):
        """
        Returns a ProfanityFilter instance.

        Kwargs:
            - custom_censor_list (list): 
                A custom list of bad words to be used instead of the default list.
            - extra_censor_list (list): 
                A custom list of bad words to be used in conjunction with the default list.
            - no_word_boundaries (bool): 
                False means no word boundaries will be used in the regex for bad words. 
                i.e abc\ **badword**\ abc will be treated as profane.
        """

        # If defined, use this instead of _censor_list
        self._custom_censor_list = kwargs.get("custom_censor_list", [])

        # Words to be used in conjunction with _censor_list
        self._extra_censor_list = kwargs.get("extra_censor_list", [])

        # Toggle use of word boundaries in regex
        self._no_word_boundaries = kwargs.get("no_word_boundaries", False)

        # What to be censored -- should not be modified by user
        self._censor_list = []

        # What to censor the words with
        self._censor_char = "*"

        # Where to find the censored words
        self._BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        self._words_file = os.path.join(self._BASE_DIR, 'data', 'badwords.txt')

        self._load_words()

    def _load_words(self):
        """Loads the list of profane words from file."""
        # with open(self._words_file, 'r') as f:
        self._censor_list = BADWORDS

    def define_words(self, word_list):
        """Define a custom list of profane words to be used instead of the default list."""
        self._custom_censor_list = word_list

    def append_words(self, word_list):
        """Define a custom list of profane words to be used in conjunction with the default list."""
        self._extra_censor_list.extend(word_list)

    def remove_word(self, word):
        """Remove given word from censor list."""
        self._censor_list.remove(word)

    def set_censor(self, character):
        """Replaces the original censor character '*' with ``character``."""
        # TODO: what if character isn't str()-able?
        if isinstance(character, int):
            character = str(character)
        self._censor_char = character

    def has_bad_word(self, text):
        """Returns True if text contains profanity, False otherwise."""
        return self.censor(text) != text

    def get_custom_censor_list(self):
        """Returns the list of custom profane words."""
        return self._custom_censor_list

    def get_extra_censor_list(self):
        """Returns the list of custom additional profane words."""
        return self._extra_censor_list

    def get_profane_words(self):
        """Returns all profane words currently in use."""
        profane_words = []

        if self._custom_censor_list:
            profane_words = [w for w in self._custom_censor_list]  # Previous versions of Python don't have list.copy()
        else:
            profane_words = [w for w in self._censor_list]

        profane_words.extend(self._extra_censor_list)
        profane_words.extend([inflection.pluralize(word) for word in profane_words])
        profane_words = list(set(profane_words))
        
        # We sort the list based on decreasing word length so that words like
        # 'fu' aren't substituted before 'fuck' if no_word_boundaries = true
        profane_words.sort(key=len)
        profane_words.reverse()

        return profane_words

    def restore_words(self):
        """Clears all custom censor lists and reloads the default censor list."""
        self._custom_censor_list = []
        self._extra_censor_list = []
        self._load_words()

    def censor(self, input_text):
        """Returns input_text with any profane words censored."""
        bad_words = self.get_profane_words()
        res = input_text

        for word in bad_words:
            # Apply word boundaries to the bad word
            regex_string = r'{0}' if self._no_word_boundaries else r'\b{0}\b'
            regex_string = regex_string.format(word)  
            regex = re.compile(regex_string, re.IGNORECASE)
            res = regex.sub(self._censor_char * len(word), res)

        return res


    def is_clean(self, input_text):
        """Returns True if input_text doesn't contain any profane words, False otherwise."""
        return not self.has_bad_word(input_text)


    def is_profane(self, input_text):
        """Returns True if input_text contains any profane words, False otherwise."""
        return self.has_bad_word(input_text)
