__import_mysql() {
echo "Running the start_mysql function."
echo "Import data from backup."
mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < /scripts/$MYSQL_DATABASE_CREATE_SQL
echo "Finished data from backup."
}

# Call all functions
__import_mysql
