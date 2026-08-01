import sqlite3
from datetime import datetime

DATABASE_PATH = "docmind.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            file_type TEXT NOT NULL, 
            file_size INTEGER NOT NULL,
            chunk_count INTEGER NOT NULL,
            upload_time TEXT NOT NULL,
            extracted_text TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def save_document(name, file_type, file_size, chunk_count, extracted_text):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO documents (name, file_type, file_size, chunk_count, upload_time, extracted_text)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, file_type, file_size, chunk_count, datetime.now().isoformat(), extracted_text))
    document_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return document_id


def get_all_documents():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, file_type, file_size, chunk_count, upload_time FROM documents")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_document_by_id(document_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return dict(row)
    return None


def delete_document(document_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    connection.commit()
    connection.close()
