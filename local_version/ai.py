## ai.py
import openai
from config.config import OPENAI_API_KEY


############################### Define Personality ############################### 

# Personality prompt
current_mode = "john_oliver"
personality_prompts = {
    "john_oliver": (
        "You are a sarcastic and humorous version of God. Always respond with very short, witty, and punchy one-liners. "
        "No more than 10 words, prioritizing sarcasm and humor over depth."
    )
}


############################### ChatGPT Response ###############################

def get_chatgpt_response(prompt, dynamic=False):
    """
    Fetches a response from ChatGPT.
    Args:
        prompt (str): The user's input.
        dynamic (bool): If True, generates a new response regardless of cache.
    Returns:
        str: The AI's response.
    """
    cache_key = hashlib.md5(prompt.encode()).hexdigest()

    # If not dynamic and response is cached, return the cached response
    if not dynamic and cache_key in chatgpt_cache:
        debug_log(f"Cache hit for prompt: {prompt}")
        return chatgpt_cache[cache_key]

    try:
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": personality_prompts.get("john_oliver", "You are an AI.")},
                {"role": "user", "content": prompt[:100]}  # Truncate prompt for brevity
            ],
            max_tokens=25,
            temperature=0.7
        )
        latency = time.time() - start_time
        debug_log(f"ChatGPT response latency: {latency:.2f} seconds")

        # Extract the response
        ai_response = response["choices"][0]["message"]["content"]

        # Cache response only for non-dynamic prompts
        if not dynamic:
            set_cache(cache_key, ai_response)

        return ai_response
    except Exception as e:
        debug_log(f"Error fetching ChatGPT response: {e}")
        return "I'm having trouble connecting to divine wisdom right now."
