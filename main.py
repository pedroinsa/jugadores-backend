from fastapi import FastAPI
from database import engine
import models
import routes.users.get_routes as users_get_routes
import routes.users.post_routes as users_post_routes
import routes.users.route_me as route_me
import routes.users.patch_routes as users_patch_routes
import routes.players.get_routes as players_get_routes
import routes.players.post_routes as players_post_routes
import routes.players.delete_routes as player_delete_routes
import routes.players.patch_routes as player_patch_routes



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_get_routes.router)
app.include_router (users_post_routes.router)
app.include_router(route_me.router)
app.include_router(users_patch_routes.router)

app.include_router(players_get_routes.router)
app.include_router(players_post_routes.router)
app.include_router(player_delete_routes.router)
app.include_router(player_patch_routes.router)