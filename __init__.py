import sublime, sublime_plugin
from subprocess import call
from subprocess import check_output

# js to relaod browsers
scripts = {}

scripts['md'] =\
scripts['html'] =\
scripts['jade'] =\
scripts['json'] =\
scripts['js'] = 'location.reload()'

scripts['css'] =\
scripts['styl'] = """
  [].slice.call(document.getElementsByTagName('link')).forEach(function(el){
    var rel = el.getAttribute('rel')
    if (rel && 0 == rel.indexOf('style')) {
      el.parentNode.replaceChild(el.cloneNode(true), el)
    }
  })
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
      repeat with theWindow in every window
        repeat with theTab in every tab of theWindow
          if theTab's URL starts with "http://localhost" or theTab's URL starts with "file:" then
            execute theTab javascript "{js}"
          end if
        end repeat
      end repeat
    end tell
  """.format(js=js)])

class RefreshBrowsers(sublime_plugin.EventListener):

  # "save" event hook
  def on_post_save_async(self, view):
    ext = view.file_name().split('.')[-1]
    if ext in scripts: run(scripts[ext])
