# Infegy Plotline

A powerful web-based dashboard for analyzing and visualizing topic narratives and their relationships using the Infegy API.

## Features

- Interactive visualization of topic hierarchies and relationships
- Real-time data analysis and processing
- Nested narrative exploration
- Sentiment analysis visualization
- Volume trend analysis
- Social personas analysis
- Responsive design for all devices

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript (D3.js)
- Backend: Python
- API: Infegy Starscape API

## Getting Started

### Prerequisites

- Python 3.x
- Web browser with JavaScript enabled
- Infegy API credentials

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/topic-analysis-dashboard.git
cd topic-analysis-dashboard
```

2. Install Python dependencies:
```bash
pip install requests
```

3. Set up your API credentials:
   - Create an `api_key.txt` file in the root directory
   - Add your Infegy API key to the file

### Usage

1. Run the data collection script:
```bash
python get_data.py
```

2. Open `index.html` in your web browser to view the dashboard

3. Use the dropdown menu to switch between different analyses

## Project Structure

```
.
├── index.html              # Main dashboard interface
├── get_data.py            # Data collection and processing
├── get_volume_data.py     # Volume data processing
├── api_key.txt            # API credentials (not tracked in git)
├── infegy_summary.json    # Sample analysis data
└── infegy_summary_2.json  # Additional analysis data
```

## Data Visualization Features

- Circle packing visualization for topic distribution
- Interactive narrative exploration
- Volume trend analysis with time series data
- Sentiment analysis visualization
- Social personas breakdown
- Nested narrative exploration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- API keys are stored in a separate file and excluded from version control
- All sensitive data is handled securely
- No user data is stored or processed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [D3.js](https://d3js.org/) for visualization
- [Infegy](https://www.infegy.com/) for the API
- [Roboto](https://fonts.google.com/specimen/Roboto) and [Inter](https://fonts.google.com/specimen/Inter) fonts

## Support

For support, please open an issue in the GitHub repository. 