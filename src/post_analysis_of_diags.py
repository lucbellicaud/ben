

from copy import deepcopy
import random
from typing import Dict, List

import numpy as np
from lia_utils import Diag, PlayerHand, Direction, Suit, Card_, Rank,TOTAL_DECK,PlayRecord

def convert_and_post_analysis_of_diags(hand_str : str, dummy_hand_str : str,player_direction : Direction, declarer : Direction,play_record : PlayRecord,players_states : List[np.ndarray],trick_i : int,probalities_list : List[np.ndarray]) :
    # Convert the data
    convert_diags(hand_str, dummy_hand_str,player_direction, declarer,play_record,players_states,trick_i)
    # Post analysis of the data
    post_analysis_of_diags()

def convert_diags(hand_str : str, dummy_hand_str : str,player_direction : Direction, declarer : Direction,play_record : PlayRecord,players_states : List[np.ndarray],trick_i : int) :
    player_hand = PlayerHand.from_pbn(hand_str)
    dummy_hand = PlayerHand.from_pbn(dummy_hand_str)
    current_trick_as_dict = (
            play_record.record[-1].cards
            if play_record.record and len(play_record.record[-1]) != 4
            else {}
        )
    hidden_cards = [
            card
            for card in deepcopy(TOTAL_DECK)
            if card
            not in dummy_hand.cards
            + player_hand.cards
            + play_record.as_unordered_one_dimension_list()
        ]
    def create_diag_from_32(
            base_diag: Diag, array_of_array_32: List[np.ndarray], pips: List[Card_]
        ):
            diag = deepcopy(base_diag)
            pips_as_dict = {
                s: [card.rank for card in pips if card.suit == s] for s in Suit
            }
            for dir in not_visible_hands_directions:
                diag.hands[dir] = create_hand_from_32(
                    array_of_array_32[dir.to_player_i(declarer)].reshape((4, 8)),
                    pips_as_dict,
                    dir,
                )
            return diag

    def create_hand_from_32(
        array_of_8_suits: np.ndarray, pips: Dict[Suit, List[Rank]], dir: Direction
    ):
        return PlayerHand(
            {
                suit: create_suit_from_8(array_8, pips[suit], suit, dir)
                for array_8, suit in zip(array_of_8_suits, Suit)
            }
        )

    def create_suit_from_8(array_8, pip: List[Rank], suit: Suit, dir: Direction):
        current_trick_card = (
            None
            if dir not in current_trick_as_dict
            else current_trick_as_dict[dir]
        )
        random.shuffle(pip)
        high_ranks = [
            Rank.from_integer(int(i))
            for i in np.nonzero(array_8[:-1])[0]
            if current_trick_card is None
            or Card_(suit, Rank.from_integer(int(i))) != current_trick_card
        ]
        try:
            low_ranks = [
                pip.pop()
                for _ in range(
                    int(array_8[-1])
                    - (
                        1
                        if current_trick_card is not None
                        and current_trick_card.rank <= Rank.SEVEN
                        and current_trick_card.suit == suit
                        else 0
                    )
                )
            ]
        except:
            raise Exception("Pop from empty ?")
        return high_ranks + low_ranks

    def get_base_diag() -> Diag:
        base_diag = Diag(
            {dir: PlayerHand({s: [] for s in Suit}) for dir in Direction},
        )
        if declarer.offset(2) == player_direction:
            base_diag.hands[player_direction] = dummy_hand
            base_diag.hands[declarer] = player_hand
        else:
            base_diag.hands[player_direction] = player_hand
            base_diag.hands[declarer.offset(2)] = dummy_hand

        return base_diag

    base_diag = get_base_diag()
    not_visible_hands_directions = [
            dir
            for dir in Direction
            if dir
            not in [
                player_direction,
                declarer.offset(2)
                if player_direction != declarer.offset(2)
                else declarer,
            ]
        ]
    
    low_hidden_cards = [c for c in hidden_cards if c.rank <= Rank.SEVEN]
    n_samples = players_states[0].shape[0]
    samples_as_diag = [
        create_diag_from_32(
            base_diag,
            [players_states[j][i, trick_i, :32] for j in range(4)],
            low_hidden_cards,
        )
        for i in range(n_samples)
    ]
    return samples_as_diag

def post_analysis_of_diags() :
    pass