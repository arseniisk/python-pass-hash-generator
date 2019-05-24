import urwid
import hashlib
import string
import nltk
import random
from random import choice

# Constants
words_file = open('words.txt', 'r')
all_words = words_file.read().split('\n')
words_file.close()

# App Controller
class App():
    def __init__(self):
        self.title = 'Hash and Password Generator'
        self.menuOptions = ['Generate Password', 'Generate Hash']
        self.hashAlgorithms = sorted(h.upper() for h in hashlib.algorithms_guaranteed)
        self.passLen = 0
        self.words = nltk.download('words')

        self.hashText = urwid.Text('')
        self.passTextRegular = urwid.Text('')
        self.passTextRemember = urwid.Text('')
        self.main = urwid.Padding(self.mainMenu(), left=2, right=2)
        self.top = urwid.Overlay(self.main, urwid.SolidFill('.'),
                            align='center', width=('relative', 90),
                            valign='middle', height=('relative', 85),
                            min_width=20, min_height=9)

        # Start Main Loop
        urwid.MainLoop(
            self.top, 
            palette = [('reversed', 'standout', '')],
            unhandled_input = self.unhandled,
        ).run()

    def unhandled(self, key):
        if key == 'enter':
            # Handle password length selection
            if self.main.original_widget.focus.caption == "Password Length? \n" :
                self.generatePassword(self.main.original_widget.focus.edit_text)

    def mainMenu(self):
        body = [
            urwid.Divider(),
            urwid.Text(self.title), 
            urwid.Divider()
        ]

        for opt in self.menuOptions:
            button = urwid.Button(opt)
            urwid.connect_signal(button, 'click', self.mainOptionSelected, opt)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def mainOptionSelected(self, button, opt):
        if opt == 'Generate Hash':
            self.hashMenu()
        elif opt == 'Generate Password':
            self.passwordMenu()

    # Terminate Program
    def exit(self, button):
        raise urwid.ExitMainLoop()

    def getExit(self):
        exitBtn = urwid.Button('Exit')
        urwid.connect_signal(exitBtn, 'click', self.exit)

        ret = [
            urwid.Divider(),
            urwid.AttrMap(exitBtn, None, focus_map='reversed'),
        ]

        return ret
        
    def hashMenu(self):
        # Menu Heading 
        hashBox = [
            urwid.Divider(),
            urwid.Text('Hash Generator'),
            urwid.Text('Please choose one of the algorithms provided by Python hashlib library'),
            urwid.Divider()
        ]

        # Append algorithm buttons
        for ha in self.hashAlgorithms:
            btn = urwid.Button(ha)
            # Connect Listener
            urwid.connect_signal(btn, 'click', self.hashAlgorithmSelected, ha)
            hashBox.append(urwid.AttrMap(btn, None, focus_map='reversed'))
        
        hashBox += self.getExit()

        # Update layout
        self.main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(hashBox))

    def passwordMenu(self):
        passLength = urwid.IntEdit('Password Length? \n')

        # Menu Heading 
        self.passBox = [
            urwid.Divider(),
            urwid.Text('Password Generator'),
            urwid.Divider(),
            passLength,
            urwid.Divider(),
            self.passTextRegular,
            self.passTextRemember,
        ]
        self.passBox += self.getExit()

        # Update layout
        self.main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(self.passBox))

    def hashAlgorithmSelected(self, button, algorithm):
        hashInput = urwid.Edit('Input the value you want to hash: \n')

        box = [
            urwid.Divider(),
            urwid.Text(f'{algorithm} Algorithm \n'), 
            hashInput,
            self.hashText
        ]
        box += self.getExit()

        urwid.connect_signal(hashInput, 'change', self.generateHash, algorithm)

        # Update layout
        self.main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(box))

    def generateHash(self, element, value, algorithm):
        h = hashlib.new(algorithm.lower())
        h.update(value.encode('utf-8'))

        self.hashText.set_text(f'\n{algorithm} Hash:\n{h.hexdigest()}')

    def generatePassword(self, length):
        passObj = Password(int(length))
        self.passTextRegular.set_text(f'Alphanumeric: {passObj.passwordRegular}')
        self.passTextRemember.set_text(f'Easy-to-Remember: {passObj.passwordRemember}')

class Password(): 
    def __init__(self, length) :
        self.alphabet = string.ascii_letters + string.digits
        self.length = length
        self.words = all_words
        self.passwordRegular = ''
        self.passwordRemember = ''

        self.validate()
    
    def validate(self):
        if self.length <= 8:
            self.passwordRegular = 'Password must be bigger than 8 characters'
        elif self.length >= 100:
            self.passwordRegular = 'Password must be smaller than 100 characters'
        else :
            self.generateRegular()
            self.generateRemember()

    def generateRegular(self):
        while True:
            self.passwordRegular = ''.join(choice(self.alphabet) for i in range(self.length))
            if (any(c.islower() for c in self.passwordRegular)
                and any(c.isupper() for c in self.passwordRegular)
                and sum(c.isdigit() for c in self.passwordRegular) >= 3):
                break

    def generateRemember(self):
        specialChars = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

        while True:
            randWord = choice(all_words).capitalize()
            randWord += str(random.randint(0,10))
            self.passwordRemember += randWord
            if (len(self.passwordRemember) >= self.length):
                self.passwordRemember = self.passwordRemember[:self.length - 1]
                self.passwordRemember += random.choice(specialChars)
                break

# App Init
if __name__ == '__main__':
    app = App()