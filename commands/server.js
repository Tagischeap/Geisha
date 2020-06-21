module.exports = {
	name: 'server',
	description: 'Gives current server info.',
	execute(message) {
    message.channel.send(`
    Server name: ${message.guild.name}
    Total members: ${message.guild.memberCount}
    `);
	},
};
