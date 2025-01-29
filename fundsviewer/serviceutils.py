import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.wsgi import WSGIMiddleware





# ---------------------- startup & shutdown
# lifespan events instead of @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/
    """
    logging.info("# Starting API and initializing all objects.")
    
    # ## load data
    logging.info("# Downloading data.")
    app.state.dataframes = {}
    
    generali_downloader = fundsviewer.GeneraliFundWebsite()
    logging.info(f"# Downloading data from {generali_downloader.web_url}")
    generali_df = downloader.get_data()
    app.state.dataframes['generali'] = generali_df
    
    # Load the ML model
    # ...
    
    # wait until closing the app
    yield
    
    # Shutdown
    # ...
    
    logging.info("# Closing API.")



# ---------------------- security





# ---------------------- other

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
