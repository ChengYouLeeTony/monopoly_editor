import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from monopoly.models import Profile, Map, Land, User
from .core.game import *
from .core.building import *
from .core.import_database import *
from .core.event import Event
from monopoly.ws_handlers.game_handler import *
from monopoly.ws_handlers.game_change_handler import *
from monopoly.ws_handlers.modal_title_enum import *
import random
import re

rooms = {}
games = {}
maps_in_use = {}
changehandlers = {}
decisions = {}
money_pass_start_str = {}

class JoinConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("now is connecting for join")
        host_name= self.scope['url_route']['kwargs']['host_name']
        map_id = self.scope['url_route']['kwargs']['map_id']
        """If host create more than one game simultaneously, delete old one"""
        if host_name in maps_in_use:
            if maps_in_use[host_name] != map_id:
                del games[host_name]
                del rooms[host_name]
                del maps_in_use[host_name]
                del money_pass_start_str[host_name]
                if host_name in decisions:
                    del decisions[host_name]

        client_name = str(self.scope["user"])
        print("hostname :", host_name)
        print("client_name :", client_name)
        # Add to the chat group
        self.room_name = host_name
        self.room_group_name = 'group_%s' % self.room_name
        self.player_name = client_name
        if not self.add_player(self.room_name, self.player_name):
            self.send(text_data=self.build_join_failed_msg())
            print("failed to join")
            return
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_join_reply_msg(self.room_name)
            }
        )
        print("join finished")

    def disconnect(self, close_code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        hostname = self.room_name  
        print('action is: ', action)
        print('hostname is: ', hostname)

        if action == "start":
            self.handle_start(hostname)
        if action == "start_game_creator":
            self.handle_start_game_creator(hostname)
        if action == "clear_friends":
            self.handle_clear_friends(hostname)
        if action == "leave_game":
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        if action == "client_leave_game":
            client_name = str(self.scope["user"])
            self.handle_client_leave_game(hostname, client_name)
        if action == "clear_history":
            self.handle_clear_history(hostname)

    def add_player(self, room_name, player_name):
        if room_name not in rooms:
            rooms[room_name] = set()
            rooms[room_name].add(room_name)

        if len(rooms[room_name]) >= 4:
            return False

        rooms[room_name].add(player_name)
        return True

    def remove_players(self, room_name):
        rooms[room_name] = set()
        rooms[room_name].add(room_name)

    def remove_client(self, room_name, client_name):
        rooms[room_name].remove(client_name)

    def build_join_failed_msg(self):
        ret = {"action": "fail_join",
        }
        print(json.dumps(ret))
        return json.dumps(ret)

    def build_join_reply_msg(self, room_name):
        players = rooms[room_name]
        print('players: ', players)
        data = []
        for player in players:
            print('player is: ', player)
            profile_user = User.objects.get(username=player)
            print('profile user: ', profile_user.username)
            try:
                profile = Profile.objects.get(user=profile_user)
            except Exception:
                profile = None
            avatar = profile.avatar.url if profile else ""
            data.append({"id": profile_user.id, "name": player, "avatar": avatar})
            print("data: ", data)

        ret = {"action": "join",
               "data": data,
               'host_name': room_name
               }
        print(json.dumps(ret))
        return json.dumps(ret)

    def reply_message(self, event):
        message = event['text']

        # Send message to WebSocket
        self.send(text_data=message)

    def handle_start(self, hostname):
        # init game
        """import cardset"""
        map_id = self.scope['url_route']['kwargs']['map_id']
        if hostname not in games:
            board, card_decks, player_variables_4_list, constant = import_map_to_board(map_id)
            players = rooms[hostname]
            player_num = len(players)
            game = Game(player_num, card_decks, board, player_variables_4_list, constant)
            games[hostname] = game
            maps_in_use[hostname] = map_id
            money_pass_start_str[hostname] = constant.MONEY_PASS_START

            change_handler = ChangeHandler(game, hostname)
            game.add_game_change_listner(change_handler)
            changehandlers[hostname] = change_handler

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_start_msg()
            }
        )
        print(len(games))
        print("start finish")

    def handle_start_game_creator(self, hostname):
        # init game
        """import cardset"""
        map_id = self.scope['url_route']['kwargs']['map_id']
        if hostname not in games:
            board, card_decks, player_variables_4_list, constant = import_map_to_board(map_id)
            players = rooms[hostname]
            player_num = len(players)
            game = Game(player_num, card_decks, board, player_variables_4_list, constant)
            games[hostname] = game
            maps_in_use[hostname] = map_id
            money_pass_start_str[hostname] = constant.MONEY_PASS_START

            change_handler = ChangeHandler(game, hostname)
            game.add_game_change_listner(change_handler)
            changehandlers[hostname] = change_handler

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_start_creator_msg()
            }
        )
        print(len(games))
        print("start creator finish")

    def handle_clear_friends(self, hostname):
        self.remove_players(hostname)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_clear_friends_msg(hostname)
            }
        )
        print("clear friends finish")

    def handle_client_leave_game(self, hostname, client_name):
        self.remove_client(hostname, client_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_client_leave_game_msg(hostname, client_name)
            }
        )
        print("client leave finish")

    def handle_clear_history(self, host_name):
        if host_name in games:
            del games[host_name]
            del rooms[host_name]
            del maps_in_use[host_name]
            del money_pass_start_str[host_name]
            if host_name in decisions:
                del decisions[host_name]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": self.build_clear_history_msg()
            }
        )
        print("clear history finish")


    def build_start_msg(self):
        ret = {"action": "start"}
        print(json.dumps(ret))
        return json.dumps(ret)

    def build_start_creator_msg(self):
        ret = {"action": "start_creator"}
        print(json.dumps(ret))
        return json.dumps(ret)

    def build_clear_friends_msg(self, room_name):
        players = rooms[room_name]
        data = []
        for player in players:
            profile_user = User.objects.get(username=player)
            try:
                profile = Profile.objects.get(user=profile_user)
            except Exception:
                profile = None
            avatar = profile.avatar.url if profile else ""
            data.append({"id": profile_user.id, "name": player, "avatar": avatar})
            print("data: ", data)

        ret = {"action": "clear_friends",
               "data": data,
               'host_name': room_name
               }
        print(json.dumps(ret))
        return json.dumps(ret)

    def build_client_leave_game_msg(self, room_name, client_name):
        players = rooms[room_name]
        data = []
        for player in players:
            profile_user = User.objects.get(username=player)
            try:
                profile = Profile.objects.get(user=profile_user)
            except Exception:
                profile = None
            avatar = profile.avatar.url if profile else ""
            data.append({"id": profile_user.id, "name": player, "avatar": avatar})
            print("data: ", data)

        ret = {"action": "client_leave_game",
               "data": data,
               'host_name': room_name,
               'client_name': client_name
               }
        print(json.dumps(ret))
        return json.dumps(ret)

    def build_clear_history_msg(self):
        ret = {"action": "clear_history"
               }
        print(json.dumps(ret))
        return json.dumps(ret)

class GameConsumer(WebsocketConsumer):
    def connect(self):
        """init"""
        self.is_land_variable_change_list = []
        self.land_variable_change_list = []
        self.rolled_rule = ""
        self.trigger_event_type = ""
        self.trigger_event_title = ""
        self.trigger_event_subtitle = ""
        self.trigger_event_message = ""
        self.trigger_event_value = ""
        self.event_info = {}
        self.rolled_money_and_variables = {}
        self.sound_info = {}
        """"""
        self.accept()
        print("now is connecting for gaming")
        username = str(self.scope["user"])
        hostname = self.scope['url_route']['kwargs']['host_name']
        is_viewer_allowed = False
        if 'mode' in self.scope['url_route']['kwargs']:
            mode = self.scope['url_route']['kwargs']['mode']
            if mode[:6] == "viewer":
                url_list = mode.split('/')
                user_hash_code = url_list[1]
                host_hash_code = User.objects.get(username = hostname).password.split("$")[-1]
                host_hash_code = re.sub("[^A-Za-z0-9]", "", host_hash_code)
                if user_hash_code == host_hash_code:
                    is_viewer_allowed = True
                
        print("debug003")
        print(self.scope)
        print(self.scope["user"].password.split("$")[-1])
        print(username)
        print(hostname)
       
        self.room_group_name = 'group_%s' % hostname
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if hostname not in games:
            print("debug001")
            self.send(text_data= build_add_err_msg())
            return
        if (hostname not in rooms or username not in rooms[hostname]) and not is_viewer_allowed:
            print("debug002")
            self.send(text_data= build_add_err_msg())
            return

        game = games[hostname]

        players = game.get_players()
        profiles = rooms[hostname]
        print("players:", players)

        cash_change = []
        pos_change = []
        init_direction = []
        player_names = []
        player_varible_1s = []
        player_varible_2s = []
        player_varible_3s = []
        player_varible_4s = []
        player_varible_5s = []
        landname = None
        for player in players:
            cash_change.append(player.get_money())
            pos_change.append(player.get_position())
            init_direction.append(player.get_move_direction())
            player_names.append(player.get_player_name())
            player_varible_1s.append(player.get_variable_1())
            player_varible_2s.append(player.get_variable_2())
            player_varible_3s.append(player.get_variable_3())
            player_varible_4s.append(player.get_variable_4())
            player_varible_5s.append(player.get_variable_5())

        wait_user_define_decision = "false"
        confirm_button_text = ""
        cancel_button_text = ""
        """for chance card decision"""
        wait_multiple_choice_decision = "false"
        multiple_choice_info = {}

        # wait for decision
        if hostname in decisions:
            wait_decision = "true"
            next_player = game.get_current_player().get_index()
            decision = decisions[hostname].beautify(players[next_player])
            landname = decisions[hostname].get_land().get_description()
            

            move_result = decisions[hostname]
            if move_result.move_result_type == MoveResultType.USER_DEFINE:
                title = move_result.get_title()
                wait_decision = "false"
                wait_user_define_decision = "true"
                user_define_option_tuple = move_result.get_user_define_option_tuple()
                confirm_button_text = user_define_option_tuple[0]
                cancel_button_text = user_define_option_tuple[1]
            elif move_result.move_result_type == MoveResultType.CHANCE_CARD:
                title = move_result.get_title()
                landname = move_result.get_subtitle()
                wait_decision = "false"
                wait_multiple_choice_decision = "true"
                multiple_choice_info =  move_result.get_multiple_choice_info()
            else:
                title_type = ModalTitleType()
                title = title_type.get_description(move_result.move_result_type)

            decision_type = move_result.move_result_type
       
        else:
            wait_decision = "false"
            decision = None
            next_player = game.get_current_player().get_index()
            title = None

        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()

        owners = game.get_land_owners()
        houses = []
        for i in range(len(owners)):
            houses.append(get_building_type(i, game))
        NUM_OF_HOUSE_EQUAL_HOTEL = game.get_NUM_OF_HOUSE_EQUAL_HOTEL()
        print("pos_change:", pos_change)
        """This part only do once, and than can be used many times"""
        self.make_is_land_variable_change_list(hostname)
        self.make_rolled_rule(hostname)

        self.send(text_data= build_init_msg(profiles, cash_change, pos_change, init_direction, wait_decision, decision, next_player, title, landname, owners, houses,
            player_names, player_varible_1s, player_varible_2s, player_varible_3s, player_varible_4s, player_varible_5s, 
            wait_user_define_decision, confirm_button_text, cancel_button_text,
            next_player_info, wait_multiple_choice_decision, multiple_choice_info, NUM_OF_HOUSE_EQUAL_HOTEL))
        

    def disconnect(self, close_code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        hostname = self.scope['url_route']['kwargs']['host_name']
        print('action is: ', action)
        print(games)
        print('hostname is: ', hostname)
        print("text_data_json:", text_data_json)
        cheat_list = ["roll_1", "roll_2", "roll_3", "roll_4", "roll_5", "roll_6", "roll_10", "roll_20", "roll_30"]
        if action in cheat_list:
            self.handle_roll(hostname, games, changehandlers, cheat_step=int(action[5:]))
        if action == "roll":
            dice_num = int(text_data_json["dice_num"])
            self.handle_roll(hostname, games, changehandlers, dice_num=dice_num)
        if action == "confirm_decision":
            self.handle_confirm_decision(hostname, games)
        if action == "confirm_user_define_decision":
            self.handle_confirm_user_define_decision(hostname, games)
        if action == "cancel_decision":
            self.handle_cancel_decision(hostname, games)
        if action == "cancel_decision_user_define":
            self.handle_cancel_decision_user_define(hostname, games)
        if action == "wrong_answer":
            self.handle_wrong_answer(hostname, games)
        if action == "chat":
            self.handle_chat(hostname,text_data_json)
        if action == "change_dice_num":
            dice_num = int(text_data_json["dice_num"])
            self.handle_change_dice_num(dice_num)
        if action == "notify_cheat":
            self.handle_notify_cheat()
        if action == "end_game":
            self.handle_end_game(hostname, games)
            del games[hostname]
            del rooms[hostname]
            del maps_in_use[hostname]
            del money_pass_start_str[hostname]

    def make_is_land_variable_change_list(self, hostname):
        """check the land whether the variable will be changed"""
        map_id = maps_in_use[hostname]
        _map = Map.objects.get(id = map_id)
        lands = Land.objects.filter(_map = _map).order_by('pos')
        self.is_land_variable_change_list = []
        self.land_variable_change_list = []
        for land in lands:
            """ex: (True, True, True, False, False)"""
            one_is_land_variable_change_tuple = (land.variable_1_change != "", land.variable_2_change != "", land.variable_3_change != "", 
            land.variable_4_change != "", land.variable_5_change != "")
            """ex: ("X1+1", "x2-1", "x3*2", "", "")"""
            one_land_variable_change_tuple = (land.variable_1_change, land.variable_2_change, land.variable_3_change, 
            land.variable_4_change, land.variable_5_change)
            self.is_land_variable_change_list.append(one_is_land_variable_change_tuple)
            self.land_variable_change_list.append(one_land_variable_change_tuple)
        print(self.land_variable_change_list)

    def make_rolled_rule(self, hostname):
        map_id = maps_in_use[hostname]
        _map = Map.objects.get(id = map_id)
        self.rolled_rule = _map.rolled_rule
        print(self.rolled_rule)

    def reply_message(self, event):
        message = event['text']

        # Send message to WebSocket
        self.send(text_data=message)

    def apply_variable_change_result(self, games, hostname, curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5, move_result):
        game = games[hostname]
        players = game.get_players()
        curr_player = game.get_current_player().get_index()
        new_pos = game.get_current_player().get_position()
        """check whether variable will be changed"""
        is_this_land_variable_change_tuple = self.is_land_variable_change_list[new_pos]
        is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change =  map(lambda x: str(x).lower(), is_this_land_variable_change_tuple)
        this_land_variable_change_tuple = self.land_variable_change_list[new_pos]
        variable_1_change, variable_2_change, variable_3_change, variable_4_change, variable_5_change = map(lambda x: x.lower(), this_land_variable_change_tuple)
        x1 = players[curr_player].get_variable_1()
        x2 = players[curr_player].get_variable_2()
        x3 = players[curr_player].get_variable_3()
        x4 = players[curr_player].get_variable_4()
        x5 = players[curr_player].get_variable_5()
        if is_variable_1_change == "true":
            new_x1 = eval(variable_1_change)
            players[curr_player].set_variable_1(new_x1)
            curr_variable_1.append(new_x1)
        if is_variable_2_change == "true":
            new_x2 = eval(variable_2_change)
            players[curr_player].set_variable_2(new_x2)
            curr_variable_2.append(new_x2)
        if is_variable_3_change == "true":
            new_x3 = eval(variable_3_change)
            players[curr_player].set_variable_3(new_x3)
            curr_variable_3.append(new_x3)
        if is_variable_4_change == "true":
            new_x4 = eval(variable_4_change)
            players[curr_player].set_variable_4(new_x4)
            curr_variable_4.append(new_x4)
        if is_variable_5_change == "true":
            new_x5 = eval(variable_5_change)
            players[curr_player].set_variable_5(new_x5)
            curr_variable_5.append(new_x5)

        """Only for chance card"""
        print(move_result.move_result_type)
        if move_result.move_result_type == MoveResultType.CHANCE_CARD:
            new_variables = players[curr_player].get_variables()
            x1 = new_variables[0]
            x2 = new_variables[1]
            x3 = new_variables[2]
            x4 = new_variables[3]
            x5 = new_variables[4]
            variables_change = move_result.get_variables_change()
            print("variables_change")
            print(variables_change)
            if variables_change[0] != '':
                new_variable_val = eval(variables_change[0])
                players[curr_player].set_variable_1(new_variable_val)
                curr_variable_1.clear()
                curr_variable_1.append(new_variable_val)
                is_variable_1_change = "true"
            if variables_change[1] != '':
                new_variable_val = eval(variables_change[1])
                players[curr_player].set_variable_2(new_variable_val)
                curr_variable_2.clear()
                curr_variable_2.append(new_variable_val)
                is_variable_2_change = "true"
            if variables_change[2] != '':
                new_variable_val = eval(variables_change[2])
                players[curr_player].set_variable_3(new_variable_val)
                curr_variable_3.clear()
                curr_variable_3.append(new_variable_val)
                is_variable_3_change = "true"
            if variables_change[3] != '':
                new_variable_val = eval(variables_change[3])
                players[curr_player].set_variable_4(new_variable_val)
                curr_variable_4.clear()
                curr_variable_4.append(new_variable_val)
                is_variable_4_change = "true"
            if variables_change[4] != '':
                new_variable_val = eval(variables_change[4])
                players[curr_player].set_variable_5(new_variable_val)
                curr_variable_5.clear()
                curr_variable_5.append(new_variable_val)
                is_variable_5_change = "true"
           



        print(is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change)
        return is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change

    def deal_rolled_event(self, general_is_option, new_pos, game, curr_player, START_REWARD):
        """This part is for user define rule rolled result"""
        """init trigger event"""
        self.trigger_event_type = ""
        self.trigger_event_title = ""
        self.trigger_event_subtitle = ""
        self.trigger_event_message = ""
        self.trigger_event_value = ""
        self.event_info = {}
        self.rolled_money_and_variables = {}
        self.sound_info = {}
        is_trigger_move_pass_start = "false"
        is_turn_over = curr_player.get_is_turn_over()
        """if is option, not trigger at first"""
        if not general_is_option:
            x1 = curr_player.get_variable_1()
            x2 = curr_player.get_variable_2()
            x3 = curr_player.get_variable_3()
            x4 = curr_player.get_variable_4()
            x5 = curr_player.get_variable_5()
            money = curr_player.get_money()
            stop_num = curr_player.get_stop_num()
            player_position = curr_player.get_position()

            exec(self.rolled_rule)
            if self.trigger_event_type == "rule_end_game_with_text" or self.trigger_event_type == "rule_end_game":
                Event.end_game_event(game)

            elif self.trigger_event_type == "teleport":
                teleport_pos = int(self.trigger_event_value)
                Event.teleport_event(curr_player, teleport_pos)

            elif self.trigger_event_type == "teleport_random":
                teleport_pos = random.randint(0, 39)
                if teleport_pos == new_pos:
                    teleport_pos += random.randint(1, 39)
                    teleport_pos = teleport_pos % 40
                Event.teleport_event(curr_player, teleport_pos)
                self.trigger_event_value = str(teleport_pos)

            elif self.trigger_event_type == "move_forward":
                move_forward_step = int(self.trigger_event_value)
                if is_turn_over == "false":                  
                    pos_after_move = (new_pos + move_forward_step) % 40
                    is_trigger_move_pass_start = Event.move_clockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)
                elif is_turn_over == "true":
                    pos_after_move = (new_pos - move_forward_step)
                    if pos_after_move < 0:
                        pos_after_move += 40
                    is_trigger_move_pass_start = Event.move_counterclockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)

                """save new position to trigger value"""
                self.trigger_event_value = str(pos_after_move)

            elif self.trigger_event_type == "move_backward":
                move_backward_step = int(self.trigger_event_value)
                if is_turn_over == "false":
                    pos_after_move = (new_pos - move_backward_step)
                    if pos_after_move < 0:
                        pos_after_move += 40
                    is_trigger_move_pass_start = Event.move_counterclockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)
                elif is_turn_over == "true":
                    pos_after_move = (new_pos + move_backward_step) % 40
                    is_trigger_move_pass_start = Event.move_clockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)
                """save new position to trigger value"""
                self.trigger_event_value = str(pos_after_move)

            elif self.trigger_event_type == "move_to":
                if is_turn_over == "false":                  
                    pos_after_move = int(self.trigger_event_value)
                    print("qq")
                    print(pos_after_move)
                    print(new_pos)
                    is_trigger_move_pass_start = Event.move_clockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)
                elif is_turn_over == "true":
                    pos_after_move = int(self.trigger_event_value)
                    is_trigger_move_pass_start = Event.move_counterclockwise_event(pos_after_move, new_pos, curr_player, START_REWARD, is_turn_over)

                """save new position to trigger value"""
                self.trigger_event_value = str(pos_after_move)
            elif self.trigger_event_type == "turn_over":
                Event.turn_over_event(curr_player)
            elif self.trigger_event_type == "swap":
                swap_event_info = Event.swap_event(curr_player, game.get_players())
                self.event_info["swap_event_info"] = swap_event_info
            elif self.trigger_event_type == "swap_all":
                swap_all_event_info = Event.swap_all_event(game.get_players())
                self.event_info["swap_all_event_info"] = swap_all_event_info
            elif self.trigger_event_type == "swap_except_self":
                swap_except_self_event_info = Event.swap_except_self_event(curr_player, game.get_players())
                self.event_info["swap_except_self_event_info"] = swap_except_self_event_info
            elif self.trigger_event_type == "teleport_all_random":
                teleport_all_random_event_info = Event.teleport_all_random_event(game.get_players())
                self.event_info["teleport_all_random_event_info"] = teleport_all_random_event_info
            elif self.trigger_event_type == "teleport_except_self_random":
                teleport_except_self_random_event_info = Event.teleport_except_self_random_event(curr_player, game.get_players())
                self.event_info["teleport_except_self_random_event_info"] = teleport_except_self_random_event_info
            elif self.trigger_event_type == "normal":
                Event.normal_event()

        self.event_info["is_trigger_move_pass_start"] = is_trigger_move_pass_start
        self.event_info["is_turn_over"] = is_turn_over


    def calculate_money_pass_start(self, curr_player, money_pass_start_str):
        x1 = curr_player.get_variable_1()
        x2 = curr_player.get_variable_2()
        x3 = curr_player.get_variable_3()
        x4 = curr_player.get_variable_4()
        x5 = curr_player.get_variable_5()
        # money = curr_player.get_money()
        money_pass_start = int(eval(money_pass_start_str))
        return money_pass_start

    def handle_roll(self, hostname, games, changehandlers, cheat_step=None, dice_num=None):
        game = games[hostname]
        players = game.get_players()
        # player_num = len(players)
        if cheat_step != None:
            steps, move_result = game.roll(steps=cheat_step)
        else:
            steps, move_result = game.roll(dice_num=dice_num)
        curr_player = game.get_current_player().get_index()
        new_pos = game.get_current_player().get_position()
        is_option = "false"
        is_cash_change = "false"
        is_user_define_cash_change = "false"
        is_game_end = "false"
        is_waiting_for_confirm = "false"
        is_new_event = "true"
        is_simple_event = "false"
        is_user_define_event = "false"
        is_chance_card_event = "false"
        is_chance_card_cash_change = "false"
        is_not_show_event = "false"
        curr_cash = []
        next_player = None
        bypass_start = None
        is_user_define_option = "false"
        confirm_button_text = ""
        cancel_button_text = ""
        """chance card part"""
        is_multiple_choice = "false"
        multiple_choice_info = {}
        chance_card_background_img_url = ""
        """variable part"""
        curr_variable_1 = []
        curr_variable_2 = []
        curr_variable_3 = []
        curr_variable_4 = []
        curr_variable_5 = []
        """All situation will be applied variables change at first, except user define option or multiple_choice_option"""
        if not (move_result.get_is_user_define_option() or move_result.get_is_multiple_choice() or move_result.is_option()):
            is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change = self.apply_variable_change_result(games, hostname, curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5, move_result)
        else:
            is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change = ["false"] * 5


        change_handler = changehandlers[hostname]

        if move_result.move_result_type == MoveResultType.CONSTRUCTION_OPTION \
                or move_result.move_result_type == MoveResultType.BUY_LAND_OPTION:
            decisions[hostname] = move_result
            is_option = "true"
        elif move_result.move_result_type == MoveResultType.PAYMENT \
                or move_result.move_result_type == MoveResultType.REWARD:
            game.make_decision(move_result)
            next_player = game.get_current_player().get_index()
            is_cash_change = "true"
            for player in players:
                curr_cash.append(player.get_money())
        elif move_result.move_result_type == MoveResultType.PARK \
            or move_result.move_result_type == MoveResultType.STOP_ROUND \
            or move_result.move_result_type == MoveResultType.IS_NOT_AFFORDABLE:
            game.make_decision(move_result)
            next_player = game.get_current_player().get_index()
            is_simple_event = "true"
        elif move_result.move_result_type == MoveResultType.USER_DEFINE:
            if move_result.get_is_user_define_option():
                decisions[hostname] = move_result
                is_user_define_option = "true"
                user_define_option_tuple = move_result.get_user_define_option_tuple()
                confirm_button_text = user_define_option_tuple[0]
                cancel_button_text = user_define_option_tuple[1]
            else:
                player_money_origin = players[curr_player].get_money()
                game.make_decision(move_result)
                player_money_after_decision = players[curr_player].get_money()
                """if money change, play sound"""
                if player_money_origin != player_money_after_decision:
                    is_user_define_cash_change = "true"
                next_player = game.get_current_player().get_index()
                for player in players:
                    curr_cash.append(player.get_money())
                is_user_define_event = "true"
        elif move_result.move_result_type == MoveResultType.CHANCE_CARD:
            if move_result.get_is_multiple_choice():
                decisions[hostname] = move_result
                is_multiple_choice = "true"
                multiple_choice_info =  move_result.get_multiple_choice_info()
            else:
                player_money_origin = players[curr_player].get_money()
                game.make_decision(move_result)
                player_money_after_decision = players[curr_player].get_money()
                """if money change, play sound"""
                if player_money_origin != player_money_after_decision:
                    is_chance_card_cash_change = "true"

                next_player = game.get_current_player().get_index()
                for player in players:
                    curr_cash.append(player.get_money())
                is_chance_card_event = "true"
            """chance card background img url"""
            chance_card_background_img_url = move_result.get_background_img_url()
        elif move_result.move_result_type == MoveResultType.NOTHING:
            game.make_decision(move_result)
            next_player = game.get_current_player().get_index()
            is_not_show_event = "true"
        else:
            game.make_decision(move_result)
            next_player = game.get_current_player().get_index()

        if is_option != "true" and change_handler.is_end():
            is_game_end = "true"
            print('roll to end')

        """deal rolled rule"""
        """If move result is not optional, deal rolled rule after make decision.
        If move result is optional, only deal rolled rule after confirm"""
        general_is_option = (move_result.get_is_user_define_option() or is_option == "true" or move_result.get_is_multiple_choice())
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(general_is_option, new_pos, game, players[curr_player], money_pass_start)

        next_player_info = {}
        if next_player != None:
            """ 0, "false" """
            next_player_info["pos"] = players[next_player].get_position()
            next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()

        if move_result.move_result_type == MoveResultType.CHANCE_CARD:
            title = move_result.get_title()
            """landname == subtitle"""
            landname = move_result.get_subtitle()
        else:
            if move_result.move_result_type == MoveResultType.USER_DEFINE:
                title = move_result.get_title()
            else:
                title_type = ModalTitleType()
                title = title_type.get_description(move_result.move_result_type)
            landname = move_result.get_land().get_description()

        if change_handler.bypass_start():
            bypass_start = "true"
            change_handler.set_bypass_start()
            curr_cash = []

            for player in players:
                curr_cash.append(player.get_money())
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_roll_res_msg(curr_player, steps, move_result.beautify(players[curr_player]), is_option, is_cash_change,
                                       is_new_event, new_pos, curr_cash, next_player, title, landname, bypass_start, is_game_end,
                                       curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5,
                                       is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change, is_user_define_event,
                                       is_user_define_option, confirm_button_text, cancel_button_text,
                                       self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, is_user_define_cash_change, self.event_info, self.rolled_money_and_variables,
                                       next_player_info, is_simple_event, is_chance_card_event, is_chance_card_cash_change,
                                       is_multiple_choice, multiple_choice_info, self.sound_info, is_not_show_event,
                                       chance_card_background_img_url)
            }
        )

    def handle_confirm_decision(self, hostname, games):
        game = games[hostname]
        curr_player = game.get_current_player().get_index()
        if hostname not in decisions:
            return
        decision = decisions[hostname]
        del decisions[hostname]
        is_game_end = "false"
        """variable part"""
        curr_variable_1 = []
        curr_variable_2 = []
        curr_variable_3 = []
        curr_variable_4 = []
        curr_variable_5 = []
        is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change = self.apply_variable_change_result(games, hostname, curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5, decision)

        decision.set_decision(True)
        confirm_result = game.make_decision(decision)
        players = game.get_players()
        curr_cash = []
        next_player = game.get_current_player().get_index()
        next_player_info = {}

        """for event message"""
        new_pos = players[curr_player].get_position()
        """deal rolled event"""
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(False, new_pos, game, players[curr_player], money_pass_start)
        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()

        for player in players:
            curr_cash.append(player.get_money())

        if confirm_result.move_result_type == MoveResultType.BUY_LAND_OPTION:
            tile_id = confirm_result.get_land().get_position()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": 'reply_message',
                    "text": build_buy_land_msg(curr_player, curr_cash, tile_id, next_player, next_player_info,
                                       new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info,
                                       curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5,
                                       is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change)
                }
            )
        elif confirm_result.move_result_type == MoveResultType.CONSTRUCTION_OPTION:
            tile_id = confirm_result.get_land().get_position()
            build_type = confirm_result.get_land().get_content().get_property()
            if build_type == BuildingType.HOUSE:
                build_type = "house"
            else:
                build_type = "hotel"
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": 'reply_message',
                    "text": build_construct_msg(curr_player, curr_cash, tile_id, build_type, next_player, next_player_info,
                                       new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info,
                                       curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5,
                                       is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change)
                }
            )

    def handle_confirm_user_define_decision(self, hostname, games):
        game = games[hostname]
        curr_player = game.get_current_player().get_index()
        is_game_end = "false"
        if hostname not in decisions:
            return
        decision = decisions[hostname]
        del decisions[hostname]
        """variable part"""
        curr_variable_1 = []
        curr_variable_2 = []
        curr_variable_3 = []
        curr_variable_4 = []
        curr_variable_5 = []
        is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change = self.apply_variable_change_result(games, hostname, curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5, decision)

        players = game.get_players()
        curr_cash = []
        decision.set_decision(True)
        game.make_decision(decision)
        next_player = game.get_current_player().get_index()
        

        """for event message"""
        new_pos = players[curr_player].get_position()
        """deal rolled event"""
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(False, new_pos, game, players[curr_player], money_pass_start)
        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()
        
        for player in players:
            curr_cash.append(player.get_money())
            if player.get_money() < 0:
                 game.notify_game_ended()
                 game._game_state = GameStateType.GAME_ENDED
                 is_game_end = "true"

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_confirm_user_define_decision_msg(next_player, curr_cash, curr_player, next_player_info,
                                       new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info,
                                       curr_variable_1, curr_variable_2, curr_variable_3, curr_variable_4, curr_variable_5,
                                       is_variable_1_change, is_variable_2_change, is_variable_3_change, is_variable_4_change, is_variable_5_change,
                                       is_game_end)
            }
        )

    def handle_cancel_decision(self, hostname, games):
        game = games[hostname]
        curr_player = game.get_current_player().get_index()
        if hostname not in decisions:
            return
        decision = decisions[hostname]
        del decisions[hostname]
        decision.set_decision(False)
        game.make_decision(decision)
        next_player = game.get_current_player().get_index()
        players = game.get_players()

        """for event message"""
        new_pos = players[curr_player].get_position()
        """deal rolled event"""
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(False, new_pos, game, players[curr_player], money_pass_start)
        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()



        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_cancel_decision_msg(curr_player, next_player, next_player_info,
                                        new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                        money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info)
            }
        )

    def handle_cancel_decision_user_define(self, hostname, games):
        game = games[hostname]
        curr_player = game.get_current_player().get_index()
        if hostname not in decisions:
            return
        decision = decisions[hostname]
        del decisions[hostname]
        players = game.get_players()
        curr_cash = []
        decision.set_decision(False)
        game.make_decision(decision)
        next_player = game.get_current_player().get_index()
        
 
        """for event message"""
        new_pos = players[curr_player].get_position()
        """deal rolled event"""
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(False, new_pos, game, players[curr_player], money_pass_start)
        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()
        
        for player in players:
            curr_cash.append(player.get_money())

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_cancel_decision_user_define_msg(next_player, curr_cash, curr_player, next_player_info,
                                       new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info)
            }
        )

    def handle_wrong_answer(self, hostname, games):
        game = games[hostname]
        curr_player = game.get_current_player().get_index()
        is_game_end = "false"
        if hostname not in decisions:
            return
        decision = decisions[hostname]
        del decisions[hostname]
        decision.set_decision(False)
        players = game.get_players()
        curr_cash = []
        game.make_decision(decision)
        next_player = game.get_current_player().get_index()
        players = game.get_players()

        """for event message"""
        new_pos = players[curr_player].get_position()
        """deal rolled event"""
        money_pass_start = self.calculate_money_pass_start(players[curr_player], money_pass_start_str[hostname])
        players[curr_player].set_pass_start_reward(money_pass_start)
        self.deal_rolled_event(False, new_pos, game, players[curr_player], money_pass_start)

        next_player_info = {}
        next_player_info["pos"] = players[next_player].get_position()
        next_player_info["is_turn_over"] = players[next_player].get_is_turn_over()

        for player in players:
            curr_cash.append(player.get_money())
            if player.get_money() < 0:
                 game.notify_game_ended()
                 game._game_state = GameStateType.GAME_ENDED
                 is_game_end = "true"

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_wrong_answer_msg(next_player, curr_cash, curr_player, next_player_info,
                                       new_pos, self.trigger_event_type, self.trigger_event_title, self.trigger_event_subtitle, self.trigger_event_message, self.trigger_event_value,
                                       money_pass_start, self.event_info, self.rolled_money_and_variables, self.sound_info,
                                       is_game_end)
            }
        )

    def handle_chat(self, hostname, msg):
        sender = msg["from"]
        content = msg["content"]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_chat_msg(sender, content)
            }
        )

    def handle_change_dice_num(self, dice_num):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_change_dice_num(dice_num)
            }
        )

    def handle_notify_cheat(self):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_notify_cheat()
            }
        )

    def handle_end_game(self, hostname, games):
        game = games[hostname]
        players = game.get_players()
        map_id = maps_in_use[hostname]
        _map = Map.objects.get(id = map_id)
        score_board_setting = _map.scoreboardsetting
        prior_variable = score_board_setting.prior_variable

        score_board_info = {
            'is_descending_order': score_board_setting.is_descending_order,
            'title': score_board_setting.title,
            'subtitle': score_board_setting.subtitle,
            'background_img_url': score_board_setting.background_img_url,
            'score_board_sound_effect': score_board_setting.score_board_sound_effect,
            'audio_url': score_board_setting.audio_url
        }

        all_scores = []
        curr_player = game.get_current_player().get_index()
        if prior_variable == "asset":
            for player in players:
                all_scores.append(player.get_asset())
        elif prior_variable == "money":
            for player in players:
                all_scores.append(player.get_money())
        elif prior_variable == "pure_asset":
            for player in players:
                all_scores.append(player.get_properties())
        elif prior_variable == "x1":
            for player in players:
                all_scores.append(player.get_variable_1())
        elif prior_variable == "x2":
            for player in players:
                all_scores.append(player.get_variable_2())
        elif prior_variable == "x3":
            for player in players:
                all_scores.append(player.get_variable_3())
        elif prior_variable == "x4":
            for player in players:
                all_scores.append(player.get_variable_4())
        elif prior_variable == "x5":
            for player in players:
                all_scores.append(player.get_variable_5())
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": 'reply_message',
                "text": build_game_end_msg(curr_player, all_scores, score_board_info)
            }
        )
        if hostname in decisions:
            del decisions[hostname]
