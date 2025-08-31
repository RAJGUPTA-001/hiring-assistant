#!/usr/bin/env python3
"""
Setup script for TalentScout Hiring Assistant
Helps users install dependencies and configure the application
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print application banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🤖 TalentScout Hiring Assistant          ║
    ║                        Setup Script                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n🔧 Setting up environment configuration...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    env_content = """# Groq API Configuration
# Get your API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional: Customize the model
# Available models: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768
GROQ_MODEL=llama3-8b-8192
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Please update the GROQ_API_KEY in the .env file with your actual API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def run_tests():
    """Run application tests"""
    print("\n🧪 Running tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_app.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                        🎉 Setup Complete!                   ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📋 Next Steps:
    
    1. 🔑 Get your Groq API key:
       - Visit: https://console.groq.com/
       - Sign up and get your API key
    
    2. ⚙️  Configure the application:
       - Open the .env file
       - Replace 'your_groq_api_key_here' with your actual API key
    
    3. 🚀 Run the application:
       streamlit run app.py
    
    4. 🌐 Access the application:
       Open your browser and go to: http://localhost:8501
    
    📚 For more information, check the README.md file
    
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Happy Hiring! 🎯                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup can continue...")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
