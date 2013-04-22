import sublime, sublime_plugin
from subprocess import call
 
class RefreshBrowsers(sublime_plugin.EventListener):

  # refresh
  def on_post_save_async(self, view):
    self.chrome()
    self.safari()

  # chrome
  def chrome(self):
    call(['osascript', '-e', """
        tell application "chrome"
            set winref to a reference to (first window whose title does not start with "Developer Tools -")    
            set winref's index to 1
            reload active tab of winref
        end tell 
    """])

  # safari
  def safari(self):
    call(['osascript', '-e', """
        tell application "safari"
            tell its first document
                set its URL to (get its URL)
            end tell
        end tell
    """])
