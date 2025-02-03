import socket
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.wsgi import WSGIMiddleware


#import fundsviewer.fundsviewer

async def wait_for_event(event: asyncio.Event) -> None:
    await event_initialized.wait()

event_initialized = asyncio.Event()

# ---------------------- startup & shutdown
# lifespan events instead of @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/
    """
    logging.info("# Starting API and initializing all objects.")
    
    # ## load data
    #logging.info("# Downloading data.")
    #app.state.dataframes = {}
    #app.state.datatables = {}
    
    #generali_downloader = fundsviewer.fundsviewer.GeneraliFundWebsite()
    #logging.info(f"# Downloading data from {generali_downloader.web_url}")
    #generali_df = generali_downloader.from_csv()
    #app.state.dataframes['generali'] = generali_df
    #app.state.datatables['generali'] = generali_df.to_html()
    
    
    # Load the ML model
    # ...
    
    # mark ending of startup actions
    event_initialized.set()
    
    # wait until closing the app
    yield
    
    # Shutdown
    # ...
    
    logging.info("# Closing API.")

mainapp = FastAPI(lifespan=lifespan)

# ---------------------- security





# ---------------------- other

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
