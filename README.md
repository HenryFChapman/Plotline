# Plotline: AI-Powered Narrative Analysis Dashboard

A web-based dashboard for analyzing and visualizing social narratives using AI-assisted hierarchical topic modeling. This tool is designed to support researchers in identifying and exploring patterns in social conversation data through structured visualizations and interactive analysis.

## Research Focus

**AI-Assisted Trend Analysis via Hierarchical Topic Modeling**

This project investigates how layered topic modeling and interactive visualization can help identify structure and evolution in social discourse. By combining nested visual representations and sentiment analysis, Plotline enables multi-level exploration of complex narrative data.

## Key Features

* **Hierarchical Topic Visualization**: Interactive circle-packing diagrams showing topic relationships
* **Sentiment Mapping**: Visual sentiment trends across clusters
* **Demographic Insights**: Gender and demographic breakdowns within topics
* **Narrative Tracking**: Temporal analysis of topic development
* **Interactive Exploration**: Navigate between broad trends and detailed insights
* **API Integration**: Connects to Infegy Starscape for live data
* **Multiple Dataset Support**: Works across diverse sources
* **Live Data Processing**: On-the-fly topic and sentiment extraction

## Methodology Overview

Plotline integrates several techniques:

1. **Hierarchical Topic Clustering**: Preserves structure within complex narratives
2. **Circle-Packing Visualization**: Represents topic hierarchies graphically
3. **Live Data Processing**: Extracts and updates topics in real-time
4. **Multi-level Sentiment Analysis**: Visualizes sentiment across different topic levels
5. **Interactive Visual Analytics**: Allows human-centered exploration of AI-generated insights
6. **Persona Analysis**: Breaks down audience data by demographics

## Live Demo

Try the dashboard here: [https://henryfchapman.github.io/Plotline/](https://henryfchapman.github.io/Plotline/)

The demo uses news-related data to illustrate how Plotline maps evolving discussions.

## Technical Stack

* **Frontend**: HTML5, CSS3, JavaScript with D3.js
* **Backend**: Python for API integration and data processing
* **APIs**:

  * Infegy Starscape (social conversation analysis)
  * Infegy Atlas (custom dataset uploads)
* **Visualization**: Custom D3.js circle-packing
* **Data Handling**: Live extraction and sentiment mapping
* **Typography**: Google Fonts (Roboto, Inter)

## Example Datasets

Included datasets highlight different domains:

* **Technology Conversations**: Social discussion on tech trends
* **Social Media Analysis**: Platform-specific conversation patterns
* **Literature Commentary**: Goodreads reviews and reactions
* **YouTube Comments**: Viewer sentiment and engagement (e.g., MKBHD)

## Installation & Setup

### Requirements

* Python 3.x
* JavaScript-enabled browser
* Infegy API credentials

### Quick Start

1. **Clone the repository**:

   ```bash
   git clone https://github.com/henryfchapman/Plotline.git
   cd Plotline
   ```

2. **Install dependencies**:

   ```bash
   pip install requests
   ```

3. **Add API keys**:

   * Create `infegy_starscape_bearer_token.txt` and `infegy_atlas_api_key.txt`
   * Paste your respective API keys into these files

4. **Run data pipeline**:

   ```bash
   python get_data.py
   ```

5. **Open the dashboard**:

   * Open `index.html` in a browser
   * Or serve locally via a simple web server

### Custom Dataset Integration

1. **Prepare CSVs**:

   * Add files to the `csvs/` folder
   * Columns should include: `Video_Title`, `Video_Date`, `Video_URL`, `Comment_Timestamp`, `Comment_Author`, `Comment_Text`

2. **Upload to Infegy**:

   ```python
   from pushing_dataset_to_infegy_api import push_data
   push_data("Your Dataset Name")
   ```

3. **Configure dataset**:

   * Update `get_data.py` with your dataset ID

### Configuration

* **Timeouts**: Adjust `TIMEOUT` and `WAIT_TIME` in `get_data.py`
* **Narrative Count**: Change `NUM_NARRATIVES` for more or fewer results
* **Filtering**: Customize filters in API queries

## 📁 Project Structure

```
Plotline/
├── index.html
├── get_data.py
├── pushing_dataset_to_infegy_api.py
├── plotline_data/
│   ├── Goodreads Data.json
│   ├── MKBHD Comments.json
│   ├── News Summary.json
│   ├── Sample Comments.json
│   └── The Lord of the Rings.json
├── data_manifest.json
├── infegy_starscape_bearer_token.txt
├── infegy_atlas_api_key.txt
├── .gitignore
└── README.md
```

## 🔍 Component Overview

### Data Pipeline (`get_data.py`)

* Handles asynchronous API responses
* Extracts and organizes topic hierarchies
* Performs demographic and sentiment analysis
* Manages errors and data merging

### Visualization (`index.html`)

* Uses D3.js for circle-packing
* Enables click-based drill-down
* Sentiment is color-coded
* Layout is responsive for different screens

### API Uploader (`pushing_dataset_to_infegy_api.py`)

* Uploads and manages custom datasets
* Converts CSVs to JSON
* Supports field mapping and batch processing

## Use Cases

Plotline may be useful in areas like:

* **Market Research**: Consumer sentiment and trend analysis
* **Social Media Monitoring**: Mapping narrative change over time
* **Trend Forecasting**: Identifying emerging topics
* **Brand Analysis**: Visualizing brand-related conversations
* **Policy Research**: Exploring public discourse on key issues
* **Content Strategy**: Analyzing audience feedback
* **Competitive Monitoring**: Observing competitor conversations

## Experimental Status

Plotline is part of an exploratory research effort involving:

* **AI-Assisted Visualization**: Translating complex data into interpretable visuals
* **Layered Topic Modeling**: Preserving relationships in hierarchical data
* **Live Data Analysis**: Working with up-to-date conversation streams
* **User-Driven Exploration**: Designing for interactivity and clarity
* **Integrated Data Types**: Merging sentiment, text, and demographic information

## Technical Highlights

* **Visual Design**: First use of nested circle-packing in this context
* **Narrative Context Preservation**: Retains structure in evolving discussions
* **Human-AI Interface**: Supports interpretability of model output
* **Scalability**: Built to handle a variety of dataset types and sizes

## Notes

### API Requirements

* Infegy Starscape: Narrative modeling
* Infegy Atlas: Custom datasets
* Respect rate limits; built-in delays may be needed

### Data Handling

* API keys are stored locally and not included in Git
* Handle sensitive data per organizational policies
* Datasets can grow large—manage storage accordingly

## Acknowledgments

* [D3.js](https://d3js.org/) for visualization
* [Infegy](https://www.infegy.com/) for APIs
* [Roboto](https://fonts.google.com/specimen/Roboto) and [Inter](https://fonts.google.com/specimen/Inter) for fonts
