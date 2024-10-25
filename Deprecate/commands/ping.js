const {
  prefix
} = require('../config.json');
module.exports = {
	name: 'ping',
  aliases: ['pong', 'beep', 'boop', 'bop', 'pop', 'bing', 'bong', 'foo'],
	description: 'Very important command!',
	execute(message) {
		const alias = message.content.toLowerCase().slice(prefix.length);
		console.log(alias);
		if (alias == 'pong') {
			message.channel.send('Ping!');
		}
		else if (alias == 'beep') {
			message.channel.send('Boop!');
		}
		else if (alias == 'boop') {
			message.channel.send('Beep!');
		}
		else if (alias == 'bop') {
			message.channel.send('Pop!');
		}
		else if (alias == 'pop') {
			message.channel.send('Bop!');
		}
		else if (alias == 'bing') {
			message.channel.send('Bong!');
		}
		else if (alias == 'bong') {
			message.channel.send('Bing!');
		}
		else if (alias == 'foo') {
			message.channel.send('bar');
		}
		else {
			message.channel.send('Pong!');
		}
	},
};
