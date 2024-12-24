import sys
from Cocoa import (
    NSApplication,
    NSApp,
    NSObject,
    NSApplicationActivationPolicyAccessory,
    NSMenu,
    NSMenuItem,
    NSStatusBar,
    NSTextField,
    NSMakeRect,
    NSVariableStatusItemLength,
    NSImage,
    NSSize
)
from PyObjCTools.AppHelper import runEventLoop
import subprocess
import os
from LLM_wrappers.openai_wrapper import OpenAIChat

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # 1. Create the status item in the menu bar
        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength
        )
        
        # 2. Load icon.png (if it exists) and set it as the menubar icon
        icon = NSImage.alloc().initWithContentsOfFile_("icon.png")
        if icon:
            # You can adjust this size as needed
            icon.setSize_(NSSize(18, 18))
            self.statusItem.button().setImage_(icon)
        else:
            # Fallback if icon not found: just use text
            self.statusItem.button().setTitle_("Menu")

        # 3. Create the dropdown menu
        menu = NSMenu.alloc().init()

        # 4. Create an NSMenuItem that holds an NSTextField
        textFieldItem = NSMenuItem.alloc().init()
        textField = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 22))
        textField.setPlaceholderString_("Enter text")

        # 5. Assign target/action so pressing Enter calls submitText_()
        textField.setTarget_(self)
        textField.setAction_("submitText:")

        # 6. Embed the text field in the NSMenuItem
        textFieldItem.setView_(textField)

        # 7. Add the text field item to the menu
        menu.addItem_(textFieldItem)

        # 8. Add a separator and a “Quit” menu item
        menu.addItem_(NSMenuItem.separatorItem())
        quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit",
            "quitApp:",
            ""
        )
        menu.addItem_(quitItem)

        # 9. Assign this menu to our status item
        self.statusItem.setMenu_(menu)

    def submitText_(self, sender):
        userInput = sender.stringValue()
        print(f"Submitted text: {userInput}")
        # Close the menu
        self.statusItem.menu().cancelTracking()
        # Clear the text field
        sender.setStringValue_("")
        # Take a ss
        ss_path = self.take_screenshot()
        # TODO: send ss to llm with text to figure out what to do

        # Example usage
        self.send_to_llm(ss_path, userInput, model="gpt-4o")
        
        # TODO: Delete ss
    
    def take_screenshot(self, output_path=os.path.join(os.path.dirname(__file__), "temp_ss.png")):
        """
        Takes a screenshot of the entire screen on macOS
        and saves it as a file.
        """
        subprocess.run(["screencapture", output_path])
        return output_path
    
    def send_to_llm(self, screenshot_path, text, model="gpt-4o"):
        if model == "gpt-4o":
            # Code to send to gpt-4o
            pass
        elif model == "o1":
            # Code to send to o1
            pass
        elif model == "sonnet-3.5":
            # Code to send to sonnet-3.5
            pass
        else:
            raise ValueError(f"Unsupported model: {model}")

    def quitApp_(self, sender):
        # Remove the status item before terminating
        NSStatusBar.systemStatusBar().removeStatusItem_(self.statusItem)
        NSApp.terminate_(self)

def main():
    app = NSApplication.sharedApplication()
    # This policy ensures your app won’t appear in the Dock, just the menubar
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    # Start the event loop
    runEventLoop()

if __name__ == "__main__":
    main()