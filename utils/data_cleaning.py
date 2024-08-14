import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import os
import re

load_dotenv()

def clean_generated_code(code, file_path):
    # Remove markdown code blocks if present
    code = re.sub(r'```python\n|```\n?', '', code)
    
    # Split the code into lines
    lines = code.split('\n')
    
    # Prepare the cleaned code
    cleaned_lines = [
        "import pandas as pd",
        "",
        f"# Read the data file",
        f"df = pd.read_csv('{file_path}') if '{file_path}'.endswith('.csv') else pd.read_excel('{file_path}')",
        "",
        "# Ensure df is a copy to avoid SettingWithCopyWarning",
        "df = df.copy()",
        "",
        "# Remove duplicates",
        "df.drop_duplicates(inplace=True)",
        "",
        "# Handle missing values and clean data"
    ]
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('import') and not line.startswith('df ='):
            # Add a check for column existence for each operation
            if '=' in line and '[' in line and ']' in line:
                column = line.split('[')[1].split(']')[0].strip("'")
                cleaned_lines.append(f"if '{column}' in df.columns:")
                cleaned_lines.append(f"    {line}")
            elif 'subset=' in line:
                columns = re.findall(r"'([^']*)'", line)
                column_check = " and ".join([f"'{col}' in df.columns" for col in columns])
                cleaned_lines.append(f"if {column_check}:")
                cleaned_lines.append(f"    {line}")
            else:
                cleaned_lines.append(line)
    
    # Add code to save the cleaned dataframe
    cleaned_lines.extend([
        "",
        "# Save the cleaned dataframe",
        f"output_path = '{file_path.rsplit('.', 1)[0]}_cleaned.{file_path.rsplit('.', 1)[1]}'",
        "df.to_csv(output_path, index=False) if output_path.endswith('.csv') else df.to_excel(output_path, index=False)",
        "print(f'Cleaned data saved to {{output_path}}')"
    ])
    
    return "\n".join(cleaned_lines)
def generate_and_execute_cleaning_code(file_path, max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        try:
            # Read the file
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                return "Error: Unsupported file format. Please use CSV or Excel files."

            # Convert dataframe to string
            data_string = df.to_string()

            # Configure Gemini API
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                return "Error: GEMINI_API_KEY not found in environment variables."
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')

            # Prompt for Gemini API
            prompt = f"""
            Given the following dataset (first few rows):
            {data_string}
            Please provide Python code to clean this dataset. The code should:
            1. Remove all duplicate rows
            2. Handle null values appropriately (e.g., drop rows with null values or fill them with appropriate values)
            3. Perform any other necessary cleaning operations you deem fit
            Return only the Python code, without any explanations. The code should use pandas and assume the dataset is stored in a variable called 'df'.
            Ensure the code is syntactically correct and can be executed directly.
            Do not include any print statements or comments in the code.
            """

            if attempt > 0:
                prompt += f"\n\nThe previous attempt resulted in the following error: {error_message}\nPlease correct the code to avoid this error."

            # Generate cleaning code
            response = model.generate_content(prompt)
            generated_code = response.text.strip()

            # Clean and improve the generated code
            cleaned_code = clean_generated_code(generated_code, file_path)
            print(f"Attempt {attempt + 1} - Generated code:\n\n{cleaned_code}")
            
            # Execute the cleaned code
            exec(cleaned_code, globals())
            
            return f"Cleaned data saved successfully to {file_path.rsplit('.', 1)[0]}_cleaned.{file_path.rsplit('.', 1)[1]}"
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt + 1} failed with error: {error_message}")
            attempt += 1
    
    return f"Failed to clean data after {max_attempts} attempts. Last error: {error_message}"

# Example usage
if __name__ == "__main__":
    file_path = "uploads/sales_data_sample.csv"  # or "path/to/your/file.xlsx"
    result = generate_and_execute_cleaning_code(file_path)
    print(result)