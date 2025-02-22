from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
try:
    import pandas as pd
    import openpyxl
except ImportError as e:
    raise ImportError(f"Required package missing: {e}. Please run 'pip install pandas openpyxl'")
from src.scraper.amazon_scraper import AmazonScraper

class ScraperWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.scraper = AmazonScraper()

    def run(self):
        try:
            def progress_callback(current, total):
                self.progress.emit(int(current), int(total))
            
            results = self.scraper.process_data(self.data, progress_callback)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Amazon Sponsored Product Rank Tracker")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.uploaded_data = None
        self.worker = None

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.title_label = QtWidgets.QLabel("Amazon Sponsored Product Rank Tracker", self)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.file_label = QtWidgets.QLabel("No file selected", self)
        self.layout.addWidget(self.file_label)

        self.upload_button = QtWidgets.QPushButton("Upload Excel File", self)
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.start_button = QtWidgets.QPushButton("Start Processing", self)
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)
        self.layout.addWidget(self.start_button)

        self.status_label = QtWidgets.QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if 'ASINs' not in df.columns or 'Keywords' not in df.columns:
                    QMessageBox.critical(self, "Error", "Excel file must contain 'ASINs' and 'Keywords' columns")
                    return

                self.uploaded_data = {
                    'asins': df['ASINs'].tolist(),
                    'keywords': df['Keywords'].tolist()
                }
                self.file_label.setText(f"File: {file_path.split('/')[-1]}")
                self.start_button.setEnabled(True)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read Excel file: {str(e)}")

    def start_processing(self):
        if not self.uploaded_data:
            QMessageBox.warning(self, "Warning", "Please upload a file first")
            return

        self.status_label.setText("Processing...")
        self.start_button.setEnabled(False)
        self.upload_button.setEnabled(False)

        # Create and start worker thread
        self.worker = ScraperWorker(self.uploaded_data)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()

    def update_progress(self, current, total):
        progress = min(100, int((current / total) * 100))
        self.progress_bar.setValue(progress)

    def processing_finished(self, results):
        self.status_label.setText("Processing completed!")
        self.start_button.setEnabled(True)
        self.upload_button.setEnabled(True)
        
        try:
            # Ask user where to save the file
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Results",
                f"amazon_rankings_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:  # Only save if user selected a location
                from src.utils.excel_handler import save_to_excel
                output_file = save_to_excel(results, file_path)
                QMessageBox.information(self, "Success", f"Results saved to: {output_file}")
            else:
                self.status_label.setText("Save cancelled by user")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")

    def processing_error(self, error_message):
        self.status_label.setText("Error occurred!")
        self.start_button.setEnabled(True)
        self.upload_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Processing failed: {error_message}")