import logging

import uvicorn

from fastapi import FastAPI, Response, BackgroundTasks, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler

import fundsviewer.fundsplots
import fundsviewer.fundsviewer
import fundsviewer.middlewares
import fundsviewer.utils.logging
from fundsviewer.utils.errors import APIError

import fundsviewer.serviceutils
from fundsviewer.serviceutils import mainapp as app
print('# API state:',app.state.__dict__)
print('# Dataframes:',fundsviewer.fundsviewer.dataframes.keys())

# set logging with unique process id (correlation_id)
fundsviewer.utils.logging.setup_logging_with_correlation_id(level=logging.INFO)

# define fastapi server
#app = FastAPI(lifespan=fundsviewer.serviceutils.lifespan)
app.add_middleware(fundsviewer.middlewares.CorrelationIdMiddleware)


# -------------------------------------- error handlers --------------------------------------
@app.exception_handler(APIError)
async def api_error_exception_handler(request: Request, exc: APIError):
    """ 
    IMPORTANT:
    we do not log exception in this exception handler
    because all APIErrors are being logged when they are being raised
    in the opposite situation, if this exception handler would log errors
    the error logs would duplicate and the analysis of the logs would be difficult
    # logging.exception(f"Error occured in API.")
    """
    return JSONResponse(status_code=500, content={"message": f"Internal server error"})

@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception):
    logging.critical(f"Unhandled error occured in the API.", exc_info=True)
    return JSONResponse(status_code=500, content={"message": f"Internal server error"})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.warning(
        f"Validation didn't pass for body = {exc.body}, details = {exc.errors()}"
    )
    return await request_validation_exception_handler(request, exc)




# -------------------------------------- endpoints --------------------------------------

# Define the main API endpoint
# TODO: get rid of error with favicon.ico -> https://stackoverflow.com/questions/65599686/fastapi-with-uvicorn-getting-404-not-found-error
@app.get("/")
def index() -> PlainTextResponse:
    return PlainTextResponse("Hello to investing funds comparer.")

# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/dashboard", WSGIMiddleware(fundsviewer.fundsplots.app1.server))

#@app.post("/table/{request}")
#async def table(request: str | None = 'generali') -> HTMLResponse:
    #background_tasks: BackgroundTasks | None = None, # cannot use non-default argument
#) -> HTMLResponse:
@app.get("/table/{fundname}")
async def table(fundname: str) -> HTMLResponse:
    logging.info(f"Received 'GET /table/' {fundname=}")
    if fundname in app.state.dataframes.keys():
        return HTMLResponse(
            content=app.state.datatables[fundname],
            status_code=status.HTTP_200_OK
        )
    else:
        return HTMLResponse(
            content="<html>" + \
                    "<head><title>Error</title></head>" + \
                   f"<body><h1>{fundname} is invalid fund name.</h1></body>" + \
                    "</html>",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@app.get('/test')
async def test(request: Request) -> PlainTextResponse:
    logging.info(f'# test request recieved {request.body()}')
    print(request)
    return PlainTextResponse("Test")



#@prefix_router.get("/readiness")
#def ready_check(request: Request) -> PlainTextResponse:
    #logging.info(f'# readiness request recieved {request.body()}')
    #request.app.state.redis_connector.is_alive()
    #return PlainTextResponse("Ready")

#@prefix_router.get("/health")
#def health_check() -> PlainTextResponse:
    #return PlainTextResponse("Healthy")




# Start the FastAPI server
if __name__ == "__main__":
    port = 9999
    if fundsviewer.serviceutils.is_port_in_use(port):
        raise APIError
    logging.info(f'# Running uvicorn server on port {port}.')
    
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=port,
        workers=1,
        reload=False,
    )
