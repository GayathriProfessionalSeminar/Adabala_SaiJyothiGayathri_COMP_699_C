# ChessMind Mirror

## Project Overview
**ChessMind Mirror**, developed by *Sai Jyothi Gayathri N Adabala*, is an innovative, psychology-focused chess reflection system that transforms the traditional chess-playing experience into a platform for self-awareness and cognitive insight. Unlike conventional chess engines or learning tools, this system uses gameplay patterns to analyze decision-making behavior and link it to real-life psychological traits.  

The project combines cognitive psychology principles with computational logic to help users understand their emotional and strategic tendencies through interactive gameplay and reflective analysis.

---

## Objectives
- To provide a **self-reflective** platform that connects chess strategies with thinking and emotional patterns.  
- To encourage **mindful gameplay** that promotes better decision-making and emotional balance.  
- To analyze move patterns, time taken per move, and risk tendencies using a data-driven approach.  
- To provide **psychologically informed feedback** that supports self-improvement and stress management.  

---

## Features
- **Interactive Chess Interface** built with Streamlit and python-chess.  
- **Behavioral Analytics**: Move timing, repetition detection, and decision confidence analysis.  
- **Psychology-Based Insights**: Interpretation of user behavior in chess contexts to real-life analogies.  
- **Offline Functionality**: No external database dependencies; all data handled locally for privacy.  
- **Secure Data Handling** with AES-256 encryption for user profiles and reports.  
- **Personalized Reports**: Automatically generated PDFs summarizing gameplay, strengths, and reflection points.  
- **Adaptive Feedback System**: Adjusts insights and tips according to user’s playing style and performance trends.  

---

## System Design and Implementation

### Major Components
1. **User Interface**: Developed entirely in Python using **Streamlit**, ensuring simplicity and accessibility.  
2. **Gameplay Logic**: Managed through **python-chess** to enable move validation, rule enforcement, and board updates.  
3. **Data Analysis**: Performed using **Pandas** for tracking and analyzing behavioral patterns.  
4. **Visualization**: Created with **Plotly** to provide dynamic charts and comparative insights.  
5. **Reporting Module**: Implemented with **ReportLab** to generate personalized and printable psychological reflection summaries.  
6. **Security Layer**: Ensures local data encryption and user confidentiality.  

### Design Considerations
- The application is **modular**, with distinct layers for interface, logic, data, and reports.  
- Focused on **usability and accessibility**, ensuring minimalistic design and responsive layout.  
- Built with **privacy-first principles**, operating entirely offline.  
- Ensures smooth performance without database overhead or external dependencies.  

---

## Installation

### Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### Setup Instructions
1. Clone the repository:
   git clone https://github.com/<your-username>/ChessMind-Mirror.git
   cd ChessMind-Mirror
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application
   streamlit run app.py
