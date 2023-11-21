from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Book {self.book_name}>"

@app.route('/book', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher} for book in books])

@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher})

@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify({"message": "Book updated"})

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

if __name__ == '__main__':
    app.run(debug=True)
