import re

# Harmful word filtering function
def filter_harmful_word(word):
    harmful_words_set = {
        # Profanity
    "damn", "hell", "crap", "ass", "bastard", "bitch", "douche", "fuck", "shit", "dick",
    "bollocks", "bugger", "bloody", "wanker", "arse", "piss", "turd", "twat", "cunt", "prick",
    
    # Hate Speech (Racial/Ethnic/Gender Slurs)
    "chink", "nigger", "spic", "kike", "faggot", "dyke", "tranny", "wetback", "honky", "gook",
    "paki", "beaner", "camel jockey", "raghead", "gypsy", "half-breed", "mulatto", "redskin", "sambo", "wop",
    
    # Sexually Explicit Terms
    "blowjob", "anal", "porn", "pussy", "dildo", "cum", "tits", "whore", "slut", "horny",
    "gangbang", "handjob", "fingering", "deepthroat", "rimjob", "nude", "erotic", "orgasm", "penetration", "strip",
    
    # Violence-Related Terms
    "kill", "murder", "rape", "bomb", "stab", "assault", "shoot", "slaughter",
    "execute", "decapitate", "massacre", "terrorism", "torture", "lynch", "assassin", "genocide", "hang", "mutilate",
    
    # Discriminatory Terms (Religious/Sexist/Other Discriminatory)
    "islamist", "terrorist", "retard", "cripple", "coon", "ape", "savage", "uncle tom", "heathen",
    "zionist", "bigot", "chauvinist", "feminazi", "homophobe", "misogynist", "supremacist", "sexist", "white trash", "xenophobe"

    }
    normalized_word = re.sub(r'[^a-zA-Z]', '', word.lower())
    return "harmful" if normalized_word in harmful_words_set else "not harmful"