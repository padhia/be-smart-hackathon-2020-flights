#! /usr/bin/env python
"A simple REST API to list airports and flights"
import datetime as dt
from pathlib import Path
from typing import List, Any, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic.dataclasses import dataclass
from teradatasql import connect
import uvicorn


@dataclass
class Airport:
	code: str
	name: str
	state_cd: str


@dataclass
class FlightLeg:
	airline_cd: str
	flight_nbr: Optional[int]
	dep_airport_cd: Optional[str]
	arvl_airport_cd: Optional[str]
	arvl_time: Optional[dt.datetime]
	dep_time: Optional[dt.datetime]


sess = connect(Path("tdconn.json").read_text())
app = FastAPI(title="Flights", description="Sample REST API Application")

us_airports_sql = """\
SELECT AIRPRT_CD
	, AIRPRT_NM
	, STATE_PROVNC_CD
FROM AA_DATA_VIEWS.AIRPORT_STATION_CURRENT
WHERE CNTRY_CD = 'US'
	AND STATE_PROVNC_CD = '{}'"""

arrivals_sql = """\
SELECT TOP 10 OPERAT_AIRLN_IATA_CD
	, OPERAT_FLIGHT_NBR
	, ACTL_LEG_DEP_AIRPRT_IATA_CD
	, ACTL_LEG_ARVL_AIRPRT_IATA_CD
	, ACTL_LEG_DEP_LCL_TMS
	, ACTL_LEG_ARVL_LCL_TMS
FROM AA_DATA_VIEWS.FLIGHT_LEG_ARVL_EVENT
WHERE OPERAT_AIRLN_IATA_CD = 'AA'
	AND ACTL_LEG_DEP_AIRPRT_IATA_CD = '{}'
	AND ACTL_LEG_ARVL_AIRPRT_IATA_CD = '{}'
ORDER BY ACTL_LEG_ARVL_LCL_TMS DESC"""


def runsql(sql: str) -> List[List[Any]]:
	"run a sql query and return results"
	with sess.cursor() as csr:
		print(sql)
		csr.execute(sql)
		return csr.fetchall()


@app.get("/", response_class=HTMLResponse)
def root() -> str:
	"Welcome page"
	return"""\
		<h1>Welcome to BE SMART Hackathon</h1>
		<p>This is a sample Python application that uses Teradata database to serve flights data to users via REST API</p>
		"""


@app.get("/airports/{state}")
def airport_list(state: str) -> List[Airport]:
	"return a list of all airports located within a US state"
	return [Airport(*row) for row in runsql(us_airports_sql.format(state))]


@app.get("/arrivals/{airport_departed}/{airport_arrived}")
def read_item(departure: str, arrival: str) -> List[FlightLeg]:
	"return a list of most recent 10 flights arrivals between pair of airports"
	return [FlightLeg(*row) for row in runsql(arrivals_sql.format(departure, arrival))]


if __name__ == "__main__":
	uvicorn.run("flights:app", host='0.0.0.0', port=8000, reload=True)
