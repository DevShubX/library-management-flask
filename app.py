from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# Routes for Books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "published_year": b.published_year} for b in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "published_year": book.published_year})

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'], published_year=data['published_year'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created", "id": new_book.id}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    book = Book.query.get_or_404(id)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)
    db.session.commit()
    return jsonify({"message": "Book updated"})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

# Routes for Members
@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{"id": m.id, "name": m.name, "email": m.email} for m in members])

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return jsonify({"id": member.id, "name": member.name, "email": member.email})

@app.route('/members', methods=['POST'])
def create_member():
    data = request.json
    new_member = Member(name=data['name'], email=data['email'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member created", "id": new_member.id}), 201

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.json
    member = Member.query.get_or_404(id)
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    db.session.commit()
    return jsonify({"message": "Member updated"})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted"})

if __name__ == '__main__':
    app.run(debug=True)
