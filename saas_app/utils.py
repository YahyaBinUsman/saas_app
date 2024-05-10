# saas_app/utils.py

from datetime import datetime
import requests

def calculate_words_left_per_day(user_subscription):
    """
    Calculate the number of words left per day based on the user's subscription.
    """
    max_words_per_day = user_subscription.plan.max_words_per_day
    words_generated_today = user_subscription.words_generated_today
    today = datetime.now().date()
    
    # Reset words generated today if subscription date is not today
    if user_subscription.subscription_date != today:
        user_subscription.words_generated_today = 0
        user_subscription.save()
        words_generated_today = 0
    
    words_left_today = max_words_per_day - words_generated_today
    
    return max(0, words_left_today)  # Ensure words left per day is non-negative

# saas_app/utils.py

import openai

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_blog(description, title, total_words, words_per_day):
    # Calculate days required to write the blog based on total words and words per day
    days_required = total_words // words_per_day + (1 if total_words % words_per_day else 0)

    # Generate prompt for the blog content
    prompt = f"Title: {title}\nDescription: {description}\nGenerate a blog post with {total_words} words in {days_required} days."

    # Call OpenAI API to generate blog content
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the engine according to your preference
        prompt=prompt,
        max_tokens=total_words,
        stop="\n",  # Stop generation at the end of the blog
        temperature=0.7,  # Adjust temperature for creativity level
        n=1,  # Generate a single response
        timeout=10,  # Timeout in seconds
    )

    # Extract generated content from the API response
    generated_content = response.choices[0].text.strip()

    return generated_content
