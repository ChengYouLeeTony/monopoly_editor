from .event_enum import *
from .game_state_type import GameStateType
import random
import itertools

class Event(object):
    @staticmethod
    def end_game_event(game):
        game.notify_game_ended()
        game._game_state = GameStateType.GAME_ENDED

    @staticmethod
    def teleport_event(curr_player, teleport_pos):
        curr_player.set_position(teleport_pos)

    @staticmethod
    def move_clockwise_event(pos_after_move, origin_pos, curr_player, START_REWARD, is_turn_over):
        is_trigger_move_pass_start= "false"
        """give pass start reward"""
        if is_turn_over == "false":
            if pos_after_move < origin_pos:
                curr_player.add_money(START_REWARD)
                is_trigger_move_pass_start = "true"
        curr_player.set_position(pos_after_move)
        return is_trigger_move_pass_start

    @staticmethod
    def move_counterclockwise_event(pos_after_move, origin_pos, curr_player, START_REWARD, is_turn_over):
        is_trigger_move_pass_start= "false"
        """give pass start reward"""
        if is_turn_over == "true":
            if pos_after_move > origin_pos:
                curr_player.add_money(START_REWARD)
                is_trigger_move_pass_start = "true"
        curr_player.set_position(pos_after_move)
        return is_trigger_move_pass_start

    @staticmethod
    def turn_over_event(curr_player):
        curr_player.flip_is_turn_over()

    @staticmethod
    def swap_event(curr_player, players):
        print("swap event")
        candidate = [ i for i in range(len(players))]
        candidate.pop(curr_player.get_index())
        curr_player_index = curr_player.get_index()
        curr_player_pos = curr_player.get_position()
        curr_player_is_turn_over = curr_player.get_is_turn_over()
        if len(candidate) > 0:
            swap_target = candidate[random.randint(0, len(candidate)-1)]
            target_player_index = players[swap_target].get_index()    
            target_player_pos = players[swap_target].get_position()                     
            target_player_is_turn_over = players[swap_target].get_is_turn_over()
            curr_player.set_position(target_player_pos)
            players[swap_target].set_position(curr_player_pos)
            return [curr_player_index, target_player_index, curr_player_pos, target_player_pos, curr_player_is_turn_over, target_player_is_turn_over]
        else:
            return [curr_player_index, curr_player_index, curr_player_pos, curr_player_pos, curr_player_is_turn_over, curr_player_is_turn_over]

    @staticmethod
    def swap_all_event(players):
        print("swap all event")
        players_index = [ i for i in range(len(players))]
        swap_all_event_info = []
        player_new_pos_list = []
        if len(players_index) > 1:
            possible_swap = list(filter(lambda p: not any(i1==i2 for i1,i2 in zip(players_index, p)), itertools.permutations(players_index, len(players_index))))
            target_swap = random.choice(possible_swap)

            for i in range(len(players_index)):
                player_index = players_index[i]
                player_new_pos = players[target_swap[i]].get_position() 
                player_is_turn_over = players[player_index].get_is_turn_over()
                swap_all_event_info.append([player_index, player_new_pos, player_is_turn_over])
                player_new_pos_list.append(player_new_pos)
                
            for i in range(len(players_index)):
                """set position"""
                players[players_index[i]].set_position(player_new_pos_list[i])

        return swap_all_event_info

    @staticmethod
    def swap_except_self_event(curr_player, players):
        """only for 3-4 players"""
        print("swap except self event")
        players_index = [ i for i in range(len(players))]
        curr_player_index = curr_player.get_index()
        players_index.pop(curr_player_index)
        swap_except_self_event_info = []
        player_new_pos_list = []
        if len(players_index) > 1:
            possible_swap = list(filter(lambda p: not any(i1==i2 for i1,i2 in zip(players_index, p)), itertools.permutations(players_index, len(players_index))))
            target_swap = random.choice(possible_swap)

            for i in range(len(players_index)):
                player_index = players_index[i]
                player_new_pos = players[target_swap[i]].get_position() 
                player_is_turn_over = players[player_index].get_is_turn_over()
                swap_all_event_info.append([player_index, player_new_pos, player_is_turn_over])
                player_new_pos_list.append(player_new_pos)
                
            for i in range(len(players_index)):
                """set position"""
                players[players_index[i]].set_position(player_new_pos_list[i])

        return swap_except_self_event_info

    @staticmethod
    def teleport_all_random_event(players):
        print("teleport all random event")
        players_index = [ i for i in range(len(players))]
        players_pos = [players[players_index[i]].get_position() for i in range(len(players_index))]
        players_is_turn_over = [players[players_index[i]].get_is_turn_over() for i in range(len(players_index))]
        teleport_all_random_event_info = []
        for i in range(len(players_pos)):
            player_new_pos = (players_pos[i] + random.randint(1, 39)) % 40
            teleport_all_random_event_info.append([players_index[i], player_new_pos, players_is_turn_over[i]])
            players[players_index[i]].set_position(player_new_pos)

        return teleport_all_random_event_info

    @staticmethod
    def teleport_except_self_random_event(curr_player, players):
        print("teleport except self random event")
        players_index = [ i for i in range(len(players))]
        curr_player_index = curr_player.get_index()
        players_index.pop(curr_player_index)
        teleport_except_self_random_event_info = []
        if len(players_index) > 0:
            players_pos = [players[players_index[i]].get_position() for i in range(len(players_index))]
            players_is_turn_over = [players[players_index[i]].get_is_turn_over() for i in range(len(players_index))]         
            for i in range(len(players_pos)):
                player_new_pos = (players_pos[i] + random.randint(1, 39)) % 40
                teleport_except_self_random_event_info.append([players_index[i], player_new_pos, players_is_turn_over[i]])
                players[players_index[i]].set_position(player_new_pos)

        return teleport_except_self_random_event_info

    @staticmethod
    def normal_event():
        print("normal event")








