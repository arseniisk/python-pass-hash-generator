import urwid
import hashlib

# App Controller
class App():
    def __init__(self):
        self.title = 'Hash and Password Generator'
        self.menuOptions = ['Generate Hash','Generate Password']
        self.hashAlgorithms = sorted(h.upper() for h in hashlib.algorithms_guaranteed)

        self.hashText = urwid.Text('')
        self.main = urwid.Padding(self.mainMenu(), left=2, right=2)
        self.top = urwid.Overlay(self.main, urwid.SolidFill('.'),
                            align='center', width=('relative', 90),
                            valign='middle', height=('relative', 85),
                            min_width=20, min_height=9)

        # Start Main Loop
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

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

    # Terminate Program
    def exit(self, button):
        raise urwid.ExitMainLoop()

    def goBack(self):
        print('not ready yet')
        
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
        
        # Back and Exit Buttons
        hashBox.append(urwid.Divider())

        backBtn = urwid.Button('Back')
        urwid.connect_signal(backBtn, 'click', self.goBack)
        hashBox.append(urwid.AttrMap(backBtn, None, focus_map='reversed'))

        exitBtn = urwid.Button('Exit')
        urwid.connect_signal(exitBtn, 'click', self.exit)
        hashBox.append(urwid.AttrMap(exitBtn, None, focus_map='reversed'))

        # Update layout
        self.main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(hashBox))

    def hashAlgorithmSelected(self, button, algorithm):
        hashInput = urwid.Edit('Input the value you want to hash: \n')

        box = [
            urwid.Divider(),
            urwid.Text(f'{algorithm} Algorithm \n'), 
            hashInput,
            self.hashText
        ]

        urwid.connect_signal(hashInput, 'change', self.generateHash, algorithm)

        # Update layout
        self.main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(box))

    def generateHash(self, element, value, algorithm):
        h = hashlib.new(algorithm.lower())
        h.update(value.encode('utf-8'))

        self.hashText.set_text(f'\n{algorithm} Hash:\n{h.hexdigest()}')

# App Init
if __name__ == '__main__':
    app = App()