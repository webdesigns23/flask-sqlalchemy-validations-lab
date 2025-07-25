from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
from marshmallow import Schema, fields, ValidationError, validates_schema, validate

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators     
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name must be provided.")
        author_exists = Author.query.filter_by(name=name).first()
        if author_exists:
            raise ValueError("Author name must not already exist")
        return name
    
    @validates('phone_number')
    def validates_phone_number(self, key, phone_number):
        phone_number = phone_number.strip()
        if not (phone_number.isdigit() and len(phone_number)==10):
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validates_title(self,key, title):
        clickbait_phrase = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrase):
            raise ValueError("Title must be clickbait-y and contain: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title
    
    @validates('content')
    def validates_content(self,key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content
    
    @validates('category')
    def validates_category(self,key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError(" Post must be categorized as Fiction or Non-Fiction.")
        return category
    
    @validates('summary')
    def validates_summary(self,key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
