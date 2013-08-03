import sublime, sublime_plugin
from subprocess import call
from subprocess import check_output

# js to relaod browsers
scripts = {}

scripts['js'] = 'location.reload()'

scripts['css'] = scripts['styl'] = """
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

# chech if `app` is running.
def running(app):
  out = check_output(['osascript', '-e', """
    tell app "System Events" to count processes whose displayed name is "{app}"
  """.format(app=app)])
  return 0 < int(out)

# tell open browsers to exec `js`
def run(js):
  if running('Google Chrome'): chrome(js)
  if running('Safari'): safari(js)

def safari(js):
  call(['osascript', '-e', """
    tell application "Safari" to do JavaScript "{js}" in document 1
  """.format(js=js)])

def chrome(js):
  call(['osascript', '-e', """
    tell application "Google Chrome"
      execute front window's active tab javascript "{js}"
    end tell
  """.format(js=js)])

class RefreshBrowsers(sublime_plugin.EventListener):

  # "save" event hook
  def on_post_save_async(self, view):
    ext = view.file_name().split('.')[-1]
    if ext in scripts: run(scripts[ext])
