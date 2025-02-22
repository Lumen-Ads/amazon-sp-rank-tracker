import pandas as pd
from PyQt5 import QtWidgets
from datetime import datetime

def read_excel(file_path):
    """Read data from an Excel file and return it as a DataFrame."""
    try:
        df = pd.read_excel(file_path)
        if 'ASINs' not in df.columns or 'Keywords' not in df.columns:
            raise ValueError("Excel file must contain 'ASINs' and 'Keywords' columns")
        return df
    except Exception as e:
        raise Exception(f"Error reading Excel file: {e}")

def write_excel(data, file_path):
    """Write data to an Excel file."""
    try:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error writing to Excel file: {e}")

def save_to_excel(data, output_path):
    """
    Save scraping results to Excel file
    Args:
        data: List of dictionaries containing the results
        output_path: Path where the file should be saved
    """
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    return output_path

def show_message(title, message):
    """Show a message box with the given title and message."""
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()