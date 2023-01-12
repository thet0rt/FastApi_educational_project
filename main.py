from fastapi import FastAPI, Depends
from routers import auth, todos, users, address
from company import companyapis, dependencies
from starlette.staticfiles import StaticFiles
app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')



app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router,
                   prefix='/companyapis',
                   tags=['companyapis'],
                   responses={418: {'description': 'Internal Use Only'}},
                   dependencies=[Depends(dependencies.get_token_header)]
                   )
app.include_router(users.router)
app.include_router(address.router)


