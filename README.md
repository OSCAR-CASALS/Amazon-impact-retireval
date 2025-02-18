# Amazon impact retrieval

## Description

A data pipeline and PyQt6 desktop application to evaluate how products fitting a user defined description were seen by
people in 2023 using deep learning models _paraphrase-MiniLM-L6-v2_ and _RoBERTa_.

All data used comes from Amazon review dataset by McAuley Lab.

## Installation

To install the required dependencies to run the program you can use
file requirements.txt as following.

```
pip install -r requirements.txt
```

## Usage

The pipeline can be used from the command line or the desktop app:

### Command line

To run the pipeline from the command line it is just needed to specify the
following arguments:

```
  -c CATEGORY, --category CATEGORY
                        Main category the product belongs to
  -ti TITLE, --title TITLE
                        Title of the product
  -d DESCRIPTION, --description DESCRIPTION
                        Description of the product
  -t TYPE, --type TYPE  It indicates whether to keep the output in a postgresql database (post) or a local sqlite database (sqlite)
  -db DATABASE, --database DATABASE
                        In case argument --type has been set to post, these argument indicates the connection string to the postgreSQL database, otherwise it contains the path where the sqlite database
                        is or will be created.
```
Below an example on how to run the pipeline is shown:

```
python add_to_database.py -c "All_Beauty" -ti "GlowRadiance Vitamin C Serum" -d "Reveal radiant, youthful skin with GlowRadiance Vitamin C Serum. Packed with potent antioxidants, this lightweight formula helps brighten dark spots, even skin tone, and boost collagen production for a natural glow. Infused with hyaluronic acid and botanical extracts, it deeply hydrates, leaving your skin plump, smooth, and refreshed. Perfect for all skin types, this non-greasy, fast-absorbing serum is your go-to for a healthy, luminous complexion. Paraben-Free | Cruelty-Free | Dermatologist-Tested. Get your glow today!" -t "sqlite" -db "database/product.db"
```

### Desktop aplication

To run the desktop application it is just necessary to run script main.py after installing all dependencies

```
python main.py
```

These app is composed of two tabs:

The first tab, under the name of "Add Project", contains a form that must be filled to run the data pipeline.

The second tab, under the name of "View", can be used to query project proposal metrics such as number of positiver reviews, average ratings...

## Structure

This repository is divided in three diferent files in a directory of multiple python functions:

- The directory _src_ contains the functions used by the pipeline.
- The file _add\_to\_database.py_ contains the data pipeline and can be run from the comand line.
- File _main.py_ contains the Back-End of the desktop aplication.
- File _Mainwindow.py_ posseses the Front-End of the desktop aplication.


