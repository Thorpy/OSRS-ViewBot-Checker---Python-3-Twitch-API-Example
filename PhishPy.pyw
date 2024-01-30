from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

import requests
import sys
from datetime import datetime

class TwitchBot:
    def __init__(self, gui=None):
        self.password = "uernwyix4vsvuuqfwmdmzekntwuv9k"
        self.client_id = "ohkcee30g6utvd9tbjdee4i2kexkj5"
        self.session = requests.Session()
        self.session.headers.update({'Client-ID': self.client_id, 'Authorization': f'Bearer {self.password}'})
        self.gui = gui

    def find_phishers(self):
        response = self.session.get('https://api.twitch.tv/helix/streams?first=5&game_id=459931')
        streams = response.json()['data']
        stream_info = []
        for stream in streams:
            user_id = stream['user_id']
            user_resp = self.session.get(f'https://api.twitch.tv/helix/users?id={user_id}')
            user_data = user_resp.json()['data'][0]
            follower_resp = self.session.get(f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}')
            followers_data = follower_resp.json()
            total_followers = followers_data.get('total', 0)  # The total field contains the total number of followers
            created_at = datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            account_age = (datetime.now() - created_at).days
            stream_info.append((stream['user_name'], stream['viewer_count'], total_followers, account_age))
            if total_followers < 100 or account_age < 3000:
                self.gui.add_phisher(stream['user_name'])  # Add the phisher to the GUI
        return stream_info

class TwitchBotGUI(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.phishers = set()
        self.initUI()

    def update_streams(self):
        streams = self.bot.find_phishers()  # Get the top 5 streams
        for i, stream in enumerate(streams):
            text = f"<b>Streamer</b>: {stream[0]}<br><b>Viewers</b>: {stream[1]}<br><b>Followers</b>: {stream[2]}<br><b>Account Age</b>: {stream[3]} days"
            if stream[0] in self.phishers:
                text = f"<font color='red'>{text}</font>"
            self.labels[i].setText(text)
        self.timer_label.setText(f"<b>Last updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.phisher_label.setText(f"<b>Identified Phishers:</b> {', '.join(self.phishers)}")

    def add_phisher(self, name):
        self.phishers.add(name)

    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_streams)
        self.timer.start(60000)  # Update the streams every minute

        self.labels = [QLabel(self) for _ in range(5)]  # Create a label for each stream
        self.timer_label = QLabel(self)
        self.phisher_label = QLabel(self)

        vbox = QVBoxLayout()
        for label in self.labels:
            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            label.setFont(QFont('Arial', 10))
            vbox.addWidget(label)

        self.timer_label.setFont(QFont('Arial', 10))
        vbox.addWidget(self.timer_label)

        self.phisher_label.setFont(QFont('Arial', 10))
        vbox.addWidget(self.phisher_label)

        btn = QPushButton('Update Now', self)
        btn.clicked.connect(self.update_streams)
        vbox.addWidget(btn)

        self.setLayout(vbox)
        self.setWindowTitle('Twitch Bot')
        self.show()

        QTimer.singleShot(0, self.update_streams)  # Populate the GUI after it has been shown

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot = TwitchBot()  # Create the bot with no GUI initially
    gui = TwitchBotGUI(bot)  # Create the GUI
    bot.gui = gui  # Update the bot with the GUI
    sys.exit(app.exec_())
