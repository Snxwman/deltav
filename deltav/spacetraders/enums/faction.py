from enum import Enum, auto

from deltav.spacetraders.enums import serialize_by_name


@serialize_by_name
class FactionSymbol(Enum):
    """
    AEGIS
    ANCIENTS
    ASTRO
    COBALT
    CORSAIRS
    COSMIC
    CULT
    DOMINION
    ECHO
    ETHEREAL
    GALACTIC
    LORDS
    OMEGA
    QUANTUM
    SHADOW
    SOLITARY
    UNITED
    VOID

    Properties:
    default
    """

    AEGIS = 'AEGIS'
    ANCIENTS = 'ANCIENTS'
    ASTRO = 'ASTRO'
    COBALT = 'COBALT'
    CORSAIRS = 'CORSAIRS'
    COSMIC = 'COSMIC'
    CULT = 'CULT'
    DOMINION = 'DOMINION'
    ECHO = 'ECHO'
    ETHEREAL = 'ETHEREAL'
    GALACTIC = 'GALACTIC'
    LORDS = 'LORDS'
    OBSIDIAN = 'OBSIDIAN'
    OMEGA = 'OMEGA'
    QUANTUM = 'QUANTUM'
    SHADOW = 'SHADOW'
    SOLITARY = 'SOLITARY'
    UNITED = 'UNITED'
    VOID = 'VOID'

    # @property
    # def default(self) -> 'FactionSymbol':
    #     return FactionSymbol.COSMIC


@serialize_by_name
class FactionTraitSymbol(Enum):
    """
    ADAPTABLE
    AGGRESSIVE
    BOLD
    BRUTAL
    BUREAUCRATIC
    CAPITALISTIC
    CLAN
    COLLABORATIVE
    COMMERCIAL
    COOPERATIVE
    CURIOUS
    DARING
    DEFENSIVE
    DEXTEROUS
    DISTRUSTFUL
    DIVERSE
    DOMINANT
    DOMINION
    ENTREPRENEURIAL
    ESTABLISHED
    EXILES
    EXPLORATORY
    FLEETING
    FLEXIBLE
    FORSAKEN
    FRAGMENTED
    FREE_MARKETS
    FRINGE
    GUILD
    IMPERIALISTIC
    INDEPENDENT
    INDUSTRIOUS
    INESCAPABLE
    INNOVATIVE
    INTELLIGENT
    ISOLATED
    LOCALIZED
    MILITARISTIC
    NOTABLE
    PEACEFUL
    PIRATES
    PROGRESSIVE
    PROUD
    RAIDERS
    REBELLIOUS
    RESEARCH_FOCUSED
    RESOURCEFUL
    SCAVENGERS
    SECRETIVE
    SELF_INTERESTED
    SELF_SUFFICIENT
    SMUGGLERS
    STRATEGIC
    TECHNOLOGICALLY_ADVANCED
    TREASURE_HUNTERS
    UNITED
    UNPREDICTABLE
    VISIONARY
    WELCOMING
    """

    ADAPTABLE = auto()
    AGGRESSIVE = auto()
    BOLD = auto()
    BRUTAL = auto()
    BUREAUCRATIC = auto()
    CAPITALISTIC = auto()
    CLAN = auto()
    COLLABORATIVE = auto()
    COMMERCIAL = auto()
    COOPERATIVE = auto()
    CURIOUS = auto()
    DARING = auto()
    DEFENSIVE = auto()
    DEXTEROUS = auto()
    DISTRUSTFUL = auto()
    DIVERSE = auto()
    DOMINANT = auto()
    DOMINION = auto()
    ENTREPRENEURIAL = auto()
    ESTABLISHED = auto()
    EXILES = auto()
    EXPLORATORY = auto()
    FLEETING = auto()
    FLEXIBLE = auto()
    FORSAKEN = auto()
    FRAGMENTED = auto()
    FREE_MARKETS = auto()
    FRINGE = auto()
    GUILD = auto()
    IMPERIALISTIC = auto()
    INDEPENDENT = auto()
    INDUSTRIOUS = auto()
    INESCAPABLE = auto()
    INNOVATIVE = auto()
    INTELLIGENT = auto()
    ISOLATED = auto()
    LOCALIZED = auto()
    MILITARISTIC = auto()
    NOTABLE = auto()
    PEACEFUL = auto()
    PIRATES = auto()
    PROGRESSIVE = auto()
    PROUD = auto()
    RAIDERS = auto()
    REBELLIOUS = auto()
    RESEARCH_FOCUSED = auto()
    RESOURCEFUL = auto()
    SCAVENGERS = auto()
    SECRETIVE = auto()
    SELF_INTERESTED = auto()
    SELF_SUFFICIENT = auto()
    SMUGGLERS = auto()
    STRATEGIC = auto()
    TECHNOLOGICALLY_ADVANCED = auto()
    TREASURE_HUNTERS = auto()
    UNITED = auto()
    UNPREDICTABLE = auto()
    VISIONARY = auto()
    WELCOMING = auto()
