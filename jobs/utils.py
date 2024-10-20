# utils.py

import requests
from django.conf import settings
from .models import Job  # Assuming Job model is available

def generate_content(prompt, language='en'):
    """Generate creative responses using the Gemini API."""
    # Check if the user is asking about available jobs
    if 'available jobs' in prompt.lower():
        job_details = fetch_jobs()  # Get job data from the database
        prompt = f"Describe the following jobs in an exciting way:\n{job_details}"

    translated_prompt = translate_prompt(prompt, language)

    url = settings.GEMINI_API_URL
    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': translated_prompt}]}]}

    response = requests.post(
        url, headers=headers, json=data, params={'key': settings.GEMINI_API_KEY}
    )

    if response.status_code == 200:
        result = response.json().get('contents', [{}])[0].get('parts', [{}])[0].get('text')
        return result if language == 'en' else translate_response(result, language)
    else:
        return "Sorry, something went wrong. Please try again."

def fetch_jobs():
    """Fetch job titles and brief details from the database."""
    jobs = Job.objects.all()[:5]  # Limit to 5 jobs for concise responses
    job_descriptions = [
        f"{job.title} at {job.agency} in {job.location} (Posted on {job.created_at:%d %B %Y})"
        for job in jobs
    ]
    return '\n'.join(job_descriptions)

def translate_prompt(prompt, language):
    """Translate prompt to the selected language (stub)."""
    if language == 'bemba':
        return f"(Bemba) {prompt}"
    elif language == 'nyanja':
        return f"(Nyanja) {prompt}"
    return prompt

def translate_response(response, language):
    """Translate response back to the selected language (stub)."""
    if language != 'en':
        return f"(Translated to {language}): {response}"
    return response
