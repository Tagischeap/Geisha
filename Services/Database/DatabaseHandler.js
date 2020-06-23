const {
  DBHost, DBName, DBUser, DBPassword
} = require('../config.json');
const Sequelize = require('sequelize');

const sequelize = new Sequelize(DBName, DBUser, DBPassword, {
	host: DBHost,
	dialect: 'mysql',
	logging: false,
});
