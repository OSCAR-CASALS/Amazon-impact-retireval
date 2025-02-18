# Amazon impact retrieval

## Description

A data pipeline and PyQt6 desktop application to evaluate how products fitting a user defined description were seen by
people in 2023.

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
options:
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

To run it from the desktop aplication, it is just necessary to fill the form at 
"Add Project" tab.

In the "View" tab it is possible to query a proposal that is already saved in an sqlite or PostgreSQL database by title.