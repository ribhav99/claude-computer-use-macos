#!/usr/bin/env python3

import sys
from Cocoa import (
    NSApplication,
    NSApp,
    NSObject,
    NSApplicationActivationPolicyAccessory,
    NSMenu,
    NSMenuItem,
    NSStatusBar,
    NSStatusItem,
    NSTextField,
    NSMakeRect,
    NSVariableStatusItemLength
)
from PyObjCTools.AppHelper import runEventLoop

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # 1. Create the status item in the menu bar
        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength
        )
        
        # 2. Give the menu bar button a title
        self.statusItem.button().setTitle_("Menu")
        
        # 3. Create the dropdown menu
        menu = NSMenu.alloc().init()
        
        # 4. Create an NSMenuItem that holds an NSTextField
        textFieldItem = NSMenuItem.alloc().init()
        textField = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 22))
        textField.setPlaceholderString_("Enter text")

        # 5. Assign target/action to trigger submitText_() on Enter
        textField.setTarget_(self)
        textField.setAction_("submitText:")

        # 6. Set the text field as the view of the NSMenuItem
        textFieldItem.setView_(textField)

        # 7. Add the text field item to the menu
        menu.addItem_(textFieldItem)

        # 8. Add a separator and a Quit item
        menu.addItem_(NSMenuItem.separatorItem())
        quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", 
            "quitApp:",
            ""
        )
        menu.addItem_(quitItem)

        # 9. Assign the menu to our status item
        self.statusItem.setMenu_(menu)

    def submitText_(self, sender):
        userInput = sender.stringValue()
        print(f"Submitted text: {userInput}")
        sender.setStringValue_("")

    def quitApp_(self, sender):
        # Remove the item from the menu bar
        NSStatusBar.systemStatusBar().removeStatusItem_(self.statusItem)
        # Terminate the app
        NSApp.terminate_(self)

def main():
    app = NSApplication.sharedApplication()
    # Use “Accessory” policy so it won’t show in Dock, only in menubar
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    # Start the app event loop
    runEventLoop()

if __name__ == "__main__":
    main()