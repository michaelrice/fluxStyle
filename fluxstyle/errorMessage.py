import gtk,textwrap
def infoMessage(message):
    message = textwrap.wrap(message,50)
    mes = ""
    for lines in message:
        mes += lines+"\n"
    m = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
        gtk.BUTTONS_NONE, mes)
    m.add_button(gtk.STOCK_OK, gtk.RESPONSE_CLOSE)
    response = m.run()
    m.hide()
    if response == gtk.RESPONSE_CLOSE:
        m.destroy()
