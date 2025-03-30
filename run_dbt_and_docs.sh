
# Go to dbt folder
cd dbt || exit

# Clean any former content 
echo "Cleaning old dbt artifacts..."
dbt clean

# Build dbt models
echo "Running dbt models..."
dbt run

# Generate dbt documents
echo "Generating dbt docs..."
dbt docs generate


echo "All done!"

