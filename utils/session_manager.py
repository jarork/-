"""
    会话管理
"""

from wxpy.api.messages.messages import Messages


class Session(Messages):
    pass

class GroupSession(Session):
    pass

class FriendSession(Session):
    def __str__(self):
        if len(self):
            string = ''
            for msg in self:
                string += f'{msg.sender.nick_name} {msg.create_time}: {msg.text}\n'
            return string
        else:        
            return '暂无聊天记录...'


class AllSessions(dict):
    pass

class AllGroupSessions(AllSessions):
    def __str__(self):
        latest_msgs = [[i,j[-1]] for i,j in self.items()]
        latest_msgs = sorted(latest_msgs, key=lambda x:x[1].create_time, reverse=True)
        latest_groups = [i[0] for i in latest_msgs]

        if len(self):
            string = ''
            
            for group in latest_groups:
                group_messages = self[group]

                string += f'【{group.nick_name}】\n'
                for msg in group_messages[-5:]:
                    string += f'\t{msg.create_time} {msg.member.nick_name} : {msg.text}\n'

            return string
        else:
            return "当前暂无群聊会话..."

class AllFriendSessions(AllSessions):
    def __str__(self):
        latest_msgs = [[i,j[-1]] for i,j in self.items()]
        latest_msgs = sorted(latest_msgs, key=lambda x:x[1].create_time, reverse=True)
        latest_friend = [i[0] for i in latest_msgs]

        if len(self):
            string = ''
            
            for friend in latest_friend:
                friend_messages = self[friend]

                string += f'【{friend.nick_name}】\n'
                for msg in friend_messages[-5:]:
                    string += f'\t{msg.create_time} {msg.sender.nick_name} -> {msg.receiver.nick_name} : {msg.text}\n'

            return string
        else:
            return "当前暂无好友会话..."

class SessionDict():
    def __init__(self, group_chats_data=None, friend_chats_data=None) -> None:
        if group_chats_data:
            self.groups = group_chats_data
        else:
            self.groups = AllGroupSessions()
        
        if friend_chats_data:
            self.friends = friend_chats_data
        else:
            self.friends = AllFriendSessions()
