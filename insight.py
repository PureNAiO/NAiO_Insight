from pydantic import BaseModel
from fastapi import FastAPI
from utils import Influx

app = FastAPI()
influx = Influx()


class ZabbixData(BaseModel):
    device_name: str
    datas: dict


class WarningData(BaseModel):
    device_name: str
    warn_msg: str


@app.post("/api/datas")
async def zabbix_recv(data: ZabbixData):
    device_name = data.device_name
    metrics = data.datas
    for metric in metrics.items():
        influx.write(pname=device_name, field_tup=metric)


@app.post("/api/warning")
async def topo_warning(data: WarningData):
    influx.write(pname=data.device_name, field_tup=('AlertMsg', data.warn_msg))
