module.exports = {
  name: 'echo',
  aliases: ['say'],
  description: 'Repeat what is said',
  usage: 'Hello.',
  execute(message, args) {
    const fArg = message.content.substr(message.content.indexOf(' ') + 1);
      if (message.member.id == 85164966612570112){
        if (message.member.permissions.has('MANAGE_MESSAGES')) {
          message.channel.send(fArg);
          message.delete({ timeout: 5000, reason: 'For echo' });
        }
        else {
          message.channel.send('"' + fArg + '"');
        }
    }
  },
};
