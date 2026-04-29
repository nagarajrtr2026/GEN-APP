# AI App Generator Backend

This is a complete backend project for an AI App Generator pipeline.
It parses natural language prompts, converts them into intermediate representation, and generates validated JSON configurations for building web applications.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   *Note: Dummy mode is enabled by default (`AI_PROVIDER=dummy`), meaning it will work instantly without any API keys!*

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **API Documentation**
   Open your browser and navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)
   You'll find the interactive Swagger UI to test everything out!

## How to Switch AI Providers
Simply open `.env` and update `AI_PROVIDER` to `gemini`, `claude`, or `openai`:
```env
AI_PROVIDER=gemini
API_KEY=your_real_api_key_here
```
The codebase naturally handles the abstraction!

## Testing
Run tests using pytest:
```bash
pytest app/tests/ -v
```