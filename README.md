# Plotline: AI-Powered Narrative Analysis Dashboard

> **Experimental Research Project** - Unraveling Tomorrow: How AI Traces the Plotlines of Emerging Trends

A cutting-edge web-based dashboard for analyzing and visualizing complex social narratives using AI-driven nested topic analysis. This experimental tool transforms how researchers understand trend evolution by revealing the hidden architecture of social conversations through hierarchical topic modeling and interactive visualizations.

## Research Focus

**AI-Based Trend Identification and Explanation Through Nested Advanced Topic Analysis**

This project explores how hierarchical topic modeling and interactive visualization can reveal patterns in social discourse that traditional linear analysis methods miss. By employing nested circle-packing algorithms and real-time sentiment analysis, Plotline enables researchers to explore social conversations at multiple levels simultaneously.

## Key Features

- **Nested Topic Visualization**: Interactive circle-packing diagrams showing hierarchical topic relationships
- **Real-time Sentiment Analysis**: Dynamic sentiment mapping across topic clusters
- **Demographic Persona Mapping**: Gender and demographic breakdowns within topics
- **Narrative Evolution Tracking**: Temporal analysis of how topics develop and relate
- **Interactive Exploration**: Seamless navigation from macro trends to granular insights
- **API Integration**: Direct connection to Infegy Starscape API for live data
- **Multi-Dataset Support**: Analysis of various social conversation datasets
- **Real-time Data Processing**: Live topic extraction and sentiment analysis

## Experimental Methodology

This research combines several innovative techniques:

1. **Hierarchical AI-Driven Topic Clustering**: Advanced topic modeling that preserves narrative relationships
2. **Nested Circle-Packing Algorithms**: Visual representation of complex topic hierarchies
3. **Real-time Topic Extraction**: Live processing of social conversation data
4. **Multi-level Sentiment Analysis**: Sentiment mapping across topic clusters and subtopics
5. **Interactive Visual Analytics**: Human-interpretable exploration of AI-generated insights
6. **Social Persona Analysis**: Demographic breakdown and persona identification within topics

## Live Demo

**Experience the tool in action**: [https://henryfchapman.github.io/Plotline/](https://henryfchapman.github.io/Plotline/)

The live demo showcases news-related discourse analysis, demonstrating how the tool reveals hidden narrative patterns and trend evolution.

##  Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript with D3.js for advanced visualizations
- **Backend**: Python for data processing and API integration
- **APIs**: 
  - Infegy Starscape API for social conversation analysis
  - Infegy Atlas API for custom dataset management
- **Visualization**: Custom D3.js circle-packing algorithms
- **Data Processing**: Real-time topic extraction and sentiment analysis
- **Styling**: Google Fonts (Roboto, Inter) for modern typography

## Sample Datasets

The tool includes analysis of various social conversations:
- **Technology and Innovation Conversations**: Tech industry trends and sentiment
- **Social Media Commentary Analysis**: Platform-specific conversation patterns
- **Literature and Book Reviews**: Goodreads data analysis
- **YouTube Content Analysis**: MKBHD comments and engagement patterns

## Installation & Setup

### Prerequisites
- Python 3.x
- Web browser with JavaScript enabled
- Infegy API credentials (Starscape and Atlas)

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/henryfchapman/Plotline.git
cd Plotline
```

2. **Install Python dependencies**:
```bash
pip install requests
```

3. **Set up API credentials**:
   - Create `infegy_starscape_bearer_token.txt` in the root directory
   - Create `infegy_atlas_api_key.txt` in the root directory
   - Add your respective Infegy API keys to these files

4. **Run data collection**:
```bash
python get_data.py
```

5. **Open the dashboard**:
   - Open `index.html` in your browser to explore the dashboard
   - Or serve it locally using a web server

### Advanced Setup

#### Custom Dataset Integration

To analyze your own data:

1. **Prepare your data**:
   - Place CSV files in a `csvs/` directory
   - Ensure columns match the expected format (Video_Title, Video_Date, Video_URL, Comment_Timestamp, Comment_Author, Comment_Text)

2. **Upload to Infegy Atlas**:
```python
from pushing_dataset_to_infegy_api import push_data
push_data("Your Dataset Name")
```

3. **Update dataset configuration**:
   - Modify `get_data.py` to use your dataset ID
   - Run the analysis pipeline

#### Configuration Options

- **API Timeouts**: Adjust `TIMEOUT` and `WAIT_TIME` in `get_data.py`
- **Narrative Count**: Modify `NUM_NARRATIVES` for different analysis depths
- **Data Filtering**: Customize query filters in the API requests

## 📁 Project Structure

```
Plotline/
├── index.html                           # Main dashboard interface
├── get_data.py                          # Data collection and processing
├── pushing_dataset_to_infegy_api.py     # Infegy Atlas API integration
├── plotline_data/                       # Processed analysis datasets
│   ├── Goodreads Data.json
│   ├── MKBHD Comments.json
│   ├── News Summary.json
│   ├── Sample Comments.json
│   └── The Lord of the Rings.json
├── data_manifest.json                   # Dataset metadata and configuration
├── infegy_starscape_bearer_token.txt    # Starscape API credentials
├── infegy_atlas_api_key.txt             # Atlas API credentials
├── .gitignore                           # Git ignore patterns
└── README.md                            # This file
```

## 🔍 Core Components

### Data Processing Pipeline (`get_data.py`)

- **Async API Handling**: Manages Infegy Starscape API's asynchronous processing
- **Nested Narrative Analysis**: Extracts hierarchical topic relationships
- **Persona Analysis**: Identifies demographic patterns within topics
- **Error Handling**: Robust error management for API failures
- **Data Enrichment**: Combines multiple analysis types into unified datasets

### Visualization Engine (`index.html`)

- **D3.js Circle Packing**: Hierarchical topic visualization
- **Interactive Navigation**: Click-to-drill-down functionality
- **Sentiment Color Coding**: Visual sentiment indicators
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Dynamic data loading and display

### API Integration (`pushing_dataset_to_infegy_api.py`)

- **Custom Dataset Management**: Upload and manage custom data
- **CSV to JSON Conversion**: Data format standardization
- **Field Mapping**: Automatic column type detection
- **Batch Processing**: Handle multiple data files

## Research Applications

This experimental methodology is particularly valuable for:

- **Market Research**: Understanding consumer sentiment evolution
- **Social Media Analysis**: Tracking narrative development across platforms
- **Trend Forecasting**: Identifying emerging topics before they become mainstream
- **Brand Monitoring**: Analyzing conversation hierarchies around brands
- **Policy Research**: Understanding public discourse on social issues
- **Content Strategy**: Optimizing content based on audience personas
- **Competitive Intelligence**: Monitoring competitor-related conversations

## 🔬 Experimental Nature

This project represents experimental research in:

- **AI-Assisted Visual Analytics**: Making complex AI outputs human-interpretable
- **Nested Topic Modeling**: Preserving context in hierarchical analysis
- **Real-time Social Analysis**: Processing live conversation data
- **Interactive Data Exploration**: Natural navigation of complex datasets
- **Multi-modal Data Integration**: Combining text, sentiment, and demographic data

## Impact & Innovation

- **Novel Visualization Approach**: First implementation of nested circle-packing for topic analysis
- **Context Preservation**: Maintains narrative relationships often lost in traditional analysis
- **Human-AI Collaboration**: Combines AI processing power with human interpretability
- **Real-time Capabilities**: Processes live social data for immediate insights
- **Scalable Architecture**: Handles multiple datasets and analysis types

## Important Notes

### API Requirements
- **Infegy Starscape API**: Required for narrative analysis and topic extraction
- **Infegy Atlas API**: Required for custom dataset management
- **Rate Limiting**: Be aware of API rate limits and implement appropriate delays

### Data Privacy
- API keys are stored locally and not tracked in version control
- Sensitive data should be handled according to your organization's policies
- Consider data retention policies for processed datasets

### Performance Considerations
- Large datasets may require significant processing time
- Browser memory usage increases with dataset size
- Consider implementing pagination for very large datasets

## Contributing

This is experimental research software. Contributions are welcome in the form of:

- **Methodology improvements**: Enhanced topic modeling algorithms
- **Visualization enhancements**: New chart types and interaction patterns
- **API integration extensions**: Support for additional data sources
- **Documentation improvements**: Better setup guides and tutorials
- **Performance optimizations**: Faster data processing and rendering
- **Bug fixes**: Issue resolution and error handling improvements

### Development Guidelines

1. **Fork the repository** and create a feature branch
2. **Test thoroughly** with different dataset types
3. **Document changes** in code comments and README updates
4. **Follow existing code style** and structure
5. **Submit pull requests** with clear descriptions

## Acknowledgments

- [D3.js](https://d3js.org/) for advanced visualization capabilities
- [Infegy](https://www.infegy.com/) for the Starscape and Atlas APIs
- [Roboto](https://fonts.google.com/specimen/Roboto) and [Inter](https://fonts.google.com/specimen/Inter) fonts for typography
- The research community for feedback and validation
