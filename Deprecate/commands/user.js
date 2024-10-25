module.exports = {
  name: 'user',
	aliases: ['icon', 'pfp', 'avatar', 'avi'],
  description: 'Returns user information.',
  execute(message, args) {
    let person;
    if (!message.mentions.users.size) {
      person = message.author;
    }
    else {
      person = message.mentions.users.first();
    }
    message.channel.send(`
	  Username: ${person.username}
	  ID: ${person.id}
	  Avatar: <${person.displayAvatarURL}>
	  `);
  },
};
