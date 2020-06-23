const {
  DBHost, DBName, DBUser, DBPassword
} = require('../../config.json');
const Sequelize = require('sequelize');

const sequelize = new Sequelize(DBName, DBUser, DBPassword, {
	host: DBHost,
	dialect: 'mysql',
	logging: false,
});

const Users = sequelize.import('Models/Users');
const CurrencyShop = sequelize.import('Models/CurrencyShop');
const UserItems = sequelize.import('Models/UserItems');

UserItems.belongsTo(CurrencyShop, { foreignKey: 'item_id', as: 'item' });

Users.prototype.addItem = async function(item) {
	const userItem = await UserItems.findOne({
		where: { user_id: this.user_id, item_id: item.id },
	});

	if (userItem) {
		userItem.amount += 1;
		return userItem.save();
	}
	return UserItems.create({ user_id: this.user_id, item_id: item.id, amount: 1 });
};

Users.prototype.getItems = function() {
	return UserItems.findAll({
		where: { user_id: this.user_id },
		include: ['item'],
	});
};

module.exports = { Users, CurrencyShop, UserItems };
