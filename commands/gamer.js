module.exports = {
  name: 'gamer',
  description: 'Toggles Gamer status, only works in the Brother guild',
  guildOnly: true,
  execute(message, args) {
	const member = message.member;
  var server = bot.guilds.get(message.guild.id).id;

    if (server === '85236952789442560') {
      const role = guild.roles.cache.find(role => role.name === 'Gamer');
      if (member.roles.cache.some(role => role.name === 'Gamer')) {
        message.channel.send('Bye Gamer.');
        member.roles.remove(role);
      }
      else {
        message.channel.send('Hey Gamer.');
        member.roles.add(role);
      }
    }
  },
};
