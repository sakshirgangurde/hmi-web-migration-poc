from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi_service.opcua_client import OPCUAClient

opcua_client = OPCUAClient()

@asynccontextmanager
async def lifespan(app: FastAPI):

    await opcua_client.connect()

    yield

    await opcua_client.disconnect()


app = FastAPI(
    title="HMI Web Migration API",
    version="1.0.0",
    lifespan=lifespan
)


class WriteRequest(BaseModel):

    value: object


@app.get("/")
async def root():

    return {
        "message": "HMI Web Migration API is running"
    }


@app.get("/tags/{tag_name}/value")
async def read_tag(tag_name: str):

    try:

        value = await opcua_client.read_value(
            tag_name
        )

        return {
            "tag": tag_name,
            "value": value
        }

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.post("/tags/{tag_name}/value")
async def write_tag(
    tag_name: str,
    request: WriteRequest
):

    try:

        await opcua_client.write_value(
            tag_name,
            request.value
        )

        return {
            "tag": tag_name,
            "value": request.value,
            "message": "Value written successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )