package database

import (
	"database/sql"
	"fmt"
	"log"
	"low-effort-sns-2/util"
	"os"
)

func InitDB() *sql.DB {
	db, err := sql.Open("sqlite", "/tmp/db.sqlite")
	if err != nil {
		log.Fatalln("failed to open sqlite db")
	}

	err = db.Ping()
	if err != nil {
		log.Fatalln("db may not have been opened properly")
	}

	initTable := `CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    bio TEXT,
    secret TEXT,
    role TEXT NOT NULL DEFAULT 'user'
);

CREATE TRIGGER IF NOT EXISTS enforce_default_role
AFTER INSERT ON user
FOR EACH ROW
WHEN (NEW.role IS NULL OR NEW.role = '')
BEGIN
    UPDATE user
      SET role = 'user'
    WHERE id = NEW.id;
END;


CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postname TEXT NOT NULL,
    postcontent TEXT NOT NULL,
    is_secret BOOLEAN NOT NULL DEFAULT 0,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);
`

	_, err = db.Exec(initTable)
	if err != nil {
		log.Fatalln("error occured during init table:", err)
	}

	return db
}

func InitAdminAccount(db *sql.DB) {
	insertUser := `INSERT INTO user (username, password, fullname, bio, secret, role)
                   VALUES (?, ?, ?, ?, ?, ?)`

	username := "admin"
	password := util.HashPassword(os.Getenv("ADMIN_PASSWORD"))
	bio := "The owner of low-effort-sns, a revolutionary idea to bring human closer to others."
	secret := fmt.Sprintf("Please don't tell anyone this. The flag is %s", os.Getenv("FLAG"))
	role := "admin"

	_, err := db.Exec(insertUser, username, password, username, bio, secret, role)
	if err != nil {
		log.Fatalln(err)
	}
}
