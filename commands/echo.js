const {
  oID
} = require('../config.json');
module.exports = {
  name: 'echo',
  aliases: ['say'],
  description: 'Repeat what is said',
  usage: 'Hello.',
  execute(message, args) {
    const fArg = message.content.substr(message.content.indexOf(' ') + 1);
    //message.member.permissions.has('MANAGE_MESSAGES') || 
    if (message.member.id == oID) {
      message.channel.send(fArg);
      /*
      message.delete({
        timeout: 5000,
        reason: 'For echo'
      });
      */
    }
    else {
      message.channel.send('"' + fArg + '"');
    }

  },
};
