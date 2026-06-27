import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    reload = os.environ.get("RELOAD", "true").lower() == "true"
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)
