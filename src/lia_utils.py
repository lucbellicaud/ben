from __future__ import annotations
from dataclasses import dataclass

from enum import Enum
from functools import total_ordering
from typing import Dict, Iterable, List, Optional, Set, Tuple

"""
Common bridge concepts such as Cardinal Direction, Suit, and Card_ Rank represented as Enums
"""


@total_ordering
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    __from_str_map__ = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
    __to_str__ = {NORTH: "North", SOUTH: "South", EAST: "East", WEST: "West"}

    @classmethod
    def from_str(cls, direction_str: str) -> Direction:
        return Direction(cls.__from_str_map__[direction_str.upper()])

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def next(self) -> Direction:
        return self.offset(1)

    def partner(self) -> Direction:
        return self.offset(2)

    def previous(self) -> Direction:
        return self.offset(3)

    def offset(self, offset: int) -> Direction:
        return Direction((self.value + offset) % 4)

    def teammates(self, other: Direction) -> bool:
        if self == other.partner() or self == other:
            return True
        return False

    def opponents(self, other: Direction) -> bool:
        return not self.teammates(other)

    def abbreviation(self) -> str:
        return self.name[0]

    def to_str(self) -> str:
        return self.__to_str__[self.value]
    
    def to_player_i(self, declarer: Direction) -> int:
        return {
            Direction.NORTH: {Direction.NORTH: 3, Direction.EAST: 0, Direction.SOUTH: 1, Direction.WEST: 2},
            Direction.EAST: {Direction.NORTH: 2, Direction.EAST: 3, Direction.SOUTH: 0, Direction.WEST: 1},
            Direction.SOUTH: {Direction.NORTH: 1, Direction.EAST: 2, Direction.SOUTH: 3, Direction.WEST: 0},
            Direction.WEST: {Direction.NORTH: 0, Direction.EAST: 1, Direction.SOUTH: 2, Direction.WEST: 3},
        }[declarer][self]


@total_ordering
class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    __from_str_map__ = {
        "S": SPADES,
        "H": HEARTS,
        "D": DIAMONDS,
        "C": CLUBS,
        "♠": SPADES,
        "♥": HEARTS,
        "♦": DIAMONDS,
        "♣": CLUBS,
    }

    __to_symbol__ = {SPADES: "♠", HEARTS: "♥", DIAMONDS: "♦", CLUBS: "♣"}

    __to_bbo_symbol__ = {SPADES: "!S", HEARTS: "!H", DIAMONDS: "!D", CLUBS: "!C"}

    __4_colors__ = {SPADES: "blue", HEARTS: "red", DIAMONDS: "orange", CLUBS: "green"}

    @classmethod
    def from_str(cls, suit_str: str) -> Suit:
        return Suit(cls.__from_str_map__[suit_str.upper()])

    def __lt__(self, other: Suit) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.__to_bbo_symbol__[self.value]

    def __str__(self) -> str:
        return self.__to_bbo_symbol__[self.value]

    def abbreviation(self) -> str:
        return self.name[0]

    def symbol(self) -> str:
        return self.__to_symbol__[self.value]

    def shape_index(self) -> int:
        return 3 - self.value

    def color(self) -> str:
        return self.__4_colors__[self.value]

    def get_opposite_suit(self) -> Suit:
        if self == Suit.SPADES:
            return Suit.HEARTS
        if self == Suit.HEARTS:
            return Suit.SPADES
        if self == Suit.DIAMONDS:
            return Suit.CLUBS
        if self == Suit.CLUBS:
            return Suit.DIAMONDS

    def get_corresponding_suit(self) -> Suit:
        if self == Suit.SPADES:
            return Suit.DIAMONDS
        if self == Suit.HEARTS:
            return Suit.CLUBS
        if self == Suit.DIAMONDS:
            return Suit.SPADES
        if self == Suit.CLUBS:
            return Suit.HEARTS

    def is_major(self):
        return True if self.value >= 2 else False

    def is_minor(self):
        return not self.is_major()

    def next(self) -> Suit:
        return Suit((self.value + 1) % 4)

    def get_offset(self, other: Suit) -> int:
        return (other.value - self.value) % 4

    def offset(self, offset: int) -> Suit:
        return Suit((self.value + offset) % 4)

    def to_suit(self):
        return self

    def __getstate__(self):
        # Serialize the Suit enum as its value
        return self.value

    def __setstate__(self, value):
        # Deserialize the Suit enum from its value
        self._value_ = value


@total_ordering
class Rank(Enum):
    TWO = 2, "2", 0, 0,0
    THREE = 3, "3", 0, 0,0
    FOUR = 4, "4", 0, 0,0
    FIVE = 5, "5", 0, 0,0
    SIX = 6, "6", 0, 0,0
    SEVEN = 7, "7", 0, 0,0
    EIGHT = 8, "8", 0, 0,0
    NINE = 9, "9", 0, 0,0
    TEN = 10, "T", 0, 0,0
    JACK = 11, "J", 1, 0,0.9
    QUEEN = 12, "Q", 2, 1,1.95
    KING = 13, "K", 3, 2,3.05
    ACE = 14, "A", 4, 3,4.1

    __from_str_map__ = {
        "2": TWO,
        "3": THREE,
        "4": FOUR,
        "5": FIVE,
        "6": SIX,
        "7": SEVEN,
        "8": EIGHT,
        "9": NINE,
        "10": TEN,
        "T": TEN,
        "J": JACK,
        "Q": QUEEN,
        "K": KING,
        "A": ACE,
    }

    __from_52_int_map__ = {
        12: TWO,
        11: THREE,
        10: FOUR,
        9: FIVE,
        8: SIX,
        7: SEVEN,
        6: EIGHT,
        5: NINE,
        4: TEN,
        3: JACK,
        2: QUEEN,
        1: KING,
        0: ACE,
    }

    __from_28_int_map__ = {
        12: EIGHT,
        11: EIGHT,
        10: EIGHT,
        9: EIGHT,
        8: EIGHT,
        7: EIGHT,
        6: EIGHT,
        5: NINE,
        4: TEN,
        3: JACK,
        2: QUEEN,
        1: KING,
        0: ACE,
    }

    @classmethod
    def from_str(cls, rank_str: str) -> Rank:
        return Rank(cls.__from_str_map__[rank_str.upper()])

    @classmethod
    def from_52_int(cls, value: int) -> Rank:
        return Rank(cls.__from_52_int_map__[value])

    @classmethod
    def from_28_int(cls, value: int) -> Rank:
        return Rank(cls.__from_28_int_map__[value])

    def __lt__(self, other: Rank) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def rank(self) -> int:
        return self.value[0]

    def __str__(self) -> str:
        return self.value[1]

    def abbreviation(self) -> str:
        return self.value[1]

    def hcp(self) -> int:
        return self.value[2]
    
    def slightly_adjusted_hcp(self) -> int:
        return self.value[4]

    def three_two_one_count(self) -> int:
        return self.value[3]

    def __hash__(self) -> int:
        return hash(repr(self))

    def below(self,n=1) -> Rank:
        # return the nth rank below the card. Example : Queen.below(2) = Ten
        return self.offset(-n)

    def above(self, n=1) -> Rank:
        # return the rank just above. Example : Queen.above(2) = ACE
        return self.offset(n)

    def offset(self, offset: int) -> Rank:
        """_summary_

        Args:
            offset (int): Offset to apply to the rank : positive will get a higher rank, negative a lower one

        Returns:
            Rank: The rank offseted
        """
        return [r for r in Rank][[r for r in Rank].index(self) + offset]
    
    @classmethod
    def from_integer(cls, rank_as_int: int) -> Rank:
        return [r for r in reversed(Rank)][rank_as_int]

    def to_integer(self) -> int:
        return [r for r in reversed(Rank)].index(self)


@total_ordering
class BiddingSuit(Enum):
    CLUBS = 0, Suit.CLUBS
    DIAMONDS = 1, Suit.DIAMONDS
    HEARTS = 2, Suit.HEARTS
    SPADES = 3, Suit.SPADES
    NO_TRUMP = 4, None

    __from_str_map__ = {
        "S": SPADES,
        "H": HEARTS,
        "D": DIAMONDS,
        "C": CLUBS,
        "N": NO_TRUMP,
        "NT": NO_TRUMP,
        "♠": SPADES,
        "♥": HEARTS,
        "♦": DIAMONDS,
        "♣": CLUBS,
        "SA": NO_TRUMP,
    }
    __to_symbol__ = {
        SPADES: "♠",
        HEARTS: "♥",
        DIAMONDS: "♦",
        CLUBS: "♣",
        NO_TRUMP: "NT",
    }
    __4_colors__ = {
        SPADES: "blue",
        HEARTS: "red",
        DIAMONDS: "orange",
        CLUBS: "green",
        NO_TRUMP: "black",
    }
    __to_bbo_symbol__ = {SPADES: "!S", HEARTS: "!H", DIAMONDS: "!D", CLUBS: "!C"}

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.__to_bbo_symbol__[self.value]

    def __str__(self) -> str:
        return self.__to_bbo_symbol__[self.value]

    def to_suit(self) -> Suit:
        return self.value[1]

    def abbreviation(self, verbose_no_trump=True) -> str:
        if self.value == BiddingSuit.NO_TRUMP.value and verbose_no_trump:
            return "NT"
        return self.name[0]

    def symbol(self) -> str:
        return self.__to_symbol__[self.value]

    def color(self) -> str:
        return self.__4_colors__[self.value]

    def next(self, ignore_NT=False) -> BiddingSuit:
        if self is BiddingSuit.CLUBS:
            return BiddingSuit.DIAMONDS
        if self is BiddingSuit.DIAMONDS:
            return BiddingSuit.HEARTS
        if self is BiddingSuit.HEARTS:
            return BiddingSuit.SPADES
        if self is BiddingSuit.SPADES:
            return BiddingSuit.CLUBS if ignore_NT else BiddingSuit.NO_TRUMP
        return BiddingSuit.CLUBS

    def previous(self) -> BiddingSuit:
        if self is BiddingSuit.CLUBS:
            return BiddingSuit.NO_TRUMP
        if self is BiddingSuit.DIAMONDS:
            return BiddingSuit.CLUBS
        if self is BiddingSuit.HEARTS:
            return BiddingSuit.DIAMONDS
        if self is BiddingSuit.SPADES:
            return BiddingSuit.HEARTS
        return BiddingSuit.SPADES

    def is_minor(self) -> bool:
        return False if self == BiddingSuit.NO_TRUMP else self.to_suit().is_minor()

    def is_major(self) -> bool:
        return False if self == BiddingSuit.NO_TRUMP else self.to_suit().is_major()

    @classmethod
    def from_str(cls, bidding_suit_str: str) -> BiddingSuit:
        return BiddingSuit(cls.__from_str_map__[bidding_suit_str.upper()])

    @classmethod
    def from_suit(cls, suit: Suit) -> BiddingSuit:
        return BiddingSuit(cls.__from_str_map__[suit.abbreviation()])


MAJORS = [Suit.HEARTS, Suit.SPADES]
MINORS = [Suit.CLUBS, Suit.DIAMONDS]


@total_ordering
class Card_:
    """A single card in a hand or deal of bridge"""

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other) -> bool:
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other) -> bool:
        return self.rank < other.rank

    def __str__(self) -> str:
        return self.rank.abbreviation() + self.suit.abbreviation()

    def to_pbn(self) -> str:
        return self.suit.abbreviation() + self.rank.abbreviation()

    def to_28(
        self, trump: BiddingSuit | Suit, new_suit_rank: Dict[Suit, Dict[Rank, int]]
    ):
        trump = BiddingSuit.from_str(trump.abbreviation())
        for rank, value in new_suit_rank[self.suit].items():
            if rank == self.rank:
                if trump == BiddingSuit.NO_TRUMP:
                    return self.suit.value * 7 + value
                return trump.to_suit().get_offset(self.suit) * 7 + value

    def suit_first_str(self) -> str:
        return self.to_pbn()

    def __repr__(self) -> str:
        return self.rank.abbreviation()

    def __hash__(self) -> int:
        return hash(repr(self))

    def is_equivalent(self, other: Card_, new_suit_rank: Dict[Suit, Dict[Rank, int]]):
        if (
            abs(
                new_suit_rank[self.suit][self.rank]
                - new_suit_rank[other.suit][other.rank]
            )
            == 1
        ):
            return True
        return False

    def trump_comparaison(self, other: Card_, trump: BiddingSuit, lead: Suit) -> bool:
        """Return true if the card is higher than the other card"""
        if self.suit == other.suit:
            return self.rank > other.rank
        if self.suit == trump.to_suit():
            return True
        if other.suit == trump.to_suit():
            return False
        if self.suit == lead:
            return True
        if other.suit == lead:
            return False
        raise Exception("None of the card is a trump or the suit led")

    @classmethod
    def get_from_52(cls, value: int, trump: BiddingSuit):
        if trump == BiddingSuit.NO_TRUMP:
            return Card_(suit=Suit(value // 13), rank=Rank.from_52_int((value) % 13))
        else:
            return Card_(
                suit=(Suit(value // 13)).offset(trump.to_suit().value),
                rank=Rank.from_52_int((value) % 13),
            )

    @classmethod
    def get_from_simplified_52(
        cls, value: int, trump: BiddingSuit, new_suit_rank: Dict[Suit, Dict[Rank, int]]
    ):
        suit = (
            Suit(value // 13)
            if trump == BiddingSuit.NO_TRUMP
            else (Suit(value // 13)).offset(trump.to_suit().value)
        )
        rank_int = value % 13
        for rank, associated_rank_value in new_suit_rank[suit].items():
            if associated_rank_value == rank_int:
                return Card_(suit, rank)
        raise KeyError("The card is not in cards left in the play")

    @classmethod
    def get_from_simplified_28(
        cls, value: int, trump: BiddingSuit, new_suit_rank: Dict[Suit, Dict[Rank, int]]
    ):
        suit = (
            Suit(value // 7)
            if trump == BiddingSuit.NO_TRUMP
            else (Suit(value // 7)).offset(trump.to_suit().value)
        )
        rank_int = value % 7
        for rank, associated_rank_value in new_suit_rank[suit].items():
            if associated_rank_value == rank_int:
                return Card_(suit, rank)
        raise KeyError("The card is not in cards left in the play")

    @classmethod
    def from_str(cls, card_str) -> Card_:
        try:
            return Card_(Suit.from_str(card_str[0]), Rank.from_str(card_str[1]))
        except:
            return Card_(Suit.from_str(card_str[1]), Rank.from_str(card_str[0]))
        
    def to_52(self) -> int:
        return self.suit.value * 13 + self.rank.to_integer()

    def to_32(self) -> int:
        return self.suit.value * 8 + 14-max(self.rank.rank(), 7)


TOTAL_DECK: List[Card_] = []
for rank in Rank:
    for suit in Suit:
        TOTAL_DECK.append(Card_(suit, rank))
LOW_CARD_DECK: List[Card_] = [
    Card_(suit, rank) for suit in Suit for rank in Rank if rank <= Rank.TEN
]


@dataclass
class Trick:
    lead: Direction
    cards: Dict[Direction, Card_]

    def winner(self, trump: BiddingSuit) -> Direction:
        winner = self.lead
        suit_led = self.lead  # Default value, should not append
        try:
            suit_led = self.cards[winner].suit
        except:
            # logging.warning(
            #     "The winner of the last trick didn't play in the following one")
            return winner
        for dir, card in self.cards.items():
            if card.trump_comparaison(self.cards[winner], trump, suit_led):
                winner = dir

        return winner

    @staticmethod
    def from_list(leader: Direction, trick_as_list: List[Card_]):
        trick_as_dict = {}
        for i, card in enumerate(trick_as_list):
            trick_as_dict[leader.offset(i)] = card
        return Trick(leader, trick_as_dict)

    def __str__(self) -> str:
        string = ""
        for dir in Direction:
            if dir in self.cards:
                string += "{0:3}".format(self.cards[dir].__str__())
        return string

    def print_as_pbn(self, first_dir: Direction) -> str:
        string = ""
        for _ in range(len(Direction)):
            if self.cards[first_dir]:
                string += self.cards[first_dir].to_pbn() + " "
            else:
                string += "-  "
            first_dir = first_dir.offset(1)
        return string[:-1]

    def __trick_as_list__(self) -> List[Tuple[Direction, Card_]]:
        trick_as_list: List[Tuple[Direction, Card_]] = []
        dir: Direction = self.lead
        for _ in range(len(self.cards)):
            trick_as_list.append((dir, self.cards[dir]))
            dir = dir.offset(1)
        return trick_as_list

    def __getitem__(self, key):
        return self.__trick_as_list__()[key]

    def __len__(self):
        return len(self.cards)


@dataclass
class Alert:
    text: str
    artificial: bool = False

    def as_dict(self) :
        return {"text" : self.text, "artificial" : self.artificial}

class PlayerHand:
    """Contain one hand"""

    def __init__(self, suits: Dict[Suit, List[Rank]]):
        self.suits: Dict[Suit, List[Rank]] = suits
        self.cards: List[Card_] = []
        self.pair_vul = False
        self.opp_vul = False
        for suit in reversed(Suit):
            for rank in self.suits[suit]:
                self.cards.append(Card_(suit, rank))

    @staticmethod
    def from_string_lists(
        spades: List[str], hearts: List[str], diamonds: List[str], clubs: List[str]
    ) -> PlayerHand:
        """
        Build a PlayerHand out of Lists of Strings which map to Ranks for each suit. e.g. ['A', 'T', '3'] to represent
        a suit holding of Ace, Ten, Three
        :return: PlayerHand representing the holdings provided by the arguments
        """
        suits = {
            Suit.SPADES: sorted(
                [Rank.from_str(card_str) for card_str in spades], reverse=True
            ),
            Suit.HEARTS: sorted(
                [Rank.from_str(card_str) for card_str in hearts], reverse=True
            ),
            Suit.DIAMONDS: sorted(
                [Rank.from_str(card_str) for card_str in diamonds], reverse=True
            ),
            Suit.CLUBS: sorted(
                [Rank.from_str(card_str) for card_str in clubs], reverse=True
            ),
        }
        return PlayerHand(suits)

    @staticmethod
    def from_cards(cards: Iterable[Card_]) -> PlayerHand:
        suits = {
            Suit.CLUBS: sorted(
                [card.rank for card in cards if card.suit == Suit.CLUBS], reverse=True
            ),
            Suit.DIAMONDS: sorted(
                [card.rank for card in cards if card.suit == Suit.DIAMONDS],
                reverse=True,
            ),
            Suit.HEARTS: sorted(
                [card.rank for card in cards if card.suit == Suit.HEARTS], reverse=True
            ),
            Suit.SPADES: sorted(
                [card.rank for card in cards if card.suit == Suit.SPADES], reverse=True
            ),
        }
        return PlayerHand(suits)

    @staticmethod
    def from_pbn(string: str) -> PlayerHand:
        """Create a hand from a string with the following syntax '752.Q864.84.AT62'"""
        tab_of_suit = string.split(".")
        cards = []
        for index, suit in enumerate(tab_of_suit):
            temp = suit.replace("10", "T").replace("X", "T")
            while temp.find("x") != -1:
                for rank in Rank:
                    if rank.abbreviation() in temp:
                        continue
                    temp = temp.replace("x", rank.abbreviation(), 1)
            for rank in temp:
                match index:
                    case 0:
                        cards.append(Card_(Suit.SPADES, Rank.from_str(rank)))
                    case 1:
                        cards.append(Card_(Suit.HEARTS, Rank.from_str(rank)))
                    case 2:
                        cards.append(Card_(Suit.DIAMONDS, Rank.from_str(rank)))
                    case 3:
                        cards.append(Card_(Suit.CLUBS, Rank.from_str(rank)))

        return PlayerHand.from_cards(cards)


class Diag:
    def __init__(self, hands: Dict[Direction, PlayerHand]):
        self.hands = hands
        self.player_cards = {
            direction: self.hands[direction].cards for direction in self.hands}

    def __str__(self) -> str:
        string = ""
        for direction in Direction:
            string += direction.name + " : " + \
                self.hands[direction].__str__() + "\n"
        return string

    @staticmethod
    def init_from_pbn(string: str) -> Diag:
        """ Create a diag from this syntax : 'N:752.Q864.84.AT62 A98.AT9.Q753.J98 KT.KJ73.JT.K7543 QJ643.52.AK962.Q'"""
        dealer = Direction.from_str(string[0])
        string = string[2:]
        hand_list = string.split(" ")
        hands = {}
        for i,hand_str in enumerate(hand_list) :
            hands[dealer.offset(i)] = PlayerHand.from_pbn(hand_str)

        return Diag(hands)

        return Diag(hands)

    def print_as_pbn(self, first_direction=Direction.NORTH) -> str:
        return "{}:{}".format(first_direction.abbreviation(), " ".join([self.hands[dir.offset(first_direction.value)].print_as_pbn() for dir in Direction]))
    
@dataclass
class PlayRecord:
    number_of_tricks: int
    leader: Direction
    record: Optional[List[Trick]]
    shown_out_suits: Dict[Direction, Set[Suit]]
    cards_played_32: List[List[int]]

    @staticmethod
    def from_pbn(string: str) -> Optional[PlayRecord]:
        str_leader = Pbn.get_tag_content(string, "Play")
        str_result = Pbn.get_tag_content(string, "Result")

        if str_result=="":
            return None

        str_declarer = Pbn.get_tag_content(
            string, "Declarer") if str_leader else ""
        if str_declarer=="":
            return None
        trump = BiddingSuit.from_str(
            Pbn.get_tag_content(string, "Contract").replace('X', '')[1:])
        raw_tricks_data = Pbn.get_content_under_tag(string, "Play")
        str_tricks = raw_tricks_data.split('\n') if raw_tricks_data else None
        list_of_str_tricks = [[c for c in trick.split()]
                              for trick in str_tricks] if str_tricks else []

        return PlayRecord.from_tricks_as_list(trump, list_of_tricks=list_of_str_tricks, declarer=Direction.from_str(
            str_declarer))

    @staticmethod
    def from_tricks_as_list(trump: BiddingSuit, list_of_tricks: List[List[str]], declarer: Direction) -> PlayRecord:
        list_of_tricks_as_cards = [
            [Card_.from_str(card) for card in trick] for trick in list_of_tricks]
        tricks: List[Trick] = []
        tricks_count: int = 0
        turn = declarer.offset(1)
        shown_out_suits: Dict[Direction, Set[Suit]] = {
            d: set() for d in Direction}
        cards_played_32: List[List[int]] = [[] for _ in range(4)]
        for trick_as_list in list_of_tricks_as_cards:
            if len(trick_as_list) == 0:
                continue
            current_trick = {}
            for i, card in enumerate(trick_as_list):
                current_trick[turn.offset(i)] = card
                cards_played_32[turn.offset(i).value].append(card.to_32())
            trick = Trick(turn, current_trick)
            if trick.shown_out_suit != {}:
                for dir, suit in trick.shown_out_suit.items():
                    shown_out_suits[dir].add(suit)
            tricks.append(trick)
            if len(trick) != 4:
                # print("Length of trick is not 4")
                continue
            turn = trick.winner(trump)
            tricks_count += 1 if turn in [declarer, declarer.partner()] else 0

        return PlayRecord(number_of_tricks=tricks_count, leader=declarer.offset(1), record=tricks, shown_out_suits=shown_out_suits, cards_played_32=cards_played_32)

    def print_as_pbn(self) -> str:
        string = ""
        string += Pbn.print_tag("Result", str(self.number_of_tricks))
        string += Pbn.print_tag("Play", self.leader.abbreviation())
        if self.record:
            for trick in self.record:
                string += trick.print_as_pbn(self.leader)+"\n"
        return string + "*"

    def as_unordered_one_dimension_list(self) -> List[Card_]:
        return [card for trick in self.record for card in trick.cards.values()] if self.record is not None else []

    def __str__(self) -> str:
        string = "Tricks : " + str(self.number_of_tricks) + "\n"
        if self.record:
            string += '{0:3}{1:3}{2:3}{3:3}\n'.format('N', 'E', 'S', 'W')
            for trick in self.record:
                string += trick.__str__() + "\n"
        return string

    def __len__(self):
        if self.record is None:
            return 0
        else:
            return len(self.record)

    def length_wo_incomplete(self):
        if self.record is None:
            return 0
        else:
            return sum([1 if len(trick) == 4 else 0 for trick in self.record])

    def get_cards_played_by_direction(self, direction: Direction) -> List[Card_]:
        cards: List[Card_] = []
        if self.record is None:
            return []
        for trick in self.record:
            if direction in trick.cards:
                cards.append(trick.cards[direction])
        return cards


class Trick():
    def __init__(self, lead: Direction, cards: Dict[Direction, Card_]) -> None:
        self.lead: Direction = lead
        self.cards: Dict[Direction, Card_] = cards
        self.shown_out_suit: Dict[Direction, Suit] = {
            dir: cards[lead].suit for dir in cards.keys() if self.cards[dir].suit != self.cards[lead].suit}

    @staticmethod
    def from_list(leader: Direction, trick_as_list: List[Card_]) -> Trick:
        trick_as_dict = {}

        for i, card in enumerate(trick_as_list):
            trick_as_dict[leader.offset(i)] = card
        return Trick(lead=leader, cards=trick_as_dict)

    def winner(self, trump: BiddingSuit) -> Direction:
        winner = self.lead
        suit_led = self.lead  # Default value, should not append
        try:
            suit_led = self.cards[winner].suit
        except:
            return winner
        for dir, card in self.cards.items():
            if card.trump_comparaison(self.cards[winner], trump, suit_led):
                winner = dir

        return winner

    def __str__(self) -> str:
        string = ""
        for dir in Direction:
            if dir in self.cards:
                string += '{0:3}'.format(self.cards[dir].__str__())
        return string

    def print_as_pbn(self, first_dir: Direction) -> str:
        string = ""
        for _ in range(4):
            if first_dir in self.cards:
                string += self.cards[first_dir].to_pbn()+" "
            else:
                string += "-  "
            first_dir = first_dir.offset(1)
        return string[:-1]

    def get_as_32_list(self):
        trick_as_list: List[Tuple[Direction, int]] = []
        dir: Direction = self.lead
        for _ in range(len(self.cards)):
            trick_as_list.append((dir, self.cards[dir].to_32()))
            dir = dir.offset(1)
        return trick_as_list

    def __trick_as_tuple_list__(self) -> List[Tuple[Direction, Card_]]:
        trick_as_list: List[Tuple[Direction, Card_]] = []
        dir: Direction = self.lead
        for _ in range(len(self.cards)):
            trick_as_list.append((dir, self.cards[dir]))
            dir = dir.offset(1)
        return trick_as_list

    def __getitem__(self, key):
        return self.__trick_as_tuple_list__()[key]

    def __len__(self):
        return len(self.cards)
