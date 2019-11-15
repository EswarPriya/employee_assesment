#!/bin/bash
 
###################################################
# First Bash Shell script to execute psql command 
###################################################
  
#Execute few psql commands: 
createdb employee_ass;
psql employee_ass;
create user employee2 with password 'employee2';
\q

