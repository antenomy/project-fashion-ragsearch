
# Full pipeline

preprocessing.py
1. Extract ids from raw input and old id file
    - Remove duplicates

    1b. OPTIONAL split-up.py
        - Split up preprocessing.txt to several files for scraping

scraper
2. Scrape ids from product page
    - Save list of failed atempts

refine.py
3. Refine for required parameters
    - Remove ids that don't fulfill basic requirements
4. Refine for non-nullable field
    - Add fake price if non-existant
5. Transform to product json structure
    - Save non-performant ids for re-scraping

embedd.py
6. Insert into database
7. Add embeddings to database entries



# Counts:
Extracted Product IDs: 5356
Sucessful Scraped Product IDs: 4944
Article IDs refined: 11273

Average Tokens: 159
Total Tokens: 1793308

Article Added and Embedded: 11273

# Usage

### Preprocessing
`python -m data_pipeline.preprocessing`

### Scraper
`cd data_pipeline/scraper`
`mvn clean compile exec:java -Dexec.mainClass="com.lucas.grant.Main"`

### Pipeline
`cd ../..`
`python -m data_pipeline.pipeline`



# Raw data extracted from product tool

**Settings:**
- Brand: Placeholder
- Region: Great Britain
- Language: UK English
- Group: Man
- Age: Adult
- Trademark: Placeholder

**Searches:**
- jackets
- shoe
- t-shirt
- hat
- cap
- pants
- hoodie
- sweater
- tanktop
- "vest top"
- cardigan
- "shorts"
- "sweatpants"
- "sneakers"
- "boots"
- parka
- bomber
- "rain"
- trench
- belt
- sunglasses
- ring