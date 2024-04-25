from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


# Define a Pydantic model for a Blog
class Blog(BaseModel):
    id: int
    title: str
    content: str


app = FastAPI()

# Sample data
blogs = [
    {"id": 1, "title": "First Blog", "content": "Content of the first blog"},
    {"id": 2, "title": "Second Blog", "content": "Content of the second blog"},
]


# Create a new blog
@app.post("/blogs/")
def create_blog(blog: Blog):
    blogs.append(blog.dict())
    return blog


# Get all blogs
@app.get("/blogs/")
def get_blogs():
    return blogs


# Get a single blog by ID
@app.get("/blogs/{blog_id}")
def get_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")


# Update a blog
@app.put("/blogs/{blog_id}")
def update_blog(blog_id: int, blog: Blog):
    for i, b in enumerate(blogs):
        if b["id"] == blog_id:
            blogs[i] = blog.dict()
            return {"message": "Blog updated successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")


# Delete a blog
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    for i, blog in enumerate(blogs):
        if blog["id"] == blog_id:
            del blogs[i]
            return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")
