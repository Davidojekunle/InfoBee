import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

def get_plot_instructions(file, error_message=None, attempt=1):

    data = pd.read_csv(file).to_string()

    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""{data}
Based on the provided CSV data, please generate instructions to a python code that will help visualize the data effectively.
you should go straight to the python code only because I will be executing the code directly from your response so avoid using for comments or whatsoever.
The output should be a python code snippet that plots different graphs using pandas and matplotlib.
Additionally, make sure to save each generated plot to a folder named 'visuals' using plt.savefig(os.path.join('visuals', 'sample_plot.png')).
The file path of the CSV data is {file}.
"""

    if error_message:
        prompt += f"\n\nAn error occurred when executing the previous code: {error_message}. Please correct the issue and regenerate the code."

    try:
        response = model.generate_content(prompt)
        plot_instructions = response.text if response.text else "No response generated."
    except Exception as e:
        return f"An error occurred while generating the plot instructions: {str(e)}"
    
    cleaned_snippet = plot_instructions.replace("python", "").replace("```", "").strip()

    try:
        exec(cleaned_snippet)
        output_dir = 'visuals'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, 'generated_plot.png'))
        plt.show()
        return "Plot saved successfully."

    except Exception as exec_error:
        if attempt < 3:
            return get_plot_instructions(file, error_message=str(exec_error), attempt=attempt + 1)
        else:
            return f"An error occurred during execution on attempt {attempt}: {str(exec_error)}"

# Run the function to generate, execute, and save the plot
# print(get_plot_instructions("uploads/sales_data_sample.csv"))
