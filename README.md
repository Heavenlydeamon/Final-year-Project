# Eco Heritage 🌿🏛️

**Eco Heritage** is an interactive, AI-powered educational platform designed to bridge the gap between cultural heritage and environmental awareness. It provides a gamified learning experience for students and robust management tools for teachers.

---

## 🚀 Key Features

### 🧠 AI-Powered Quiz Generator
- **Gemma Integration:** Uses the Gemma model (via Ollama) to generate intelligent multiple-choice questions from any text.
- **PDF Extraction:** Upload PDF documents to automatically generate quizzes.
- **Hybrid Distractor Logic:** Combines AI creativity with Python-based logic to ensure high-quality, challenging questions.

### 📜 Heritage & Environment Modules
- **Interactive Storytelling:** Immersive narratives like the "Naranathu Branthan" folklore and Western Ghats environmental studies.
- **Classroom Sessions:** Dedicated modules for lower and upper-class students with tiered complexity.

### 🎮 Gamification & Analytics
- **Progress Tracking:** Real-time analytics for student performance.
- **Linear Progression:** Enforced learning paths to ensure students master content before moving forward.
- **Knowledge Bloom:** Interactive dashboard components using a modern glassmorphic aesthetic.

---

## 🛠️ Tech Stack

- **Backend:** Django 5.2 (Python)
- **AI Engine:** Ollama (Gemma 2), PyMuPDF (fitz)
- **Frontend:** Vanilla JS, CSS (Modern Glassmorphism UI)
- **Database:** SQLite (Local Development)

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) (For AI features)

### 2. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/YourUsername/ecoheritage.git
cd ecoheritage

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup the AI Model
Ensure Ollama is running and pull the Gemma model:
```bash
ollama pull gemma2:2b
```

### 4. Database Initialization
```bash
python manage.py migrate
python manage.py createsuperuser  # Create an admin account
```

### 5. Run the Server
```bash
python manage.py runserver
```

---

## 📂 Project Structure

This project follows a "Soft Restructuring" pattern for better scalability:

```text
ecoheritage/
├── apps/                # Business logic grouped by domain
│   ├── accounts/        # User profiles & Authentication
│   ├── mainapp/         # AI Engine & Core views
│   ├── gamification/    # Progress & Rewards
│   └── ... (6 more)
├── ecoheritage/         # Project configuration (settings, urls)
├── static/              # CSS, JavaScript, and Media assets
└── templates/           # HTML Templates
```

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
