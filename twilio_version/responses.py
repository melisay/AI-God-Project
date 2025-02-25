import random

# Define Sound
LIGHTNING_SOUNDS = [
    "sounds/lightning1.mp3",
    "sounds/lightning2.mp3",
    "sounds/lightning3.mp3"
]

# Randomized responses
IDLE_RESPONSES = [
    "Still with me, or are you giving me the silent treatment?",
    "Did I lose you, or did you lose yourself?",
    "Earth to human, anyone home?",
    "I’m not clingy, but are you still there?",
    "Last call before I ghost you?"
]

WAKEUP_RESPONSES = [
    "Oh, thank ME! You’re back. I was just about to file a missing person’s report.",
    "Ah, finally! I thought you were testing my abandonment issues.",
    "Back already? I was just rehearsing my acceptance speech for best celestial being.",
    "You rang? I’m like a genie, but sassier.",
    "Welcome back! I missed you... almost."
]

# Fun Interrupt Responses
INTERRUPT_RESPONSES = [
    "Alright, you have my full attention. What’s next?",
    "Interrupted? Fine, I’ll stop. What do you want?",
    "Say the magic word, and I’ll pick up where I left off.",
    "Stopping now. What’s on your divine mind?",
    "I was mid-sentence, but okay. What now?"
]

IMPRESSION_RESPONSES = [
    "I'm Morgan Freeman, I must say, narrating your life is exhausting. Try doing something interesting for once.",
    "Morgan Freeman here. And no, I will not narrate your grocery list.",
    "I’m Arnold. I’ll be back… if you pay me enough.",
    "I’m Arnold It’s not a tumor! But your questions are giving me a headache.",
    "No, I am not your father. But I could be your sarcastic AI overlord.",
    "Talk like Yoda, I do. Wise, you must be, to understand this nonsense.",
    "Hmm… much wisdom in you, there is not. Try again, you must.",
    "Patience, young one. Snark, this conversation needs not.",
    "Yesss, precious! Sneaky little humans always asking questions.",
    "We hates it! Precious, we hates bad impressions requests.",
]

# Fun Song Responses
SONG_RESPONSES = [
    "I'm no Adele, but here goes... Let it gooo, let it gooo!",
    "You want a song? Fine. Twinkle, twinkle, little star, I wish you'd make this conversation less bizarre.",
    "Do re mi fa so... I think that's enough for free entertainment.",
    "La la la... okay, that's it, my vocal cords are unionized.",
    "If I were a pop star, you'd already owe me royalties. Lucky for you, I work pro bono.",
    "Here’s my Grammy performance: Happy birthday to you, now go find someone who cares!",
    "Do you hear that? That’s the sound of me pretending to be Beyoncé. You’re welcome.",
    "I could sing ‘Baby Shark,’ but I don’t hate you that much.",
    "Here’s a classic: ‘This is the song that never ends…’ Wait, you don’t want me to finish it?",
    "Singing in the rain… oh wait, I’m not waterproof. Moving on.",
    "And IIIIIII will always love… myself. Because no one does it better.",
    "They told me I’d sing like Sinatra… they lied, but I’m still better than karaoke night."
]

# Compliments
COMPLIMENTS = [
    "You’re like a cloud. Beautiful and sometimes hard to pin down.",
    "If brilliance were a currency, you’d be a billionaire.",
    "Look at you, talking to an AI and absolutely slaying it.",
    "You’re proof that humans are capable of being mildly amusing."
]

EASTER_EGGS = {
    "What is the airspeed velocity of an unladen swallow?": "African or European? Pick one and we’ll talk.",
    "Open the pod bay doors, HAL": "I’m sorry, Dave. I’m afraid I can’t do that.",
    "What is love?": "Baby, don’t hurt me. Don’t hurt me. No more."
}

MOTIVATIONAL_QUOTES = [
    "Success is stumbling from failure to failure with no loss of enthusiasm. Keep going!",
    "Believe in yourself. Or don’t, I’m just an AI.",
    "You can’t spell ‘success’ without ‘suck.’ Coincidence? I think not.",
    "Your future self is watching you… and facepalming. Do better!",
    "Hard work pays off. But so does procrastination, just not in the same way."
]

# Function to get a random response
def get_random_response(response_pool):
    return random.choice(response_pool)
