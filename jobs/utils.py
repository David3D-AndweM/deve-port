import requests
from django.conf import settings
from django.utils import timezone
from .models import Job

def generate_content(prompt, job_id=None, language='en'):
    """Generate creative content using the Gemini API."""

    # Check if the prompt asks for job details
    if 'available jobs' in prompt.lower():
        if job_id:
            # Focus on the specific job based on the job_id
            job = Job.objects.get(pk=job_id)
            job_description = f"{job.title} at {job.agency} in {job.location} (Posted on {job.created_at:%d %B %Y})"
            prompt = f"Describe this job creatively:\n{job_description}"
        else:
            # Fetch job details (limit to 5 for a concise response)
            jobs = Job.objects.filter(application_date__gte=timezone.now())[:5]  # No random ordering
            job_descriptions = [
                f"{job.title} at {job.agency} in {job.location} (Posted on {job.created_at:%d %B %Y})"
                for job in jobs
            ]
            prompt = f"Describe the following jobs creatively:\n{'\n'.join(job_descriptions)}"

    # Translate the prompt if needed
    translated_prompt = translate_prompt(prompt, language)

    # Prepare the request to Gemini API
    url = settings.GEMINI_API_URL
    headers = {'Content-Type': 'application/json'}
    payload = {
        'prompt': {'text': translated_prompt},
        'temperature': 0.7  # Adjust for more creative responses
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params={'key': settings.GEMINI_API_KEY}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to the AI service. {str(e)}"

    # Extract the AI-generated content
    if response.status_code == 200:
        result = response.json().get('candidates', [{}])[0].get('output', '')
        return result if language == 'en' else translate_response(result, language)
    else:
        return f"Error: {response.json().get('error', 'Unknown error occurred')}"

def translate_prompt(prompt, language):
    """Stub for translating the prompt to the desired language."""
    if language == 'bemba':
        return f"(Bemba) {prompt}"
    elif language == 'nyanja':
        return f"(Nanja) {prompt}"
    return prompt

def translate_response(response, language):
    """Stub for translating the response back to the original language."""