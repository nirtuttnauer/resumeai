import json
import openai
import jinja2
import pdfkit
from dotenv import load_dotenv
import os

model = "gpt-4-turbo"

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def check_chances_of_getting_hired(data, job_description):
    print("Checking the chances of getting hired...")
    prompt = f"""
    Given the following personal data and a job description, determine the chances of getting hired for the job. Consider the match between the skills, experience, and qualifications of the candidate (personal data) with the requirements and responsibilities of the job description.

    Personal Data:
    {json.dumps(data, indent=2)}

    Job Description:
    {job_description}
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Determine the chances of getting hired for the job."},
            {"role": "user", "content": prompt}
        ]
    )
    response_message = response.choices[0].message.content
    return response_message

def check_job_type(job_description):
    print("Checking the job type...")
    prompt = f"""
    Given a job description, determine the type of job (e.g., software engineer, data scientist, product manager, etc.) based on the keywords, requirements, and responsibilities mentioned in the description.

    Job Description:
    {job_description}
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Determine the type of job based on the job description. just answer the job type with dashes instead of spaces."},
            {"role": "user", "content": prompt}
        ]
    )
    response_message = response.choices[0].message.content
    return response_message



def fetch_and_curate_resume(data, job_description):
    print("Curating the resume content...")
    prompt = f"""
    Given the following personal data and a job description, generate a curated resume that highlights the most relevant skills, projects, and experience. Ensure all sections from the personal data are included in the response, including the profile, education, projects, experience, certifications, awards, skills, and languages.

    Personal Data:
    {json.dumps(data, indent=2)}

    Job Description:
    {job_description}

    Structure the response in JSON format as follows:
    {{
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": "",
        "profile": "",
        "education": "",
        "projects": [],
        "experience": [],
        "certifications": [],
        "awards": [],
        "army": "",
        "skills": "",
        "languages": []
    }}
    """
    print (f"prompt: {prompt}")
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Respond with a JSON object containing the curated resume content."},
            {"role": "user", "content": prompt}
        ]
    )
    response_message = response.choices[0].message.content
    print(response_message )
    return response_message


def suggest_improvements(data, job_description):
    print("Suggesting improvements for the resume content...")
    prompt = f"""
    Given the following personal data, provide suggestions to improve the resume content. The suggestions should include recommended changes, additions, or restructuring of the resume content to make it more effective and impactful.

    Personal Data:
    {json.dumps(data, indent=2)}
    
    Job Description:
    {job_description}
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide suggestions to improve the resume content."},
            {"role": "user", "content": prompt}
        ]
    )
    response_message = response.choices[0].message.content
    return response_message

def render_template(template_path, context):
    with open(template_path) as file_:
        template = jinja2.Template(file_.read())
    return template.render(context)

def save_pdf(html_content, output_path, config=None):
    pdfkit.from_string(html_content, output_path, configuration=config)

def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def ShouldUseAI():
    useai = input("Would you like to use the AI to curate the resume content? (yes/no): ")
    if useai.lower() == "yes":
        return True
    else:
        return False
    
def main():
    useai = ShouldUseAI()
    try:
        # Load data from the JSON file
        with open('mydata.json', 'r') as file:
            data = json.load(file)
        
        if not data:
            print("No personal data found. Please fill out the mydata.json file.")
            return
        
        if useai == True:
        
            # Get job description from the user
            job_description = get_multiline_input("Enter the job description (type 'END' on a new line to finish):")
            job_type = check_job_type(job_description)
            print(f"Job Type: {job_type}")
            print(f"Chances of getting hired: {check_chances_of_getting_hired(data, job_description)}")

            # Use ChatGPT to curate the resume content
            curated_resume = fetch_and_curate_resume(data, job_description)
        
            # Attempt to parse the response as JSON
            try:
                curated_resume_data = json.loads(curated_resume)
                print(f"tips: {suggest_improvements(curated_resume_data, job_description)}")
                
            except json.JSONDecodeError:
                print("The response from the AI was not a valid JSON. Ensure the AI is returning JSON format.")
                return

            # Define the template and output paths
            template_path = 'resume_template.html'
            output_path = f"Nir-Tuttnauer-Resume.pdf"
            
            # Render the HTML content with the curated data
            html_content = render_template(template_path, curated_resume_data)
        else:
            # Define the template and output paths
            template_path = 'resume_template.html'
            output_path = 'Nir-Tuttnauer-Resume.pdf'
            
            # Render the HTML content with the curated data
            html_content = render_template(template_path, data)
        # Configure pdfkit with the path to wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        
        # Save the rendered HTML as a PDF
        save_pdf(html_content, output_path, config=config)
        print(f"Resume has been successfully generated and saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()