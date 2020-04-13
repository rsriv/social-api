python3 -m pip install PyMySQL
python3 -m pip install Faker
echo "Generating data..."
rm -rf insertData.sql
python3 gen_data.py
echo "Setting up DB, input MySQL Password for root:"
mysql -u root -p < ./setup.sql
echo "Loading generated data, input MySQL Password for root:"
mysql -u root social -p < ./insertData.sql
alias social-api='python3 api.py'
