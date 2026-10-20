# AgentOS — Basic chatbot with persistent MySQL history

## Backend (Windows PowerShell)

1. Open a terminal in `backend`.
2. Create and activate a virtual environment if needed:
   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`, then set your own Gemini API key and MySQL connection URL. Never commit or share `.env`.
5. Start the API from the `backend` directory:
   ```powershell
   uvicorn app.main:app --reload
   ```
6. Test `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`.

The SQLAlchemy models are imported at startup and missing tables are created. `create_all()` does not migrate existing table schemas.

## Frontend

In a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Persistent-memory test

1. Tell AgentOS: `My friend who sits beside me is Satya`.
2. Ask: `Who sits beside me?`
3. Refresh the frontend or restart the backend.
4. Ask again in the same saved chat. The frontend restores the session ID and loads messages from MySQL.

A new chat intentionally starts a separate session. All messages remain in MySQL; the latest 20 messages are sent to Gemini as context.

## Security

Never share `.env`, API keys, or database passwords. Rotate any credentials accidentally exposed in a shared archive or repository.
