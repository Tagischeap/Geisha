const {
  DBHost, DBName, DBUser, DBPassword
} = require('../../config.json');
const Sequelize = require('sequelize');


const sequelize = new Sequelize(DBName, DBUser, DBPassword, {
	host: DBHost,
	dialect: 'mysql',
	logging: false,
});

const CurrencyShop = sequelize.import('Models/CurrencyShop');
sequelize.import('Models/Users');
sequelize.import('Models/UserItems');

const force = process.argv.includes('--force') || process.argv.includes('-f');

sequelize.sync({ force }).then(async () => {
	const shop = [
		CurrencyShop.upsert({ name: 'Tea', cost: 1 }),
		CurrencyShop.upsert({ name: 'Coffee', cost: 2 }),
		CurrencyShop.upsert({ name: 'Cake', cost: 5 }),
	];
	await Promise.all(shop);
	console.log('Database synced');
	sequelize.close();
}).catch(console.error);
