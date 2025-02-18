import os
import sys
import sqlite3
import psycopg2
from sqlalchemy import create_engine, text
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
import subprocess
import pyqtgraph as pg

from Mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # Initialising first tab.
        self.loadingLabel.setVisible(False)
        self.databasePathLabel.setVisible(False)
        self.databasePathLineEdit.setVisible(False)
        self.typeComboBox.currentTextChanged.connect(self.change_database_type)
        self.pushButton.clicked.connect(self.submit_clicked)
        # Initialising second tab.
        self.postgreSQLurl.setVisible(False)
        self.plot = pg.plot()
        self.bargraph = pg.BarGraphItem(x=[0, 1, 2], height=[0, 0, 0], width = 0.6, brush="g")
        self.plot.addItem(self.bargraph)
        self.plot.getAxis('bottom').setTicks([[(0, 'positive'), (1, 'neutral'), (2, 'negative')]])
        self.plot.setYRange(0, 10)
        self.plot.setTitle("Positive, Neutral, and Negative Reviews")
        self.graphLayout.addWidget(self.plot)
        self.queryButton.clicked.connect(self.get_project)
        self.comboBox_2.currentTextChanged.connect(self.show_postgre_url)

    def show_postgre_url(self, opt):
        '''
        Show or hide a LineEdit Widget depending on the value of opt
        :param opt: A string that can be both sqlite or post.
        '''
        if opt == "sqlite":
            self.postgreSQLurl.setVisible(False)
        else:
            self.postgreSQLurl.setVisible(True)

    def change_database_type(self, text):
        '''
        Based on text show or hide widgets
        :param text: can be sqlite or post
        '''
        if text == "sqlite":
            self.databasePathLabel.setVisible(False)
            self.databasePathLineEdit.setVisible(False)
        else:
            self.databasePathLabel.setVisible(True)
            self.databasePathLineEdit.setVisible(True)
    
    def submit_clicked(self):
        '''
        Run data pipeline.
        '''
        # Collect inputs and safe some to use for when the pipeline finishes
        category = self.comboBox.currentText()
        title = self.titleLineEdit.text()
        self.last_title = title
        type_database = self.typeComboBox.currentText()
        self.last_db_type = type_database
        connection_string = self.databasePathLineEdit.text() if type_database == "post" else "database/product.db"
        connection_string = connection_string.strip()
        self.last_connection_string = connection_string
        description = self.textEdit.toPlainText()

        # Checking that all necessary inputs are defined
        if ((title.strip() == "") or (description.strip() == "") or
                ((connection_string.strip() == "") and type_database == "post")):
            self.loadingLabel.setText('''<html><head/><body><p><span style=" font-weight:600; color: red;">
            Missing inputs.</span></p></body></html>''')
            self.loadingLabel.setVisible(True)

            return
        # Showing loading text and disabling submit button
        self.loadingLabel.setText('''<html><head/><body><p><span style=" font-weight:600; color: red;">
        Downloading data, processing it, and uploading it to the database.
        This process may take a while...</span></p></body></html>''')
        self.loadingLabel.setVisible(True)

        self.pushButton.setEnabled(False)

        # Runing pipeline

        self.process = subprocess.Popen(["python", "add_to_database.py", "-c", category, "-ti", title,
                                         "-d", description, "-t", type_database, "-db", connection_string],
                                        stdout=None, stderr=None)

        # Set up a timer to check if the process finished every 500 ms.
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_process)
        self.timer.start(500)  # Check every 500 ms

        return

    def check_process(self):
        '''
        Check if the process runing the pipeline finished, if it did, change to tab View and
        perform a query to the newly created proposal
        '''
        if self.process.poll() is not None:
            self.project_name.setText(self.last_title)
            self.tabWidget.setCurrentIndex(1)
            self.loadingLabel.setVisible(False)
            self.pushButton.setEnabled(True)

            if self.last_db_type != "sqlite":
                self.comboBox_2.setCurrentText("postgreSQL")
                self.postgreSQLurl.setText(self.last_connection_string)

            self.get_project()

            self.timer.stop()

    def get_row_by_title(self, title_value):
        '''
        Get row from table new_products with specific title. This function works with SQLite
        :param title_value: title to query
        :return:
        array ---- array with the row returned
        '''
        conn = sqlite3.connect("database/product.db")
        cursor = conn.cursor()

        query = f"SELECT * FROM new_products WHERE title = ?"
        cursor.execute(query, (title_value,))

        row = cursor.fetchone()  # Retrieve one matching row
        conn.close()

        return row

    def get_row_by_title_postgre(self, title_value, connection_url):
        '''
        Get row from table new_products with specific title. This function works with PostgreSQL
        :param title_value: title to query
        :param connection_url: connection url to PostgreSQL database in string format.
        :return:
        array ---- array with the row returned
        '''
        # Create an engine
        engine = create_engine(connection_url)

        # Use the engine to execute the query
        with engine.connect() as conn:
            query = "SELECT * FROM new_products WHERE title = :title_value"
            result = conn.execute(text(query), {"title_value": title_value})

            # Fetch one row that matches
            row = result.fetchone()

        return row

    def get_project(self):
        '''
        Collect information from table new_products based on the title inputed in widget project_name.
        This function updates certain labels to display some metrics and updates a barplot showing ammount of positive,
        negative and neutral reviews.
        '''
        self.queryButton.setEnabled(False)
        p_name = self.project_name.text()
        db_type = self.comboBox_2.currentText()


        if db_type == "sqlite":
            project_metrics = self.get_row_by_title(p_name)
        else:
            url_connection = self.postgreSQLurl.text().strip()
            if url_connection != "":
                project_metrics = self.get_row_by_title_postgre(p_name, url_connection)
            else:
                project_metrics = None

        if project_metrics:
            positive_reviews = project_metrics[3]
            neutral_reviews = project_metrics[4]
            negative_reviews = project_metrics[5]

            average_price = project_metrics[6]
            average_rating = project_metrics[7]
            average_review_rating = project_metrics[8]
            verified_purchases = project_metrics[9]
            rating_number = project_metrics[10]
            review_number = project_metrics[11]

            # Updating labels to show metrics
            self.averageReviewRatingLabel.setText(f"Average Review Rating: {average_review_rating}")
            self.averageRatingLabel.setText(f"Average Rating: {average_rating}")
            self.AveragePriceLabel.setText(f"Average Price: {average_price}")
            self.reviewNumbLabel.setText(f"Number of Reviews: {review_number}")
            self.ratingNumberLabel.setText(f"Number of Ratings: {rating_number}")
            self.verifiedPurchasesLabel.setText(f"Verified Purchases: {verified_purchases}")
             # Creating graph to display positive, negative and neutral reviews

            self.bargraph.setOpts(height=[positive_reviews, neutral_reviews, negative_reviews])
            self.plot.setYRange(0, max(positive_reviews, neutral_reviews, negative_reviews) + 10)
            self.plot.update()
        else:
            self.averageReviewRatingLabel.setText("Average Review Rating:")
            self.averageRatingLabel.setText("Average Rating:")
            self.AveragePriceLabel.setText("Average Price:")
            self.reviewNumbLabel.setText("Number of Reviews:")
            self.ratingNumberLabel.setText("Number of Ratings:")
            self.verifiedPurchasesLabel.setText("Verified Purchases:")

            self.bargraph.setOpts(height=[0, 0, 0])
            self.plot.setYRange(0, 10)
            self.plot.update()

            print(project_metrics)

        self.queryButton.setEnabled(True)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()