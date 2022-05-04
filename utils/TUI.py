class TUI():
    def __init__(self, chat_holder) -> None:
        self.holder = chat_holder
        pass

    def run(self):
        while True:
            opt = input('1. 查看最新好友会话\n2. 查看最新群聊会话\n3. 和好友聊天\n4. 加入群聊天 \nQ. 退出登录\n')
            if opt == '1':
                self.show_active_friend_chats()

            elif opt == '2':
                self.show_active_group_chats()

            elif opt == '3':
                self.chat_with_friend()

            elif opt == 'Q':
                self.holder.bot.logout()
                exit()

            # 清屏
            self.print_empty_line(15)
    

    def show_active_friend_chats(self):
        print(self.holder.sessions.friends)
        exit = input('')
        return True

    def show_active_group_chats(self):
        print(self.holder.sessions.groups)
        exit = input('')
        return True

    def chat_with_friend(self):
        friend_search_name = input('请输入好友名称：')
        possible_friends = self.holder.friends.search(friend_search_name)[:10]
        if not len(possible_friends):
            print('没有查找到好友。')
            return False

        # 打印好友列表
        print('为您查找到以下好友：')
        for i, friend in enumerate(possible_friends):
            print(f'【{i}】 {friend.nick_name}\n')
        
        while True:
            try:
                choice = int(input(f'该找谁聊天呢？【输入代号】'))
                friend = possible_friends[choice]
                break
            except:
                print('代号不对，请输入有效的代号...')

        assert self.enter_friend_chatroom(friend), f'【警告】您与好友{friend.nick_name}的聊天出现了异常。'
        print(f'您与好友{friend.nick_name}的聊天已结束。')

        return True

    def enter_friend_chatroom(self, friend):
        print(f'已为您转接好友{friend.nick_name}，输入任意信息发送，退出请随时输入"(Q)"...\n')
        self.print_friend_chat_history(friend)

        while True:
            message_text = input('')
            if message_text == '(Q)':
                break
            else:
                friend.send(message_text)
        
        return True

    def print_friend_chat_history(self, friend):
        if friend in self.holder.sessions.friends:
            print(self.holder.sessions.friends[friend])
        else:
            pass
        return None

    ###################### 工具函数 #########################

    @staticmethod
    def print_empty_line(num:int):
        print('\n'*num)