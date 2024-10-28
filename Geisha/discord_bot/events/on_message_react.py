# events/on_message_react.py

import discord
import random
import asyncio

# Define your bank of words and the emoji to react with
BANK_OF_WORDS = {
    "spooky", "witch", "ghost", "haunted", "pumpkin", "monster", "vampire", "zombie", "candy", "cauldron", "skeleton", "ghoul", "cobweb", "mummy", "grim", "reaper", "moonlit", "eerie", "fright", 
    "curse", "phantom", "cackle", "creepy", "bat", "boo", "lantern", "goblin", "bewitched", "scream", "midnight", "Halloween", "werewolf", "tombstone", "spirit", "shadow", "potion", "broomstick", 
    "jack-o-lantern", "darkness", "fang", "spell", "scarecrow", "casket", "crypt", "skull", "fog", "howl", "clown", "mask", "apparition", "horror", "macabre", "nightmare", "voodoo", "spider", 
    "chilling", "moonlight", "sinister", "trick", "treat", "eclipse", "terror", "omen", "gory", "fangs", "dread", "incantation", "undead", "phantasm", "possession", "fear", "hex", "ritual", 
    "specter", "grisly", "wicked", "fearsome", "grave", "creep", "mystery", "fable", "myth", "fairy", "gloom", "witchcraft", "spellbound", "demon", "ghastly", "occult", "evil", 
    "spectral", "shadowy", "mystic", "unholy", "shiver", "unseen", "lurking", "cursed", "blight", "dusk", "dawn", "nocturnal", "shadows", "netherworld", "wraith", "phantasmal", "morbid", 
    "pallor", "necromancer", "bewitch", "pale", "tremor", "wail", "flesh", "soul", "afterlife", "frighten", "twilight", "dark", "ominous", "shade", "unrest", "peril", "fearful", "shudder", 
    "frightful", "cremation", "poltergeist", "creature", "nightfall", "scary", "bizarre", "black", "freaky", "blood", "scare", "moon", "nightshade", "ghoulish", "devilish", "hellish", 
    "crematory", "beast", "nightmarish", "graveyard", "screech", "bloodshot", "paranormal", "murky", "banshee", "cold", "brooding", "witchery", "haunt", 
    "stalk", "shroud", "shriek", "devil", "sinful", "plague", "supernatural", "forsaken", "gallows", "phantomlike", "necrotic", "vile", "hollow", "mournful", "sepulchral", 
    "grimy", "crone", "hexed", "phantasmagoric", "cryptic", "bewitching", "noir", "freak", "mystify", "bone", "tremble", "moonbeam", "hallowed", "scythe", "blasphemy", "lament", 
    "blackcat", "brimstone", "hood", "stalker", "silhouette", "phantasmic", "gloomy", "spectre", "wraithlike", "relic", "umbra", "nightly", "lunar", "underworld", "witchy", 
    "hooded", "gore", "foul", "leech", "creeping", "arcane", "lair", "bloodcurdling", "seance", "darkened", "ritualistic", "foreboding", "mystical", "underground", "cobwebby", 
    "bleak", "eclipsed", "mortal", "fabled", "ethereal", "damned", "hauntings", "spook", "nether", "crepuscular", "forebode", "loom", "dreadful", "faint", "scepter", "sorcery", "beware", 
    "scorn", "scared", "sorceress", "veiled", "phantasmagoria", "deathly", "graven", "asylum", "batty", "cadaver", "catacomb", "chimera", "conjure", "doom", "exorcism", 
    "fiend", "hysteria", "labyrinth", "madness", "psycho", "revenant", "thicket", "void", "bewitchment", "bloodlust", "bone-chilling", "carnage", "coffin", 
    "conjuring", "curse-bound", "deadly", "decay", "desecrate", "disembodied", "eldritch", "ensnare", "entrails", "eternal", "eyeless", "fiendish", "frightening", 
    "ghast", "gore-soaked", "grimace", "haunting", "hollow-eyed", "horrifying", "husk", "infernal", "inferno", "infestation", "jittery", "keening", "lamenting", "lich", "lurker", 
    "lycanthrope", "madman", "marionette", "menacing", "noxious", "petrifying", "putrid", "rotting", "sacrilege", "scourge", "slayer", "stygian", "tainted", 
    "talisman", "torture", "torment", "unearthly", "vexed", "wretched", "writhing", "yowl", "zealot", "beldam", "bloodletting", "brujeria", "changeling", "daemon", "diabolical", "fae", 
    "familiar", "harbinger", "hemlock", "incubus", "mephitic", "miasma", "nefarious", "necropolis", "nighttide", "portent", "sepulcher", "sorcerer", "tenebrous", "threnody", "wyrm", 
    "alchemist", "amalgam", "arcana", "astral", "baneful", "besmirched", "bogeyman", "carnivorous", "conjurer", "crepuscule", "darkling", "doppelgänger", "drear", "ephemeral", 
    "exhumed", "grimoire", "harrow", "hoodoo", "lamentation", "lycan", "maelstrom", "malediction", "memento", "menace", "morass", "nocturne", "plague-ridden", "quagmire", 
    "shadowed", "spellcaster", "succubus", "tormented", "transmutation", "umbrous", "vengeful", "voidwalker", "whisperer", "wraithling", "yokai", "zephyr"
}  # Add words here
EMOJI_LIST = ["🎃", "👻", "🕸️", "🕷️", "💀", "☠️", "👽", "🧛", "🧙", "🧟", "🌕", "🔮", "🎭", "🕯️", "⚰️", "🪦", "⚱️", "🍬", "🍭", "🧹", "🩸", "😱", "🧛‍♂️", "🧛‍♀️", "🧙‍♂️", "🧙‍♀️", "🧟‍♂️", "🧟‍♀️"]  # List of emojis to choose from

async def react_to_message(client, message):
    try:
        """Handles reactions based on words in the BANK_OF_WORDS."""
        if message.author == client.user:
            return  # Ignore messages from the bot itself

        # Check if any word in the message matches a word in the bank
        message_words = set(message.content.lower().split())
        if message_words & BANK_OF_WORDS:  # If there's an intersection, react
            random_emoji = random.choice(EMOJI_LIST)  # Pick a random emoji
            await message.add_reaction(random_emoji)  # React with the chosen emoji
            await asyncio.sleep(1)  # 1-second delay between reactions to prevent rate limiting
    except discord.HTTPException as e:
        print(f"Failed to add reaction: {e}")