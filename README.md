<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=260&section=header&text=NeoForge%20v0.5&fontSize=90&fontAlignY=38&animation=twinkling"/>

<h3 align="center">The safest read-only AI terminal assistant — ever.</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Any-black?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google"/>
  <img src="https://img.shields.io/badge/Security-100%25%20Read--Only-critical?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Made%20in-India-%23FF9933?style=for-the-badge&logo=india"/>
</p>

<p align="center">
  Android • Linux • macOS • Windows (WSL) • 2 GB to 64 GB — boots in <500 ms everywhere
</p>

## Features
- Strictly read-only — 23 safe commands including ls, cat, grep, find, date, uptime, ps, free, du, df and more (zero chance of rm, sudo, cd, pip, or file modification)
- Physically impossible to run rm, sudo, cd, pip, wget, chmod, delete, or modify anything
- Bank-level command + character filtering
- Gorgeous hacker-terminal UI powered by Rich
- Zero escape possible — even if Gemini goes rogue

## Install (under 2 minutes)

```bash
git clone https://github.com/yourusername/NeoForge.git
cd NeoForge
cp .env.example .env          # add your Gemini key
`python -m venv venv`
Windows: `.\venv\Scripts\activate`
macOS/Linux: `source venv/bin/activate`
pip install -r requirements.txt
python neoforge_safe_v0.5.py
