from wxpy import Bot
from utils.messages_list_parser import ChatHolder

if __name__ == '__main__':
    bot = Bot()

    parser = ChatHolder(
        bot, 
        refresh_interval = 0.1,
        mute_group_message = True,
        mute_friend_message = False
    )
    parser.run()