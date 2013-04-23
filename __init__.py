import sublime, sublime_plugin
from subprocess import call
from subprocess import check_output

# js to replace styles

js = """
  var links = document.getElementsByTagName('link');
  var len = links.length;
  var cloned = null;
  for (var i = 0; i < len; ++i) {
    if (style(links[i])) {
      clone = links[i].cloneNode(true)
      links[i].parentNode.appendChild(clone)
      links[i].parentNode.removeChild(links[i])
    }
  }

  function style(el){
    return 0 == el.getAttribute('rel').indexOf('style');
  }
"""
 
class RefreshBrowsers(sublime_plugin.EventListener):

  # refresh
  def on_post_save_async(self, view):
    if self.running('Google Chrome'):
      self.chrome()
    if self.running('Safari'):
      self.safari()

  # chech if `app` is running.
  def running(self, app):
    out = check_output(['osascript', '-e', """
      tell app "System Events" to count processes whose displayed name is "{app}"
    """.format(app=app)])
    return 0 < int(out)

  # chrome
  def chrome(self):
    call(['osascript', '-e', """
      tell application "Google Chrome"
        execute front window's active tab javascript "{js}"
      end tell
    """.format(js=js)])

  # safari
  def safari(self):
    call(['osascript', '-e', """
      tell application "Safari" to do JavaScript "{js}" in document 1
    """.format(js=js)])

    
