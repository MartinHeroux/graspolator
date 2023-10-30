from dataclasses import dataclass

CONDITION_NAMES_EXP1 = [
    "D1 dominant",
    "D1 non-dominant",
    "D2 dominant 1",
    "D2 dominant 2",
]
CONDITION_NAMES_EXP2 = ["Line to width", "Width to line", "Width to width"]
CONDITION_PAIRS = ["between_hands", "between_days", "within_day"]


@dataclass
class ExpCodes:
    exp1: str
    exp2: str


@dataclass
class GeneralConstants:
    condition_names_exp1: list
    condition_names_exp2: list
    condition_pairs: list
    subject_ids: list


EXP_CODES = ExpCodes(exp1="exp2", exp2="exp1")


@dataclass
class ExampleParticipantIDs:
    kathy_participant_1: str = "SUB18R"
    kathy_participant_2: str = "SUB02R"
    kathy_participant_3: str = "SUB03R"
    lovisa_participant_1: str = "sub26"
    lovisa_participant_2: str = "sub23"
    lovisa_participant_3: str = "sub29"
