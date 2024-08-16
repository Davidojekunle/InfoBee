import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from utils.analysis import insights

load_dotenv()

MAX_ATTEMPTS = 16

def create_visuals(file, user_name, error_message=None, attempt=1):
    # Determine file type and read accordingly
    file_extension = os.path.splitext(file)[1].lower()
    if file_extension == '.csv':
        original_data = pd.read_csv(file)
    elif file_extension in ['.xlsx', '.xls']:
        original_data = pd.read_excel(file)
    else:
        return f"Unsupported file format: {file_extension}"

    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create subfolder for user
    file_name = os.path.splitext(os.path.basename(file))[0]
    output_dir = os.path.join('visuals', f"{user_name}_{file_name}")
    os.makedirs(output_dir, exist_ok=True)

    # Get insights
    data_insights = insights(file)

    prompt = f"""Based on the provided data and insights, please generate Python code to restructure the data and create meaningful visualizations that can automatically reveal key insights.

    Original Data columns: {', '.join(original_data.columns)}

    Insights: {data_insights}

    Steps to Follow:


    2. Data Cleaning and Preparation:
       * Handle missing values effectively.
       * Convert data types as necessary (e.g., dates to datetime, strings to numeric).
       * Create derived columns or features that could help in visualizing patterns or trends.

    3. Generate Visualizations to Extract Insights:
       * Create a variety of graphs that automatically highlight important patterns, trends, or anomalies in the data.
       * For each graph, use the following structure:
          * Use plt.figure(figsize=(12, 8)) to define the figure size.
          * Apply plt.tight_layout() before saving to avoid overlapping elements.
          * Save each plot to the folder '{output_dir}' using plt.savefig(os.path.join('{output_dir}', 'plot_name.png'), dpi=300, bbox_inches='tight').
          * Close each figure after saving with plt.close().
       * Ensure the graphs answer the following:
          * What are the main trends or patterns over time?
          * Are there any noticeable outliers or anomalies?
          * How do different categories or groups compare?
          * What are the correlations between key variables?
       * Follow these additional plotting rules:
          * Maximize the data-to-ink ratio by removing non-essential elements.
          * Maintain consistent fonts, colors, and styles across all charts.
          * Avoid 3D effects in charts.
          * Round numbers to an appropriate number of decimal places for clarity.
          * For bar and column charts, always start the y-axis at zero.
          * Use color or other visual cues to highlight important data points.
          * Ensure charts are accessible to color-blind individuals.
          * For scatter plots with many data points, use transparency or jittering to prevent overplotting.
          * Use logarithmic scales when data spans several orders of magnitude.
          * For pie charts:
             - Limit to 2-3 categories, maximum 5-6 if necessary.
             - Group small categories into an "Other" category if needed.
             - Order slices from largest to smallest, starting from 12 o'clock and moving clockwise.
             - Use clear contrasting colors for easy distinction.
             - Label slices directly when possible, instead of using a legend.
             - Consider using a donut chart for a more modern and readable alternative.

    4. Return Only the Python Code:
       * Generate the Python code that follows the above steps, without any additional explanations or comments.

    The file path of the original data is {file}.

    If any errors occur during execution, please include error handling code to address these issues and retry the process.

    Return only the Python code without any explanations or comments."""

    if error_message:
        prompt += f"\n\nAn error occurred when executing the previous code: {error_message}. Please correct the issue and regenerate the code. Ensure that the data restructuring step is handling any problematic columns or data points."

    try:
        response = model.generate_content(prompt)
        plot_instructions = response.text if response.text else "No response generated."
    except Exception as e:
        return f"An error occurred while generating the plot instructions: {str(e)}"

    cleaned_snippet = plot_instructions.replace("python", "").replace("```", "").strip()

    try:
        # Add necessary imports and original data loading
        setup_code = f"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from datetime import datetime

original_data = pd.read_{'csv' if file_extension == '.csv' else 'excel'}("{file}")
output_dir = "{output_dir}"
"""
        exec(setup_code + cleaned_snippet)
        
        # Get all image files in the output directory
        image_files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        image_paths = [os.path.join(output_dir, f) for f in image_files]
        
        if not image_paths:
            raise Exception("No images were generated.")
        
        return image_paths
    except Exception as exec_error:
        if attempt < MAX_ATTEMPTS:
            return create_visuals(file, user_name, error_message=str(exec_error), attempt=attempt + 1)
        else:
            return f"Unable to generate graphs after {MAX_ATTEMPTS} attempts. Last error: {str(exec_error)}"

# Example usage:
# result = create_visuals("uploads/sales_data_sample.csv", "john_doe")
# print(result)