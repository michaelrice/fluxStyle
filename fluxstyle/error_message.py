import gtk
import textwrap

def info_message(message):
    """Creates a GTK MessageDialog and displays a message in it"""
    message = textwrap.wrap(message, 50)
    mes = ""
    for lines in message:
        mes += lines + "\n"
    dialog = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_NONE,
            mes)
    dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_CLOSE)
    response = dialog.run()
    dialog.hide()
    if response == gtk.RESPONSE_CLOSE:
        dialog.destroy()
