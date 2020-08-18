__export_mysql() {
echo "Running the export_mysql function."

echo "Export data to backup."

mysqldump -u$MYSQL_DATABASE_BACKUP_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > ./scripts/$MYSQL_DATABASE_BACKUP_SQL

echo "Finished exporting data to backup."

}

# Call all functions
__export_mysql
