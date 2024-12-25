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
    NSSize,
    NSScrollView,
    NSTextView,
    NSBezelBorder,
    NSViewHeightSizable,
    NSViewWidthSizable,
    NSFont,
    NSButton,
    NSButtonTypeSwitch
)
from PyObjCTools.AppHelper import runEventLoop
import subprocess
import os
from LLM_wrappers.openai_wrapper import OpenAIChat

global_assistant = OpenAIChat(model="gpt-4o")

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
        
        # Create the dropdown menu
        menu = NSMenu.alloc().init()

        # Add chat history view
        chatHistoryItem = NSMenuItem.alloc().init()
        
        # Create scroll view to contain the chat
        scrollView = NSScrollView.alloc().initWithFrame_(NSMakeRect(0, 0, 300, 400))
        scrollView.setBorderType_(NSBezelBorder)
        scrollView.setHasVerticalScroller_(True)
        
        # Create text view for chat history
        self.chatView = NSTextView.alloc().initWithFrame_(scrollView.contentView().frame())
        self.chatView.setEditable_(False)
        self.chatView.setFont_(NSFont.systemFontOfSize_(12))
        
        # Configure scroll view
        scrollView.setDocumentView_(self.chatView)
        chatHistoryItem.setView_(scrollView)
        
        # Add chat history to menu
        menu.addItem_(chatHistoryItem)

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

        # 10. Initialise LLM
        self.assistant = global_assistant
        self.send_ss = False

        # 11. Add checkbox for ss
        checkboxItem = NSMenuItem.alloc().init()
        self.checkbox = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 22))  # Store reference in self.checkbox
        self.checkbox.setButtonType_(NSButtonTypeSwitch)  # Set the button type to a checkbox
        self.checkbox.setTitle_("Add screen context")
        self.checkbox.setState_(0)  # 0 means unchecked by default
        self.checkbox.setTarget_(self)
        self.checkbox.setAction_("toggleCheckbox:")  # Define action for checkbox toggle

        # Embed the checkbox in the NSMenuItem
        checkboxItem.setView_(self.checkbox)
        # Add the checkbox item to the menu
        menu.addItem_(checkboxItem)
    
    def toggleCheckbox_(self, sender):
        if sender.state():
            self.send_ss = True
        else:
            self.send_ss = False

    def submitText_(self, sender):
        user_input = sender.stringValue()
        # Clear the text field
        sender.setStringValue_("")
        
        # Add user message to chat
        # self.append_to_chat(user_input, "user")
        
        if self.send_ss:
            # TODO:Close the menu
            # problem with below is that it wasn't closing before the ss.
            # self.statusItem.menu().cancelTracking()
            # TODO: Reopen the dropdown menu
            ss_path = self.take_screenshot()
            response = self.assistant.chat(user_input, image_path=ss_path)
            # TODO: Delete ss
        else:
            response = self.assistant.chat(user_input)
        # self.append_to_chat(response, "assistant")
        if self.checkbox:
            self.checkbox.setState_(0)  # Uncheck the checkbox
            self.send_ss = False
        self.append_to_chat()

    def take_screenshot(self, output_path=os.path.join(os.path.dirname(__file__), "temp_ss.png")):
        """
        Takes a screenshot of the entire screen on macOS
        and saves it as a file.
        """
        subprocess.run(["screencapture", output_path])
        return output_path

    def quitApp_(self, sender):
        # Remove the status item before terminating
        NSStatusBar.systemStatusBar().removeStatusItem_(self.statusItem)
        NSApp.terminate_(self)

    def append_to_chat(self):
        """Synchronize displayed chat with global_assistant history"""
        # global_assistant.conversation_history.append({"role": sender, "content": message})
        chat_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in global_assistant.conversation_history])
        self.chatView.setString_(chat_text)
        self.chatView.scrollRangeToVisible_((len(chat_text), 0))

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