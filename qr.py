import pyqrcode

link = pyqrcode.create('https://t.me/interviewme_bot')

link.png('bot.png', scale=10)