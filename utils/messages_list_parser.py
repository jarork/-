import wxpy
from wxpy import embed
from time import time
from threading import Thread

from utils.session_manager import FriendSession, SessionDict, GroupSession
from utils.TUI import TUI

class ChatHolder():
    def __init__(self, bot, refresh_interval:int=1, mute_group_message=False, mute_friend_message=False) -> None:
        self.bot = bot
        self.me = bot.self
        self.friends = bot.friends()
        self.refresh_interval = refresh_interval
        self.sessions = SessionDict()
        self.mute_group = mute_group_message
        self.mute_friend = mute_friend_message
        self.tui = TUI(self)

    def run(self):
        session_refreshing_thread = Thread(target=self.standalone)
        session_refreshing_thread.start()
        self.tui.run()

    def standalone(self):
        prev_time = time()
        while True:
            cur_time = time()
            if cur_time - prev_time > self.refresh_interval:
                messages = self.bot.messages
                session_dict = self.refresh_sessions_list(messages)
                prev_time = time()
            else:
                pass

    def refresh_sessions_list(self, messages):
        """
            将Messages转换为Session格式
        : messages -> wx.messages : 当前消息队列
        : return -> dict : 会话列表 {wx.chat : list(message)}
        """
        # 如果消息队列中有信息，做消息解析生成session
        while len(messages):
            new_msg = messages.pop()
            self.insert_msg_to_sessions(new_msg)
        
    def insert_msg_to_sessions(self, message):
        """
            将一条信息插入到整理后的全部会话之内
        : message -> wx.message : 一条消息
        : return -> None :
        """
        sender, receiver = message.sender, message.receiver
        # 群聊信息
        is_group_chat = isinstance(sender, wxpy.api.chats.group.Group) or isinstance(receiver, wxpy.api.chats.group.Group)
        is_friend_chat = isinstance(sender, wxpy.api.chats.friend.Friend)
        if is_group_chat:
            group = receiver if sender == self.me else sender
            if group not in self.sessions.groups:
                self.sessions.groups[group] = GroupSession()
            self.sessions.groups[group].append(message)
            if not self.mute_group:
                print(message)
        elif is_friend_chat: 
            friend = receiver if sender == self.me else sender
            if friend not in self.sessions.friends:
                self.sessions.friends[friend] = FriendSession()
            self.sessions.friends[friend].append(message)
            if not self.mute_friend:
                print(message)
