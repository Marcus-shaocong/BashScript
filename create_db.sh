#!/bin/bash

 USER="root"
 PASS="123456"

 mysql -u $USER -p$PASS <<EOF 2>/dev/null
 CREATE DATABASE students;
EOF

[ $? -eq 0 ] && echo Create DB || echo DB already exists

mysql -u $USER -p$PASS students <<EOF  2> /dev/null
 CREATE TABLE students(
id int,
name varchar(100),
mark int,
dept varchar(4)
 );
EOF

[ $? -eq 0 ] && echo Created table students || echo Talbe student already exist

 mysql -u $USER -p$PASS students <<EOF
 DELETE FROM students;
EOF
