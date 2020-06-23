const Sequelize = require('sequelize');

const sequelize = new Sequelize('taggylan_box', 'taggylan_ghost', 'cxwEhnmc5QYjWp9', {
	host: 'taggy.land',
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
