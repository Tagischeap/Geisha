module.exports = {
  name: 'purge',
  aliases: ['delete'],
  description: 'Deletes messages in bulk',
  usage: 'purge 10',
  execute(message, args) {
    if (message.member.hasPermission('MANAGE_MESSAGES')) {
      const amount = parseInt(args[0]) + 1;
      if (isNaN(amount)) {
        return message.reply('You didn\'t say how much.');
      }
      else if (amount <= 1 || amount > 100) {
        return message.reply('You need to input a number between 1 and 99.');
      }
      message.channel.bulkDelete(amount, true);
    }
  },
};
