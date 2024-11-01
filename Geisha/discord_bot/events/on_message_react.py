# events/on_message_react.py

import discord
import random
import asyncio
import logging
# Set up logging for debugging
logger = logging.getLogger(__name__)

# Define your bank of words and the emoji to react with
BANK_OF_WORDS = {
   "halloween", "afterlife", "alchemist", "amalgam", "apparition", "arcana", "arcane", "astral", 
   "asylum", "baneful", "banshee", "bat", "batty", "beast", "beldam", "besmirched", "beware", "bewitch", 
   "bewitched", "bewitching", "bewitchment", "bizarre", "black", "blackcat", "blasphemy", "bleak", "blight", 
   "blood", "bloodcurdling", "bloodletting", "bloodlust", "bloodshot", "bogeyman", "bone", "bone-chilling", 
   "boo", "brimstone", "brooding", "broomstick", "brujeria", "cackle", "cadaver", "candy", "carnage", 
   "carnivorous", "casket", "catacomb", "cauldron", "changeling", "chilling", "chimera", "clown", "cobweb", 
   "cobwebby", "coffin", "cold", "conjure", "conjurer", "conjuring", "creature", "creep", "creeping", "creepy", 
   "cremation", "crematory", "crepuscular", "crepuscule", "crone", "crypt", "cryptic", "curse", "curse-bound", 
   "cursed", "daemon", "damned", "dark", "darkened", "darkling", "darkness", "dawn", "dead", "deadly", "deathly", 
   "decay", "demon", "desecrate", "devil", "devilish", "diabolical", "disembodied", "doom", "doppelgänger", 
   "dread", "dreadful", "drear", "dusk", "eclipse", "eclipsed", "eerie", "eldritch", "ensnare", "entrails", 
   "ephemeral", "eternal", "ethereal", "evil", "exhumed", "exorcism", "eyeless", "fable", "fabled", "fae", 
   "faint", "fairy", "familiar", "fang", "fangs", "fear", "fearful", "fearsome", "fiend", "fiendish", 
   "flesh", "fog", "forebode", "foreboding", "forsaken", "foul", "freak", "freaky", "fright", "frighten", 
   "frightening", "frightful", "gallows", "ghast", "ghastly", "ghost", "ghoul", "ghoulish", "gloom", "gloomy", 
   "goblin", "gore", "gore-soaked", "gory", "grave", "graven", "graveyard", "grim", "grimace", "grimoire", 
   "grimy", "grisly", "hallowed", "harbinger", "harrow", "haunt", "haunted", "haunting", "hauntings", "hellish", 
   "hemlock", "hex", "hexed", "hollow", "hollow-eyed", "hood", "hooded", "hoodoo", "horrifying", "horror", 
   "howl", "husk", "hysteria", "incantation", "incubus", "infernal", "inferno", "infestation", "jack-o-lantern", 
   "jittery", "keening", "labyrinth", "lair", "lament", "lamentation", "lamenting", "lantern", "leech", "lich", 
   "loom", "lunar", "lurker", "lurking", "lycan", "lycanthrope", "macabre", "madman", "madness", "maelstrom", 
   "malediction", "marionette", "mask", "memento", "menace", "menacing", "mephitic", "miasma", "midnight", 
   "monster", "moon", "moonbeam", "moonlight", "moonlit", "morass", "morbid", "mortal", "mournful", "mummy", 
   "murky", "mystery", "mystic", "mystical", "mystify", "myth", "necromancer", "necropolis", "necrotic", 
   "nefarious", "nether", "netherworld", "nightfall", "nightly", "nightmare", "nightmarish", "nightshade", 
   "nighttide", "nocturnal", "nocturne", "noir", "noxious", "occult", "omen", "ominous", "pale", "pallor", 
   "paranormal", "peril", "petrifying", "phantasm", "phantasmagoria", "phantasmagoric", "phantasmal", 
   "phantasmic", "phantom", "phantomlike", "plague", "plague-ridden", "poltergeist", "portent", "possession", 
   "potion", "psycho", "pumpkin", "putrid", "quagmire", "reaper", "relic", "revenant", "ritual", "ritualistic", 
   "rotting", "sacrilege", "scare", "scarecrow", "scared", "scary", "scepter", "scorn", "scourge", "scream", 
   "screech", "scythe", "seance", "sepulcher", "sepulchral", "shade", "shadow", "shadowed", "shadows", "shadowy", 
   "shiver", "shriek", "shroud", "shudder", "silhouette", "sinful", "sinister", "skeleton", "skull", "slayer", 
   "sorcerer", "sorceress", "sorcery", "soul", "specter", "spectral", "spectre", "spell", "spellbound", 
   "spellcaster", "spider", "spirit", "spook", "spooky", "stalk", "stalker", "stygian", "succubus", "supernatural", 
   "tainted", "talisman", "tenebrous", "terror", "thicket", "threnody", "tombstone", "torment", "tormented", 
   "torture", "transmutation", "treat", "tremble", "tremor", "trick", "twilight", "umbra", "umbrous", "undead", 
   "underground", "underworld", "unearthly", "unholy", "unrest", "unseen", "vampire", "veiled", "vengeful", "vexed", 
   "vile", "void", "voidwalker", "voodoo", "wail", "werewolf", "whisperer", "wicked", "witch", "witchcraft", 
   "witchery", "witchy", "wraith", "wraithlike", "wraithling", "wretched", "writhing", "wyrm", "yokai", "yowl", 
   "zealot", "zephyr", "zombie" 
}  # Add words here
EMOJI_LIST = ["🎃", "👻", "🕸️", "🕷️", "💀", "⚰️", "🪦", "🍬"]  # List of emojis to choose from

async def react_to_message(client, message):
    try:
        if message.author == client.user:
            return

        # Convert message content to lowercase words
        message_words = set(word.lower() for word in message.content.split())
        
        # Check if message contains any Halloween-related words
        if message_words.intersection(BANK_OF_WORDS):
            # Ensure no reaction duplicates
            if not any(reaction.me for reaction in message.reactions):
                random_emoji = random.choice(EMOJI_LIST)
                await message.add_reaction(random_emoji)
                await asyncio.sleep(1)  # Rate limit prevention
    except discord.HTTPException as e:
        logger.error(f"Failed to add reaction: {e}")