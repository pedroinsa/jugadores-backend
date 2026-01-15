from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
import routes.player_career.get_routes as player_career_get_routes
import routes.player_career.post_routes as player_career_post_routes
import routes.player_career.patch_routes as player_career_patch_routes
import routes.posts.get_routes as posts_get_routes
import routes.posts.post_routes as posts_post_routes
import routes.posts.patch_routes as posts_patch_routes
import routes.posts.delete_routes as posts_delete_routes
import routes.comments.get_routes as comments_get_routes
import routes.comments.post_routes as comments_post_routes
import routes.comments.patch_routes as comments_patch_routes
import routes.comments.delete_routes as comments_delete_routes
import routes.likes.get_routes as likes_get_routes
import routes.likes.post_routes as likes_post_routes
import routes.likes.delete_routes as likes_delete_routes


models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173", 
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,           
    allow_methods=["*"],              
    allow_headers=["*"],     
)


app.include_router(users_get_routes.router)
app.include_router (users_post_routes.router)
app.include_router(route_me.router)
app.include_router(users_patch_routes.router)

app.include_router(players_get_routes.router)
app.include_router(players_post_routes.router)
app.include_router(player_delete_routes.router)
app.include_router(player_patch_routes.router)

app.include_router(player_career_get_routes.router)
app.include_router(player_career_post_routes.router)
app.include_router(player_career_patch_routes.router)

app.include_router(posts_get_routes.router)
app.include_router(posts_post_routes.router)
app.include_router(posts_patch_routes.router)
app.include_router(posts_delete_routes.router)

app.include_router(comments_get_routes.router)
app.include_router(comments_post_routes.router)
app.include_router(comments_patch_routes.router)
app.include_router(comments_delete_routes.router)

app.include_router(likes_get_routes.router)
app.include_router(likes_post_routes.router)
app.include_router(likes_delete_routes.router)