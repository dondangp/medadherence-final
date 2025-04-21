import openai
import time
import re
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPEN_AI_KEY')

def load_api_key():
    api_key = os.getenv('OPEN_AI_KEY')
    if not api_key:
        print("Warning: OpenAI API key not found in environment variables")
        return None
    return api_key

# Function to detect drug interactions using OpenAI API
def detect_drug_interactions(medications, api_key):
    if not api_key:
        return "Please set up your OpenAI API key to use this feature."
    
    if not medications:
        return "No active medications found to analyze."
    
    # Set the API key
    openai.api_key = api_key
    
    # Prepare the list of medications
    med_names = [med["Medication"] for med in medications]
    med_list = ", ".join(med_names)
    
    # Prepare the prompt
    prompt = f"""
Analyze the following medications for potential drug interactions:
{med_list}

Please provide:
1. A list of any potential drug interactions between these medications
2. Severity of each interaction (Mild, Moderate, Severe)
3. Description of the potential effects
4. Recommendations for the me (the patient) on what to do if an interaction is found

If no interactions are found, clearly state "No drug interactions found."
"""
    
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a pharmacological expert assistant providing medication analysis and drug interaction information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        # Extract the response text
        result = response.choices[0].message.content.strip()
        
        # Check if no interactions were found
        if "no drug interactions found" in result.lower():
            return "✅ No drug interactions found between your current medications."
        
        return result
    
    except Exception as e:
        return f"Error analyzing drug interactions: {str(e)}"

# Function to generate medication insights using OpenAI API
def generate_medication_insights(medications, api_key):
    if not api_key:
        return "Please set up your OpenAI API key to use this feature."
    
    if not medications:
        return "No active medications found to analyze."
    
    # Set the API key
    openai.api_key = api_key
    
    # Prepare the data
    insights_data = {}
    
    for med in medications:
        try:
            # Prepare the prompt for each medication
            prompt = f"""
Provide concise insights about the medication '{med["Medication"]}' with the following information:
1. Primary purpose/uses
2. Common side effects
3. How to take it properly
4. What to avoid while taking it
5. When to consult a doctor

Keep each point brief (1-2 sentences) and focused on essential information a patient would need.
"""
            
            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medication expert assistant providing clear, factual information about medications in a concise format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            # Extract the response text
            result = response.choices[0].message.content.strip()
            
            # Add to our insights dictionary
            insights_data[med["Medication"]] = result
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            insights_data[med["Medication"]] = f"Error retrieving insights: {str(e)}"
    
    return insights_data

# Function to format insights for display
def format_insights(insights_dict):
    if isinstance(insights_dict, str):
        return insights_dict  # Return error message if it's a string
    
    formatted_text = ""
    
    for med_name, insight in insights_dict.items():
        formatted_text += f"### {med_name}\n\n"
        
        # Try to extract and format the numbered points
        pattern = r"\d\.\s+(.*?)(?=\n\d\.|\Z)"
        matches = re.findall(pattern, insight, re.DOTALL)
        
        if matches:
            for i, match in enumerate(matches):
                titles = ["Purpose", "Side Effects", "How to Take", "What to Avoid", "When to Consult Doctor"]
                if i < len(titles):
                    formatted_text += f"**{titles[i]}**: {match.strip()}\n\n"
                else:
                    formatted_text += f"{match.strip()}\n\n"
        else:
            # If pattern extraction fails, just use the raw text
            formatted_text += f"{insight}\n\n"
        
        formatted_text += "---\n\n"
    
    return formatted_text